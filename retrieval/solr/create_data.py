import json
import sys
import datetime
from dateutil.parser import parse
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

def convert_to_utc(date: str) -> str:
    dt = parse(date, fuzzy=True)

    dt = dt.astimezone(datetime.timezone.utc).isoformat()
    dt = dt[:-6]
    
    return dt + "Z"

def main():
    curr_id = 0

    objects = []
    while True:
        line = sys.stdin.readline()
        if line == "":
            break
        
        obj = json.loads(line)
        obj["doc_type"] = "track"
        
        obj["id"] = str(curr_id)
        curr_id += 1

        combined_text = ""

        if "publishedAt" in obj:
            obj["publishedAt"] = convert_to_utc(obj["publishedAt"])
        
        for child in obj["lyrics"]:
            child["doc_type"] = "lyric_section"
            
            # if "title" in child:
            #     child["title"] = child["title"]
                # del child["title"]
                
            if "content" in child:
                # child["content"] = child["content"]
                combined_text += child["content"]
                # del child["content"]
            
            child["id"] = str(curr_id)
            curr_id += 1
            
        obj["entities.text"] = list(map(lambda x: x["text"], obj["entities"]))
        obj["entities.start"] = list(map(lambda x: x["start"], obj["entities"]))
        obj["entities.end"] = list(map(lambda x: x["end"], obj["entities"]))
        obj["entities.type"] = list(map(lambda x: x["type"], obj["entities"]))
        
        del obj["entities"]
        
        obj["album.image"] = obj.get("album", {}).get("image", None)
        if not obj["album.image"]:
            del obj["album.image"]
            
        obj["album.name"] = obj.get("album", {}).get("name", None)
        if not obj["album.name"]:
            del obj["album.name"]
            
        if "album" in obj:
            del obj["album"]
        
        # obj["_childDocuments_"] = obj["lyrics"].copy()
        # del obj["lyrics"]
        del obj["__order"]

        # semantic search
        obj["content_vector"] = get_embedding(combined_text)
        
        objects.append(obj)
        
    print(json.dumps(objects, indent=4))
        
    # def wrap_obj(obj):
    #     return f'''"add": {{
    #         "doc": {json.dumps(obj)} 
    #     }}'''
        
    # objects = map(wrap_obj, objects[:20])
    # json_final = ",\n".join(objects)
    
    # json_final_final = f'''{{
    #     {json_final},
    #     "commit": {{}}
    # }}'''
    
    # print(json_final_final)
        
if __name__ == '__main__':
    main()
    # pass