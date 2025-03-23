from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from src.routes import base, data


app = FastAPI()
app.include_router(base.base_router)
