from typing import Union

from src.book_id.query.query_model import QueryModel
from src.book_id.query.query_service import QueryService


def build_query_model(query: str) -> Union[QueryModel, IndexError]:
    query_service = QueryService(query)
    return query_service.build_query_model()
