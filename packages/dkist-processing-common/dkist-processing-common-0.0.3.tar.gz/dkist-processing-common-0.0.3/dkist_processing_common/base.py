"""

"""
import json
from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from os import umask
from pathlib import Path
from typing import Generator
from typing import List
from typing import Optional
from typing import Union

from astropy.io import fits
from dkist_processing_core import TaskBase

from dkist_processing_common._util.graphql import CreateRecipeRunStatusResponse
from dkist_processing_common._util.graphql import graph_ql_client
from dkist_processing_common._util.graphql import RecipeRunInputDatasetQuery
from dkist_processing_common._util.graphql import RecipeRunMutation
from dkist_processing_common._util.graphql import RecipeRunResponse
from dkist_processing_common._util.graphql import RecipeRunStatusMutation
from dkist_processing_common._util.graphql import RecipeRunStatusQuery
from dkist_processing_common._util.graphql import RecipeRunStatusResponse
from dkist_processing_common._util.interservice_bus import CatalogFrameMessage
from dkist_processing_common._util.interservice_bus import CatalogObjectMessage
from dkist_processing_common._util.scratch import WorkflowFileSystem


class TaskBaseExt(TaskBase, ABC):
    @staticmethod
    @contextmanager
    def mask():
        old_mask = umask(0)
        try:
            yield
        finally:
            umask(old_mask)

    @property
    def _scratch(self, scratch_base_path: Union[Path, str, None] = None):
        return WorkflowFileSystem(scratch_base_path=scratch_base_path)

    @property
    def input_dataset_path(self):
        return self._scratch.workflow_base_path / "input_dataset.json"

    @property
    def output_paths(self):
        return self._scratch.find_all(tags=["OUTPUT"])

    def input_dataset(self, section: str = "all") -> Union[dict, None]:
        if not self.input_dataset_path.exists():
            # Get input dataset from db
            input_dataset_response = graph_ql_client.execute_gql_query(
                query_base="recipeRuns",
                query_response_cls=RecipeRunResponse,
                query_parameters=RecipeRunInputDatasetQuery(recipeRunId=self.recipe_run_id),
            )
            # Write document to disk for future use
            self.write_input_dataset(
                input_dataset_response[0].recipeInstance.inputDataset.inputDatasetDocument
            )

        input_dataset_document = self.read_input_dataset()

        section = section.lower()
        if section == "all":
            return input_dataset_document
        return input_dataset_document.get(section, None)

    def write_input_dataset(self, input_dataset):
        self._scratch.write(
            bytes(input_dataset, "utf-8"), self.input_dataset_path.parts[-1], tags=["INPUTDATASET"]
        )

    def read_input_dataset(self) -> dict:
        with self.input_dataset_path.open("r") as f:
            return json.loads(f.read())

    def read_input_fits(self, datatype: str) -> Generator[fits.HDUList, None, None]:
        return self.read_fits(tags=["INPUT", datatype.upper()])

    def write_intermediate_fits(
        self, data: fits.HDUList, datatype: str, tags: Optional[List] = None
    ) -> None:
        relative_path = f"{datatype}.fits"
        full_tags = ["INTERMEDIATE", datatype.upper()]
        if tags:
            for tag in tags:
                full_tags.append(tag)
        self._scratch.write_fits(data=data, relative_path=relative_path, tags=full_tags)

    def write_output_fits(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        # TODO how are filenames determined for output data?
        relative_path = "filename.fits"
        full_tags = ["OUTPUT", "OBSERVE", "L1"]
        if tags:
            for tag in tags:
                full_tags.append(tag)
        self._scratch.write_fits(data=data, relative_path=relative_path, tags=full_tags)

    def read_intermediate_fits(self, datatype: str):
        try:
            paths = self._scratch.find_all(["INTERMEDIATE", datatype.upper()])
            filepath = next(paths)
        except StopIteration:
            raise FileNotFoundError(f"No files found of type {datatype}")
        try:
            next(paths)
        except StopIteration:
            return fits.open(filepath)
        raise RuntimeError(f"More than one file found of type {datatype}")

    def read_fits(self, tags: Union[List, str]):
        filepaths = self._scratch.find_all(tags=tags)
        return (fits.open(filepath) for filepath in filepaths)

    def write_movie(
        self, data
    ):  # TODO Write this method and potentially move it to the movie writing class in 'common'
        pass


class SupportTaskBase(TaskBaseExt, ABC):
    recipe_run_statuses = {
        "INPROGRESS": "Recipe run is currently undergoing processing",
        "COMPLETEDSUCCESSFULLY": "Recipe run processing completed with no errors",
    }

    def change_status_to_in_progress(self):
        self._change_status(status="INPROGRESS", is_complete=False)

    def change_status_to_completed_successfully(self):
        self._change_status(status="COMPLETEDSUCCESSFULLY", is_complete=True)

    def _change_status(self, status: str, is_complete: bool):
        status_response = self.get_message_status_query(status=status)

        # If the status was found
        if len(status_response) > 0:
            # Get the status ID
            recipe_run_status_id = status_response[0].recipeRunStatusId
        else:
            # Add the status to the db and get the new status ID
            recipe_run_status_id = self.add_new_recipe_run_status(
                status=status, is_complete=is_complete
            )

        self.apply_status_id_to_recipe_run(recipe_run_status_id=recipe_run_status_id)

    @staticmethod
    def get_message_status_query(status: str):
        return graph_ql_client.execute_gql_query(
            query_base="recipeRunStatuses",
            query_response_cls=RecipeRunStatusResponse,
            query_parameters=RecipeRunStatusQuery(recipeRunStatusName=status),
        )

    def add_new_recipe_run_status(self, status: str, is_complete: bool) -> int:
        if not isinstance(status, str):
            raise TypeError(f"status must be of type str: {status}")
        if not isinstance(is_complete, bool):
            raise TypeError(f"is_complete must be of type bool: {is_complete}")
        recipe_run_status_response = graph_ql_client.execute_gql_mutation(
            mutation_base="createRecipeRunStatus",
            mutation_response_cls=CreateRecipeRunStatusResponse,
            mutation_parameters=RecipeRunStatusMutation(
                recipeRunStatusName=status,
                isComplete=is_complete,
                recipeRunStatusDescription=self.recipe_run_statuses[status],
            ),
        )
        return recipe_run_status_response.recipeRunStatus.recipeRunStatusId

    def apply_status_id_to_recipe_run(self, recipe_run_status_id: int):
        graph_ql_client.execute_gql_mutation(
            mutation_base="updateRecipeRun",
            mutation_parameters=RecipeRunMutation(
                recipeRunId=self.recipe_run_id, recipeRunStatusId=recipe_run_status_id
            ),
        )

    @property
    def proposal_id(self) -> str:
        try:
            getattr(self, "_proposal_id")
        except AttributeError:
            self._proposal_id = graph_ql_client.execute_gql_query(
                query_base="recipeRuns",
                query_response_cls=RecipeRunResponse,
                query_parameters=RecipeRunInputDatasetQuery(recipeRunId=self.recipe_run_id),
            )[0].recipeInstance.processingCandidate.proposalId
        return self._proposal_id

    def create_frame_message(self, object_filepath: str):
        catalog_frame_message = CatalogFrameMessage(
            objectName=object_filepath, conversationId=str(self.recipe_run_id)
        )
        return catalog_frame_message

    def create_movie_message(self, object_filepath: str):
        catalog_movie_message = CatalogObjectMessage(
            objectType="MOVIE",
            objectName=object_filepath,
            groupId=self.dataset_id,
            conversationId=str(self.recipe_run_id),
        )
        return catalog_movie_message


class ScienceTaskL0ToL1(TaskBaseExt):
    def record_provenance(self):
        pass  # TODO

    @property
    def input_dark_frames(self) -> Generator[fits.HDUList, None, None]:
        return self.read_input_fits(datatype="DARK")

    @property
    def input_gain_frames(self) -> Generator[fits.HDUList, None, None]:
        return self.read_input_fits(datatype="GAIN")

    @property
    def input_target_frames(self) -> Generator[fits.HDUList, None, None]:
        return self.read_input_fits(datatype="TARGET")

    @property
    def input_instpolcal_frames(self) -> Generator[fits.HDUList, None, None]:
        return self.read_input_fits(datatype="INSTPOLCAL")

    @property
    def input_telpolcal_frames(self) -> Generator[fits.HDUList, None, None]:
        return self.read_input_fits(datatype="TELPOLCAL")

    @property
    def input_geometric_frames(self) -> Generator[fits.HDUList, None, None]:
        return self.read_input_fits(datatype="GEOMETRIC")

    def write_dark(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        self.write_intermediate_fits(data=data, datatype="DARK", tags=tags)

    def write_gain(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        self.write_intermediate_fits(data=data, datatype="GAIN", tags=tags)

    def write_target(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        self.write_intermediate_fits(data=data, datatype="TARGET", tags=tags)

    def write_instpolcal(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        self.write_intermediate_fits(data=data, datatype="INSTPOLCAL", tags=tags)

    def write_telpolcal(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        self.write_intermediate_fits(data=data, datatype="TELPOLCAL", tags=tags)

    def write_geometric(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        self.write_intermediate_fits(data=data, datatype="GEOMETRIC", tags=tags)

    @property
    def intermediate_dark(self) -> fits.HDUList:
        return self.read_intermediate_fits(datatype="DARK")

    @property
    def intermediate_gain(self) -> fits.HDUList:
        return self.read_intermediate_fits(datatype="GAIN")

    @property
    def intermediate_target(self) -> fits.HDUList:
        return self.read_intermediate_fits(datatype="TARGET")

    @property
    def intermediate_instpolcal(self) -> fits.HDUList:
        return self.read_intermediate_fits(datatype="INSTPOLCAL")

    @property
    def intermediate_telpolcal(self) -> fits.HDUList:
        return self.read_intermediate_fits(datatype="TELPOLCAL")

    @property
    def intermediate_geometric(self) -> fits.HDUList:
        return self.read_intermediate_fits(datatype="GEOMETRIC")

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method that must be overridden to execute the desired DAG task.
        """
