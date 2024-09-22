from sqlalchemy import Column, Integer, Float, Date, Time
from .database import Base
from datetime import datetime

class SpeedTestResult(Base):
    __tablename__ = "speedtest_results"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    download_speed = Column(Float)
    upload_speed = Column(Float)
    ping = Column(Float)

    def __init__(self, download_speed, upload_speed, ping):
        self.download_speed = download_speed
        self.upload_speed = upload_speed
        self.ping = ping
        now = datetime.now()
        self.date = now.date()
        self.time = now.strftime("%H:%M:%S")  # Format time as string
