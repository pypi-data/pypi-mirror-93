import mongosql
import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.orm.attributes
from typing import Type, Optional, ClassVar, Union, Tuple

from apiens.views.crud.crud_settings import CrudSettings
from apiens.views.mongoquery_crud.defs import QueryObject


class MongoCrudSettings(CrudSettings):
    """ Settings for MongoSql-enabled Crud Base

    Expectations:
    * crud.query_object: MongoSql query object
    * (optional) crud._mongoquery(_mongoquery: MongoQuery): a hook to customize the MongoQuery before it's finalized
    """
    # MongoQuery class to use for queries. Possible to customize.
    MONGOQUERY_CLASS: ClassVar[Type[mongosql.MongoQuery]] = mongosql.MongoQuery

    # MongoSQL default query object
    _query_defaults: Optional[dict] = None

    # Load only for CRUD operations
    _load_only: Tuple[Union[str, sa.orm.attributes.InstrumentedAttribute]] = ()

    # The MongoQuery object that's going to be used for new queries
    _reusable_mongoquery: Optional[mongosql.MongoQuery] = None

    # Configure

    def load_only(self, *fields: Union[str, sa.orm.attributes.InstrumentedAttribute]):
        """ Configure the names of instance fields that will be loaded for your CRUD handler.

        Only name fields that you're actually going to use in your update() and delete() operations

        Args:
            *fields: Names of fields, attributes, or columns
        """
        self._load_only = fields
        return self

    def query_defaults(self, **query_defaults):
        """ Configure MongoSQL auerying

        Args:
            query_defaults: MongoSQL query defaults
        """
        self._query_defaults = query_defaults
        return self

    def mongosql_config(self, **mongoquery_settings):
        """ Configure MongoSQL auerying

        Args:
            **mongoquery_settings: Settings for MongoQuery.
                See `MongoQuerySettingsDict`.
        """
        self._reusable_mongoquery = mongosql.Reusable(  # noqa
            self.MONGOQUERY_CLASS(self.Model, mongoquery_settings)
        )
        return self

    # Is configured?

    @property
    def _mongoquery_enabled(self):
        """ Check: MongoQuery configured and enabled? """
        return self._reusable_mongoquery is not None

    # Query

    def _mongoquery(self, from_query: sa.orm.Query, query_object: Optional[QueryObject] = None):
        """ Start a MongoSql query using the provided QueryObject and Query

        Args:
            from_query: SqlAlchemy Query to start a MongoSql query from
            query_object: MongoSql Query Object
        """
        # Merge the defaults in
        query_obj = {
            **(self._query_defaults or {}),
            **(query_object or {})
        }

        # Go
        return self._reusable_mongoquery.from_query(from_query).query(**query_obj)
