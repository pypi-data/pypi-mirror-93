import logging
import sys
from dataclasses import dataclass
from typing import ClassVar
from dataclasses_json import DataClassJsonMixin
from pyvise.configuration import get_setting


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def get_logger(name):
    return logging.getLogger(name)


@dataclass
class HasuraBase(DataClassJsonMixin):
    """
    # [Reference Library](https://pypi.org/project/dataclasses-json/)
    # [GraphQL Queries](https://graphql.org/learn/queries/)
    """
    GRAPHQL_BASE: ClassVar[str] = get_setting('HASURA_ENDPOINT')
    __tablename__: ClassVar[str] = 'db_table_name'
    logger = get_logger(__name__)

    @classmethod
    def generate_fields(cls):
      instance = cls()
      field_strings = ""
      attributes = []

      for field in instance.__annotations__:
        if (not field.startswith('__')) and (field[0].islower()) :
          attributes.append(field)

      for idx, annotation in enumerate(attributes, start=1):        
        field_strings += annotation + ( ", " if idx < len(attributes) else "")

      return field_strings

    @classmethod
    def generate_singular_name(cls):
        return 'AccountProfile'
