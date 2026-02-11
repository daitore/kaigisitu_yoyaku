from  sqlalchemy.orm import Session
from  . import models, schemas

#ユウザー一覧取得
def get_users(db: Session, skip: int = 0,limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()#クエリ発行  、何件からとる、リミット、全件取得

#会議室一覧取得
def get_rooms(db: Session, skip: int = 0,limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()#クエリ発行  、何件からとる、リミット、全件取得

#予約一覧取得
def get_bookings(db: Session, skip: int = 0,limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()#クエリ発行  、何件からとる、リミット、全件取得

#ユウザー登録
def create_user(db: Session, user: schemas.User):#FastAPIのスキーマ受け取りDBに登録
    db_user = models.User(username=user.username)#モデルインスタンス生成
    db.add(db_user)#追加
    db.commit()#コミット
    db.refresh(db_user)#再読込
    return db_user

#会議室登録
def create_room(db: Session, room: schemas.Room):#FastAPIのスキーマ受け取りDBに登録
    db_room = models.Room(room_name=room.room_name,capacity = room.capacity)#モデルインスタンス生成
    db.add(db_room)
    db.commit()#コミット
    db.refresh(db_room)#再読込
    return db_room

#予約登録
def create_booking(db: Session, booking: schemas.Booking):#FastAPIのスキーマ受け取りDBに登録
    db_booking = models.Booking(
        user_id = booking.user_id,
        room_id = booking.room_id,
        booked_num = booking.booked_num,
        start_datetime = booking.start_datetime,
        end_datetime = booking.end_datetime
    )#モデルインスタンス生成
    db.add(db_booking)
    db.commit()#コミット
    db.refresh(db_booking)#再読込
    return db_booking