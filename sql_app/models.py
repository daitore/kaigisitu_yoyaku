from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from  .database import Base

class User(Base):#継承
    __tablename__ = "users"#テーブル名指定
    user_id = Column(Integer, primary_key=True, index=True)#主キー自動、インデックス作成
    username = Column(String, unique=True, index=True)#ユニーク制約、インデックス作成

class Room(Base):#継承
    __tablename__ = "rooms"#テーブル名指定
    room_id = Column(Integer, primary_key=True, index=True)#主キー、インデックス作成
    room_name = Column(String, unique=True, index=True)#ユニーク制約、インデックス作成
    capacity = Column(Integer)#インデックス作成

class Booking(Base):#継承
    __tablename__ = "bookings"#テーブル名指定
    booking_id = Column(Integer, primary_key=True, index=True)#主キー、インデックス作成
    user_id = Column(Integer, ForeignKey("users.user_id",ondelete ="SET NULL"), nullable =False)#userテーブルのuser_id参照紐づけ,親削除時子をNULL
    room_id = Column(Integer, ForeignKey("rooms.room_id",ondelete ="SET NULL"), nullable =False)#roomテーブルのroom_id参照紐づけ,親削除時子をNULL
    booked_num = Column(Integer)#インデックス作成
    start_datetime = Column(DateTime,nullable = False)#日時型
    end_datetime = Column(DateTime,nullable = False)#日時型