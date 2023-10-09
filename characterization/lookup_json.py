#!/usr/bin/env python3

import sys
import json

def dump(obj, property_path, if_undefined=None):
    if len(property_path) == 0:
        print(obj)
        return
        
    first_property, *rest_property = property_path
     
    if isinstance(obj, dict):
        if first_property not in obj:
            if if_undefined is not None:
                print(if_undefined)
                
            return
        
        dump(obj[first_property], rest_property, if_undefined)
        return
    
    if isinstance(obj, list):
        
        if first_property == "*":
            for elem in obj:
                dump(elem, rest_property, if_undefined)
                
            return

        if first_property.isnumeric():
            index = int(first_property)
            
            if index < len(obj):            
                dump(obj[index], rest_property, if_undefined)
                return
            
        if if_undefined is not None:
            print(if_undefined)
            return
    
    raise ValueError(f"Invalid property path: {str(property_path)} on {obj}")
            
                

def main():
    args = sys.argv[1:]

    if len(args) not in range(2, 4):
        print("Usage: lookup_json <input> <property> [if not exists]")
        return
    
    input_file = args[0]
    input_fd = sys.stdin if input_file == "-" else open(input_file, "r", encoding="utf8")
    
    property_path = args[1].split(".")
    if_not_exists = None if len(args) <= 2 else args[2]
    
    while True:
        line = input_fd.readline()
        if line == "":
            break
        
        obj = json.loads(line)
        dump(obj, property_path, if_not_exists)
        
        
    input_fd.close()
        
if __name__ == "__main__":
    main()