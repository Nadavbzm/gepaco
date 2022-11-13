from fileinput import filename
from struct import pack
from protocol_parser import ProtocolParser
import os
from yaml.scanner import ScannerError
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from pickletools import uint8
from hydration import *
import json
from socket_creator import *
from structs import * 
from struct_handling import load_structs_from_path
from hydration_structs_parser import HydrationStructsParser

packets_json = {}

known_structs = {}
structs_initialized = False
socket_initialized = False

sock = None

app = FastAPI()

current_directory = os.path.dirname(__file__)
frontend_directory = os.path.join(current_directory, 'static')

app.mount("/app", StaticFiles(directory=frontend_directory, html = True), name="static")

def generate_json_schemas_from_structs(structs_filename : str):
    global packets_json
    hydration_parser = HydrationStructsParser(structs_filename)
    packets_json = hydration_parser.run()


@app.post("/connect/")
async def conenct(connection_type: str, ip: str, port : int):
    global sock
    global socket_initialized
    sock, succuss = create_socket(connection_type, ip, port)
    if succuss:
        socket_initialized = True
        return "Successfully created connection"
    
    return "Failed to create socket with given parameters"

@app.get("/structs/")
def get_structs():
    global packets_json
    return packets_json

@app.post("/packet/{packet_id}")
async def packet(packet_id: str, packet_request : str):
    global structs_initialized
    global socket_initialized
    global sock
    global packets_json

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