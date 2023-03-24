from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..app import models, schemas
from ..app.database import get_db
from ..app.main import verify_id

routers = APIRouter(
    prefix= "/users",
    tags= ["Users"]
)

@routers.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    check_user = db.query(models.User).filter(models.User.email == user.email).first()
    if check_user is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already exists")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"detail": "User created successfully"}

@routers.get("/{id}", response_model=schemas.UserResponse)
def get_user(id, db: Session = Depends(get_db)) -> schemas.UserResponse:
    id = verify_id(id)
    get_user = db.query(models.User).filter(models.User.id == id).first()
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return get_user