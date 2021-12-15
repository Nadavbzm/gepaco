import argparse
from protocol_parser import ProtocolParser
import os
from yaml.scanner import ScannerError
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

def main():
    uvicorn.run("server:app", host="127.0.0.1", port=5000, log_level="info")