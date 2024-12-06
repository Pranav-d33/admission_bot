# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from query_resolver import resolve_query

app = FastAPI()

# Pydantic model to validate incoming data
class UserQuery(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Query Resolver!"}


@app.post("/resolve-query/")
def resolve_user_query(user_query: UserQuery):
    """
    Resolve the user query and return the best match.
    """
    # Pass the string query to resolve_query
    result = resolve_query(user_query.query)
    return {"query": user_query.query, "result": result}
