#!/usr/bin/env python

from argparse import ArgumentParser
from ast import If
from nis import match
import os
from pickletools import uint8
from unittest import case
from hydration import *
import json
import jsonschema
import serial
import socket
from socket_creator import *
import config

SCHEMAS_DIR_PATH = "schemas/"
FRONT_END_SCHEMA_FILE_NAME="front_end_schema.json"
SUPPORTED_FILE_EXTENTIONS = [".json"]
front_end_schema = {}

class MockPacket(Struct):
    header = UInt8
    data = UInt16

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

def parse_args():
    parser = ArgumentParser(description="Packet Communicator")
    parser.add_argument("-packet=", dest="filename", required=True,
                        help="input file with struct to parse", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))

    return parser.parse_args()

def load_schemas():
    global front_end_schema
    with open(SCHEMAS_DIR_PATH + FRONT_END_SCHEMA_FILE_NAME, 'r') as file:
        front_end_schema = json.loads(file.read()) 


def main():
    load_schemas()
    
    # get schema from front end
    args = parse_args()
    front_end_params = args.filename.read()

    if not is_valid_json(front_end_params, front_end_schema):
        print("invalid json data")
        return 1
    
    json_data = json.loads(front_end_params)
    socket = None

    sock = create_socket(json_data["connection_type"], json_data["connection_info"])
    
    print(json_data)
    
    packet = MockPacket(**dict(json_data["packet_data"]))
    connection_data = (json_data["connection_info"]["ip"], int(json_data["connection_info"]["port"]))
    sock.sendto(bytes(packet), connection_data)

if __name__ == "__main__":
    main()
