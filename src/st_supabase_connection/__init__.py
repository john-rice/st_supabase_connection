import os

from postgrest import AsyncRequestBuilder
from streamlit import cache_resource
from streamlit.connections import ExperimentalBaseConnection
from supabase import Client, create_client

__version__ = "0.0.0"


# TODO: Add Supabase Storage connector. Rename `SupabaseConnection` to `SupabaseDBConnection`
# TODO: Update README.md and setup.py
# TODO: Add docstrings with usage examples. Copy docstring from https://postgrest-py.readthedocs.io/en/latest/api/request_builders.html
class SupabaseConnection(ExperimentalBaseConnection[Client]):
    def _connect(self, **kwargs) -> None:
        @cache_resource
        def __connect(_self, **kwargs) -> None:
            if "url" in kwargs:
                url = kwargs.pop("url")
            elif "SUPABASE_URL" in _self._secrets:
                url = _self._secrets["SUPABASE_URL"]
            elif "SUPABASE_URL" in os.environ:
                url = os.environ.get("SUPABASE_URL")
            else:
                raise ValueError(
                    "Supabase URL not provided. "
                    "You can provide the url by "
                    "passing it as the 'url' kwarg while creating the connection, or "
                    "setting the 'SUPABASE_URL' environment variable or Streamlit secret."
                )

            if "key" in kwargs:
                key = kwargs.pop("key")
            elif "SUPABASE_KEY" in _self._secrets:
                key = _self._secrets["SUPABASE_KEY"]
            elif "SUPABASE_KEY" in os.environ:
                key = os.environ.get("SUPABASE_KEY")
            else:
                raise ValueError(
                    "Supabase Key not provided. "
                    "You can provide the key by "
                    "passing it as the 'key' kwarg while creating the connection, or "
                    "setting the 'SUPABASE_KEY' environment variable or Streamlit secret."
                )
            _self.client = create_client(url, key)

        return __connect(self, **kwargs)

    def table(
        self,
        table: str,
    ) -> AsyncRequestBuilder:
        """
        The name of the table to query. This is a string that will be used as the table name in the query.


        Returns:
                An : class : ` AsyncRequestBuilder ` that can be used to make requests to the table's content
        """
        return self.client.table(table)
