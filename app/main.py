from fastapi import FastAPI, status, HTTPException
# from fastapi.params import Body
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from ..routers import post, user

# setup connection to database using ORM (sqlalchemy)
models.Base.metadata.create_all(bind=engine)

#setup fastapi server
app = FastAPI(docs_url="/docs", redoc_url=None)

#setup connection to database directly using psygopg2
# while True:
    
#     try:
#         db_connect = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='     ', cursor_factory=RealDictCursor)
#         cursor = db_connect.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print(f'Connection to database failed with error {error}')
#         time.sleep(1)

def verify_id(id):
    try:
        isinstance(int(id), int) 
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Id")
    else:
        return id    

app.include_router(post.router)
app.include_router(user.router)


# use the async keyword if the function performs a time consuming task
@app.get("/")
def root() -> dict:
    return {"detail": "Hello World"}

