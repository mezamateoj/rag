from pydantic import BaseModel, TypeAdapter


class Movie(BaseModel):
    id: int
    title: str
    description: str


MovieListValidator = TypeAdapter(list[Movie])
