import config as cfg
import sys
import hashlib
import pprint
import json
import re

def validate_email(address):
    hash_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not hash_regex.match(address):
        return False
    return True


def validate_hash(h):
    result = None
    #print("validate Hash: "+h)
    try: 
        #result = re.match(r'^0x[a-f0-9]{64}$', h).group(0)
        result = re.match(r'^[a-f0-9]{64}$', h).group(0)
    except: 
        pass
    return result is not None

def is_json(x):
    result = False
    #print("validate Json")
    try: 
        result = json.loads(x, strict=False) 
    except: 
        pass
    return result