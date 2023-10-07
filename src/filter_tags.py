
from multiprocessing import RLock
import time
import requests
import dotenv
import os
import sys
import csv
from concurrent.futures import ThreadPoolExecutor

dotenv.load_dotenv()

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

RPS = 20

reader = csv.reader(open("./data-limwa/track_lyrics.csv", 'r'))
writer = csv.writer(open("./data-limwa/track_tags.csv", 'w'), quoting=csv.QUOTE_NONNUMERIC)


class LockableSet:
    def __init__(self, set):
        self.set = set
        self.lock = RLock()
        
    def __enter__(self):
        while not self.lock.acquire():
            pass
        
        return self.set

    def __exit__(self, exc_type, exc_value, traceback):
        #Do what you want with the error
        self.lock.release()

valid_genres = LockableSet(set())
invalid_genres = LockableSet(set())


last_request = 0

def get_from_lastfm(method: str, **kwargs) -> dict | None:
    global last_request

    while True:
        now = time.time()
        if now - last_request > 1 / RPS:
            break
        
        time.sleep(1 / RPS - (now - last_request))
        
    last_request = time.time()
    
    kwargs['api_key'] = LASTFM_API_KEY
    kwargs['format'] = 'json'
    kwargs['method'] = method
    
    while True:
        try:
            response = requests.get(f'https://ws.audioscrobbler.com/2.0/', params=kwargs)
            
            if not response.ok:
                print(f"Request not ok with status code {response.status_code} on URL \"{response.url}\"\n{response.text}\n", file=sys.stderr)
                return None
    
            return response.json()

        except InterruptedError:
            sys.exit(1)
        except Exception as e:
            print(f"Request caused exception {e} on params \"{kwargs}\"\n", file=sys.stderr)
            time.sleep(5)
            
def is_tag_genre(tag: str) -> bool:
    
    res = get_from_lastfm('tag.getinfo', tag=tag)
    if res is None:
        return False
    
    if 'tag' not in res or 'wiki' not in res['tag'] or 'summary' not in res['tag']['wiki']:
        return False
    
    summary = res['tag']['wiki']['summary']
    if 'genre' in summary.lower():
        return True
    
    return False
    
def process_row(index, row):
    print(f"Iteration {index}")
    tags = list(map(str.lower, row[7].split("%SEP%")))

    valid_tags = []
    
    for tag in tags:
        with valid_genres as v:
            if tag in v:
                valid_tags.append(tag)
                continue
        
        with invalid_genres as i:
            if tag in i:
                continue
        
        if is_tag_genre(tag):
            with valid_genres as v:
                v.add(tag)
                valid_tags.append(tag)
        else:
            with invalid_genres as i:
                i.add(tag)
            
    modified_row = [*row, "%SEP%".join(valid_tags)]
    
    return modified_row
        
def main():
    
    # Define the maximum number of threads (you can adjust this)
    MAX_THREADS = 32
    
    # Create a ThreadPoolExecutor with the specified number of threads
    with ThreadPoolExecutor(MAX_THREADS) as executor:
        
        # Iterate through each row in the DataFrame and submit tasks
        futures = [executor.submit(process_row, index, row) for index, row in enumerate(reader)]
        
        # Wait for all tasks to complete
        for future in futures:
            modified_row = future.result()
            writer.writerow(modified_row)     
        
    print("Done, writing tags")
    
    with open("valid_tags.txt", "w") as f:
        with valid_genres as v:
            f.write("\n".join(v))
        
    with open("invalid_tags.txt", "w") as f:
        with invalid_genres as i:
            f.write("\n".join(i))
        
    print("Done")   
    
if __name__ == '__main__':
    main()