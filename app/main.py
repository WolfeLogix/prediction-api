from fastapi import FastAPI
#from dotenv import load_dotenv
from api.routers import api_router

# Load environment variables from .env file
#load_dotenv('.env')


app = FastAPI(
    title="prediction-api",
    description="API for prediction of price data",
)
app.include_router(api_router)


# TODO - remove this route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
