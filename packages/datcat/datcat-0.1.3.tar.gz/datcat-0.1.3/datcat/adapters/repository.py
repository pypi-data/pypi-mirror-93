import abc
import json
import os
import typing
from glob import glob

from datcat.domain import model


class AbstractRepository:
    @abc.abstractmethod
    def add(self, *args):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *args):
        raise NotImplementedError

    @abc.abstractmethod
    def list_all(self, *args):
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, *args):
        raise NotImplementedError


class SchemaRepository(AbstractRepository):
    # TODO: figure out whether we can have db persistence
    # TODO: rename this to BaseRepository and create two separate classes
    #  that inherit Base for Schema and Configurations
    def __init__(self):
        self.in_memory_schema_repository: model.SchemaRepo = {}

    def add(
        self, schema_key: model.SchemaKey, schema_definition: model.SchemaDefinition
    ) -> None:
        self.in_memory_schema_repository[schema_key] = schema_definition

    def get(self, schema_key: model.SchemaKey) -> model.SchemaDefinition:
        return self.in_memory_schema_repository.get(schema_key)

    def list_all(self) -> model.SchemaRepo:
        return self.in_memory_schema_repository

    def load(self, schemas_path: str) -> None:
        for schema_filename in glob(f"{schemas_path}/*.json"):
            # make sure schema_filename is just a schema_filename so it does not break the schema_path var
            schema_filename = os.path.basename(schema_filename)
            schema_path = os.path.join(schemas_path, schema_filename)
            schema_name = os.path.basename(schema_path).partition(".")[0]
            with open(schema_path, "r") as sp:
                self.add(schema_name, self._validated_json(sp.read()))

    @staticmethod
    def _validated_json(payload: typing.Union[str, bytes]):
        # output = []
        try:
            output = json.loads(payload)
        except json.JSONDecodeError as jde:
            output = [{"JSONDecodeError": f"{jde}"}]
        return output


class MappingsRepository:
    def __init__(self):
        self.in_memory_mappings_repository: model.MappingRepo = {}

    def add(self):
        pass

    def get(self, key: int) -> typing.Dict[str, str]:
        return self.in_memory_mappings_repository.get(key)

    def list_all(self) -> model.MappingRepo:
        return self.in_memory_mappings_repository

    def load(self, mappings_filepath: str) -> None:
        with open(mappings_filepath, "r") as mf:
            self.in_memory_mappings_repository = json.loads(mf.read())
