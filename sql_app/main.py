from  typing import List
from  fastapi  import  FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)#テーブル作成

app = FastAPI()
#1リクエストごとにDB接続を作る
def get_db():
    db = SessionLocal()#セッションinstance
    try:
        yield db #DBを渡す
    finally:
        db.close()


#Read ユーザー一覧等を取得するAPI http://127.0.0.1:8000/users/
@app.get("/users/",response_model=List[schemas.User])#response_modelで返す型(Userスキーマのリスト（複数）を指定,設計と違う返り値を返しても自動で削除してくれる
async def read_users(skip:int = 0 , limit: int = 100,db:Session = Depends(get_db)):#何件飛ばすか,（最大何件取得,DB接続を自動で用意
    users = crud.get_users(db, skip=skip, limit=limit)#crudのget_users関数を呼び出してDBからユーザー一覧を取得
    return users#response_model = List[schemas.User]User型のリストだけ返します」 とFastAPIに宣言している。もし余計なデータが混ざっても 自動で削除してくれる

@app.get("/rooms/",response_model=List[schemas.Room])
async def read_rooms(skip:int = 0 , limit: int = 100,db:Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms

@app.get("/bookings/",response_model=List[schemas.Booking])
async def read_bookings(skip:int = 0 , limit: int = 100,db:Session = Depends(get_db)):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

#Create#新しいユーザーをDBに登録する
@app.post("/users/", response_model=schemas.User)#response_modelで返す型(Userスキーマを指定,設計と違う返り値を返しても自動で削除してくれる
async def create_users(user: schemas.UserCreate,db:Session = Depends(get_db)): #classUserを継承
    return crud.create_user(db=db, user=user)#インスタンス化しないのでこの形で返す

@app.post("/rooms/", response_model=schemas.Room)
async def create_rooms(room: schemas.RoomCreate,db:Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)

@app.post("/bookings/", response_model=schemas.Booking)
async def create_bookings(booking: schemas.BookingCreate,db:Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)
