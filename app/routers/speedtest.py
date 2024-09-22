from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import speedtest
from .. import models, database

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to run speedtest and save results
@router.post("/speedtest")
def run_speedtest(db: Session = Depends(get_db)):
    try:
        # Run the broadband speed test
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        download_speed = round(download_speed, 1)   # Round to 1dp
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        upload_speed = round(upload_speed, 1)       # Round to 1dp
        ping = st.results.ping

        # print(f"Download: {download_speed}, Upload: {upload_speed}, Ping: {ping}")

        # Save the results to the database
        speedtest_result = models.SpeedTestResult(
            download_speed=download_speed,
            upload_speed=upload_speed,
            ping=ping
        )
        db.add(speedtest_result)
        db.commit()
        db.refresh(speedtest_result)

        return speedtest_result
    except Exception as e:
        return {"error": str(e)}

@router.get("/speedtest/results")
def get_speedtest_results(db: Session = Depends(get_db)):
    results = db.query(models.SpeedTestResult).all()
    return results
