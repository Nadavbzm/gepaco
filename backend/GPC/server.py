import argparse
from .protocol_parser import ProtocolParser
import os
from yaml.scanner import ScannerError
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/", StaticFiles(directory="static",html = True), name="static")

def run():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")