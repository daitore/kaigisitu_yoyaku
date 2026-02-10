from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"#SQLiteのファイル名、同じDRに作成してDBにする

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)#SQLite特有の引数

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#セッション定義
Base = declarative_base()#ベースクラス作成 継承していく