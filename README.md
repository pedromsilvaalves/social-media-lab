# Social Media Lab

## Details

This project is a social media creation lab, the final objetive is to create a social media end-to-end.

The current objetive is the creation of the back-end API using Python and FastAPI framework.
In this project we will be using PostgreSQL as the database.

The automatic generated API documentation are on the following URLs:

- <http://127.0.0.1:8000/docs>
- <http://127.0.0.1:8000/redoc>

## Requirements

- Python
- PostgreSQL
- FastAPI
- psycopg2
- SQLAlchemy
- Passlib
- Bcrypt

## Setting up the dependencies

### Project packages and extensions

```bash
pip install -r requirements.txt
```

> **Note**
> Generate the requirements.txt by using:
>
> ```bash
> pip freeze > requirements.txt
> ```

or

``` bash
pip install "fastapi[all]"
pip install psycopg2
pip install SQLAlchemy
pip install passlib[bcrypt]
```

### Postgres database setup

All the Postgres database setup is done by the SQLAlchemy(ORM)

Current tables:

- posts
- users

#### Deprecated

Create necessary database tables

SQL for the posts table setup:

```sql
-- This sequence takes care of the Unique IDs of the system
CREATE SEQUENCE IF NOT EXISTS public.posts_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE IF NOT EXISTS public.posts
(
    id integer NOT NULL DEFAULT nextval('posts_id_seq'::regclass),
    title character varying COLLATE pg_catalog."default" NOT NULL,
    content character varying COLLATE pg_catalog."default" NOT NULL,
    published boolean NOT NULL DEFAULT true,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT posts_pkey PRIMARY KEY (id)
);
```

Change the credentials to log into the Database:

```python
# Line 22 @ app/main.py
conn = psycopg2.connect(
            host="<hostname>",
            dbname="<dbname>",
            user="<db_username>",
            password="<db_password>",
            port=<int: db_port>,
            cursor_factory=RealDictCursor # Configure the extension to call the tables headers
        )
```

## How to use

..

### Start the API

```bash
uvicorn app.main:app --reload
```

## References

[Python API Development - Comprehensive Course for Beginners - Sanjeev Thiyagarajan](https://www.youtube.com/watch?v=0sOvCWFmrtA)

