from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()
posts = [
    {"id": 1, "title": "title of post 1", "content": "content of post 1"},
    {"id": 2, "title": "title of post 2", "content": "content of post 2"},
]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    for post in posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for index, post in enumerate(posts):
        if post["id"] == id:
            return index


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} doesn't exist",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} doesn't exists",
        )
    posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} doesn't exists",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    posts[index] = post_dict
    return {"data": post_dict}
