from fastapi import FastAPI
from app.api.predict_time import router as predict_time_router

app = FastAPI()

# Include routers
app.include_router(predict_time_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Count-Time Predict API!"}
