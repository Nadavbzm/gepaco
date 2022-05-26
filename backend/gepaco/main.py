import argparse
from fileinput import filename
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
import jsonschema
import string
import socket
from socket_creator import *
import config
from structs import * 
from pydantic import BaseModel
from struct_handling import load_structs_from_path
from hydration_structs_parser import HydrationStructsParser

SCHEMAS_DIR_PATH = "schemas/"
FRONT_END_SCHEMA_FILE_NAME="send_packet_request_schema.json"
SUPPORTED_FILE_EXTENTIONS = [".json"]

PACKET_SCHEMA_PREFIX = "packet_schema_"

known_structs = {}
structs_initialized = False
socket_initialized = False

sock = None

def is_valid_json(json_data, json_schema):
    try:
        jsonschema.validate(instance=json.loads(json_data), schema=json_schema)
    except ValueError as err:
        return False
    return True

def is_valid_file(parser, arg):
    filename, file_extension = os.path.splitext(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    if file_extension not in SUPPORTED_FILE_EXTENTIONS:
        print(file_extension)
        parser.error("The file %s is not in supported type" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

def load_schema(packet_id):
    with open(PACKET_SCHEMA_PREFIX + str(packet_id), 'r') as file:
        return json.loads(file.read()) 

def generate_json_schemas_from_structs(structs):
    hydration_parser = HydrationStructsParser()
    pass

current_directory = os.path.dirname(__file__)
frontend_directory = os.path.join(current_directory, 'static')

app = FastAPI()

app.mount("/app", StaticFiles(directory=frontend_directory, html = True), name="static")

@app.post("/connect/")
async def conenct(connection_info: str):
    global sock
    sock = create_socket(packet_request_json["connection_type"], packet_request_json["connection_info"])
    socket_initialized = True
    pass

@app.post("/packet/{packet_id}")
async def packet(packet_id: str, packet_request : str):
    global structs_initialized
    global socket_initialized

    if not structs_initialized:
        return "Send a struct firsrt :("

    if not socket_initialized:
        return "connect to a socket first :("

    packet_schema = load_schema(packet_id)
    if not is_valid_json(packet_request, packet_schema):
        return "Validation of request failed"

    print(packet_request)

    if packet_id not in known_structs:
        return "Unknown struct id"
    
    packet_request_json = json.loads(packet_request)
        
    packet = known_structs[packet_id](**dict(packet_request_json["packet_data"]))
    connection_data = (packet_request_json["connection_info"]["ip"], int(packet_request_json["connection_info"]["port"]))
    sock.sendto(bytes(packet), connection_data)

    return "Packet sent successfully"

@app.post("/structs/")
def strucs(structs_path : str):
    global structs_initialized

    if not os.path.exists(structs_path):
        return "Path does not exist"

    known_structs.update(load_structs_from_path(structs_path))
    with open(structs_path, "r") as struct_file_handler:
        struct_file_data = struct_file_handler.read()
        json_schemas = generate_json_schemas_from_structs(struct_file_data)
        for id, schema in enumerate(json_schemas):
            with open(PACKET_SCHEMA_PREFIX + str(id), 'w') as packet_file:
                packet_file.write(schema)
        
    structs_initialized = True
    return "successfully loaded structs"

def run():
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")