import  datetime
from  pydantic  import  BaseModel,Field

class BookingCreate(BaseModel):#継承
    user_id: int
    room_id: int
    booked_num:int
    start_datetime: datetime.datetime#時間日付
    end_datetime: datetime.datetime

class Booking(BookingCreate):#継承
    booking_id: int

    class Config: #Pydanticの設定
         orm_mode = True #dicでなくORMモードでも有効化

class UserCreate(BaseModel):
    username: str = Field( max_length=12)

class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True

class RoomCreate(BaseModel):
    room_name: str = Field( max_length=12)
    capacity: int
#継承
class Room(RoomCreate):
    room_id: int
    room_name: str = Field( max_length=12)

    class Config:
        orm_mode = True



