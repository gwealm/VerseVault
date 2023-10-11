"""Utility functions for the crawler."""

from os.path import join
from time import sleep, time

from config import DATA_DIR

def normalize_xml_value(value) -> list:
    """Normalize XML value to list."""
    
    if isinstance(value, list):
        return value
    
    if isinstance(value, dict):
        return [value]
    
    raise TypeError(f"Unknown type {type(value)} for XML normalization of {value}")

def get_data_path(*path) -> str:
    """Get a filesystem path relative to the data directory."""
    return join(DATA_DIR, *path)

def throttle(rps: int):
    """Roughly throttle function to only run the given ammount of runs per second."""
    
    def decorator(func):
        
        last_call_time = 0
        
        def wrapper(*args, **kwargs):
            
            nonlocal last_call_time
            
            now = time()
            
            sleep_time = 1 / rps - (now - last_call_time)
            last_call_time = now
            
            if sleep_time > 0:
                sleep(sleep_time)
                
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator