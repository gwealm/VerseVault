"""Last.fm API wrapper."""

import requests

from config import RPS, LASTFM_API_KEY
from utils import throttle

@throttle(RPS)
def get_from_lastfm(method: str, **kwargs) -> dict | None:
    """Perform a request to the Last.fm API."""
    
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