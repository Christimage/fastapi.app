from fastapi import Response, status, HTTPException, Depends, APIRouter
# from fastapi.params import Body
# import psycopg2
# from psycopg2.extras import RealDictCursor
from typing import List
from sqlalchemy import desc
from sqlalchemy.orm import Session
from ..app import models, schemas
from ..app.database import get_db
from ..app.main import verify_id

routers = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)

@routers.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)) -> List[schemas.PostResponse]:
    posts = db.query(models.Post).all()
    # getting posts directly from db i.e with db driver
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts


@routers.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db)) -> dict:  
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # creating posts directly to db i.e with db driver
    # cursor.execute("""INSERT INTO posts
    # (title, content, published)
    # VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # db_connect.commit()
    # if you need to fetch the post
    # new_post = cursor.fetchone()
    return {"detail": "Post created successfully"}

#this func must be above the /posts/id get request 
# for both to function as expected
@routers.get("/posts/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db)) -> schemas.PostResponse:
    post = db.query(models.Post).order_by(desc(models.Post.id)).first()
    
    # getting latest added post directly from db i.e with db driver
    # cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
    # post = cursor.fetchone()
    return post

@routers.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id, db: Session = Depends(get_db)) -> schemas.PostResponse:
    id = verify_id(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # getting post directly from db i.e with db driver
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    # post = cursor.fetchone()
    # if post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return post

@routers.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(get_db)) -> None:
    id = verify_id(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
        

    # delete post from db i.e with db driver
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    # post = cursor.fetchone()
    # if post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # else:
    #     db_connect.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@routers.patch("/posts/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update_post(id, post: schemas.PostUpdate, db: Session = Depends(get_db)) -> dict: #pass this line as a func parameter if connecting without ORM #post: dict = Body(...)
    id: str = verify_id(id)
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    for field, value in post.dict(exclude_unset=True).items():
        setattr(db_post, field, value)
    db.commit()
    db.refresh(db_post)

    # query: str = "UPDATE posts SET "
    # values = []
    # if 'title' in post:
    #     query += "title=%s, "
    #     values.append(post['title'])
    # if 'content' in post:
    #     query += "content=%s, "
    #     values.append(post['content'])
    # if 'published' in post:
    #     query += "published=%s, "
    #     values.append(post['published'])
    # query = query[:-2] + " WHERE id=%s RETURNING *"
    # values.append(id)
    # cursor.execute(query, tuple(values))
    # updated_post = cursor.fetchone()
    # if updated_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # else:
    #     db_connect.commit()
    return {"detail": "Post updated successfully"}