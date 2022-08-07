import time
import psycopg2

from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class post_model(BaseModel):
    title: str
    content: str
    published: bool = True


is_database_connected = False

while not is_database_connected:
    try:
        conn = psycopg2.connect(
            host="<hostname>",
            dbname="<dbname>",
            user="<db_username>",
            password="<db_password>",
            port=<db_port>,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        is_database_connected = True
        print("Database connection was succesfull")
    except Exception as error:
        print("Database connection failed. Error: ", error)
        time.sleep(2)


@app.get("/posts")
def get_posts():
    sql_query = """
    SELECT * FROM posts    
    """

    cursor.execute(sql_query)
    posts = cursor.fetchall()

    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    sql_query = """
    SELECT * FROM posts 
        WHERE id = %s
    """

    cursor.execute(sql_query, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: post_model):
    sql_query = """
    INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    RETURNING *
    """

    cursor.execute(sql_query, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: post_model):
    sql_query = """
    UPDATE posts
        SET
            title = %s,
            content = %s,
            published = %s
        WHERE 
            id = %s
    RETURNING *
    """

    cursor.execute(sql_query, (post.title, post.content,
                   post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")

    return updated_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    sql_query = """
    DELETE FROM posts
        WHERE id = %s
    RETURNING *
    """

    cursor.execute(sql_query, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
