import os

from sqlalchemy import create_engine, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column

from datetime import datetime
from typing import Annotated, Optional
from config import config

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "3306"),
    "username": os.getenv("DB_USERNAME", "root"),
    "password": os.getenv("DB_PASSWORD", "admin"),
    "database": os.getenv("DB_DATABASE", config.DB_NAME)
}

DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

engine = create_engine(
    DATABASE_URL,
    echo=True, # SQL打印
    pool_size=10, # 连接池大小
    pool_recycle=3600 # 连接回收时间（秒）
)

# Primary key definition
PrimaryKey = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

class Base(DeclarativeBase):
    ...

class Host(Base):
    """
    主机管理
    """
    __tablename__ = "k_host"

    id: Mapped[PrimaryKey]
    project_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(50))
    ip: Mapped[str] = mapped_column(String(50))
    port: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    # 状态（online/在用 offline/下线）
    status: Mapped[str] = mapped_column(String(50), default="online")
    description: Mapped[Optional[str]] = mapped_column(Text)
    create_time: Mapped[datetime] = mapped_column(default=datetime.now)

Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print(f"database [{config.DB_NAME}] init successfully!")