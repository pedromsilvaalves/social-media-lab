from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # DIRECT METHOD
    # sql_query = """
    # SELECT * FROM posts
    # """
    # cursor.execute(sql_query)
    # posts = cursor.fetchall()

    # ORM METHOD
    posts = db.query(models.Post).all()

    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # DIRECT METHOD
    # sql_query = """
    # SELECT * FROM posts
    #     WHERE id = %s
    # """

    # cursor.execute(sql_query, (str(id),))
    # post = cursor.fetchone()

    # ORM METHOD
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # OR
    post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # DIRECT METHOD
    # sql_query = """
    # INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    # RETURNING *
    # """

    # cursor.execute(sql_query, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # ORM METHOD
    new_post = models.Post(
        **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # DIRECT METHOD
    # sql_query = """
    # UPDATE posts
    #     SET
    #         title = %s,
    #         content = %s,
    #         published = %s
    #     WHERE
    #         id = %s
    # RETURNING *
    # """

    # cursor.execute(sql_query, (post.title, post.content,
    #                post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # ORM METHOD
    db_post = db.query(models.Post).filter(models.Post.id == id)

    if not db_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")

    db_post.update(post.dict(), synchronize_session=False)
    db.commit()

    updated_post = db_post.first()

    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # DIRECT METHOD
    # sql_query = """
    # DELETE FROM posts
    #     WHERE id = %s
    # RETURNING *
    # """

    # cursor.execute(sql_query, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # ORM METHOD
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
