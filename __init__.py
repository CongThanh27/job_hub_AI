from flask import Flask
from app import refresh_data
from app import get_recommendation_jobs_by_user_id, get_recommendation_users_by_job_id, hello
from collaborative_filtering import CF
from handle_data import process_data, encode_data
from recommendation import user_user_collaborative_filtering, item_item_collaborative_filtering, get_recommendation_user_by_job, get_recommendation_job_by_user
from db_connection import connect_to_database_sql, connect_to_mongodb


def __getattr__(name: str) -> t.Any:
    if name == "__version__":
        import importlib.metadata
        import warnings

        warnings.warn(
            "The '__version__' attribute is deprecated and will be removed in"
            " Flask 3.1. Use feature detection or"
            " 'importlib.metadata.version(\"flask\")' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return importlib.metadata.version("flask")

    raise AttributeError(name)