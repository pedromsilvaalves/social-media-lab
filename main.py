from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class post_model(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"id": 1, "title": "Title 1", "content": "Content 1"},
    {"id": 2, "title": "Title 2", "content": "Content 2"}
]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: post_model):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.put("/posts/{id}")
def update_post(id: int, updated_post: post_model, response: Response):
    new_post_dict = updated_post.dict()
    new_post_dict['id'] = id
    post = find_post(id)
    if post:
        my_posts.remove(post)
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_201_CREATED
    my_posts.append(new_post_dict)
    return new_post_dict


@app.delete("/posts/{id}")
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
