from sqlalchemy import Column, Integer, String, Date, Time
from app.db.database import Base
from datetime import date, datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    provider = Column(String, nullable=False)  # Google, GitHub, etc.
    created_date = Column(Date, default=date.today)  # Automatically stores current date
    created_time = Column(Time, default=datetime.now().time) 
