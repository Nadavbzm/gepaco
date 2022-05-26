import argparse
from fileinput import filename
from struct import pack
from protocol_parser import ProtocolParser
import os
from yaml.scanner import ScannerError
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ast import If
import os
from pickletools import uint8
from unittest import case
from hydration import *
import json
from socket_creator import *
from structs import * 
from pydantic import BaseModel
from struct_handling import load_structs_from_path
from hydration_structs_parser import HydrationStructsParser

SCHEMAS_DIR_PATH = "schemas/"
FRONT_END_SCHEMA_FILE_NAME="send_packet_request_schema.json"
SUPPORTED_FILE_EXTENTIONS = [".json"]

PACKET_SCHEMA_PREFIX = "packet_schema_"
packet_schemas = {}

known_structs = {}
structs_initialized = False
socket_initialized = False

sock = None

def is_valid_file(parser, arg):
    filename, file_extension = os.path.splitext(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    if file_extension not in SUPPORTED_FILE_EXTENTIONS:
        print(file_extension)
        parser.error("The file %s is not in supported type" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

def generate_json_schemas_from_structs(structs_filename : str):
    global packet_schemas
    hydration_parser = HydrationStructsParser(structs_filename)
    packet_schemas = hydration_parser.run()

    print(packet_schemas)
    pass

current_directory = os.path.dirname(__file__)
frontend_directory = os.path.join(current_directory, 'static')

app = FastAPI()

app.mount("/app", StaticFiles(directory=frontend_directory, html = True), name="static")

@app.post("/connect/")
async def conenct(connection_type: str, ip: str, port : int):
    global sock
    global socket_initialized
    sock = create_socket(connection_type, ip, port)
    socket_initialized = True
    pass

@app.get("/structs/")
def get_structs():
    global packet_schemas
    return packet_schemas

@app.post("/packet/{packet_id}")
async def packet(packet_id: str, packet_request : str):
    global structs_initialized
    global socket_initialized
    global sock
    global packet_schemas

    if not structs_initialized:
        return "Send a struct firsrt :("

    if not socket_initialized:
        return "connect to a socket first :("

    if packet_id not in known_structs:
        return "Unknown struct id"

    packet_request_json = json.loads(packet_request)
    
    try:
        packet = known_structs[packet_id](**dict(packet_request_json))
        print(packet)
    except:
        return "Failed to create packet with given data"

    sock.send(bytes(packet))

    return "Packet sent successfully"

@app.post("/structs/")
def strucs(structs_path : str):
    global structs_initialized

    if not os.path.exists(structs_path):
        return "Path does not exist"

    known_structs.update(load_structs_from_path(structs_path))
    generate_json_schemas_from_structs(structs_path)
        
    structs_initialized = True
    return "successfully loaded structs"

def run():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")