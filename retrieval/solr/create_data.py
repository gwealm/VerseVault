import json
import sys
import datetime

def main():
    month_dict = { "Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", 
                  "Jul" : "07", "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12" }
    
    def convert_to_utc(date: str) -> str:
        day_month_year, hour_min = date.split(",")[0], date.split(",")[1]
        day, month, year = int(day_month_year.split(" ")[0]), int(month_dict[day_month_year.split(" ")[1]]), int(day_month_year.split(" ")[2])
        hour, min = int(hour_min.split(":")[0]), int(hour_min.split(":")[1])

        # x = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=min, tzinfo=datetime.timezone.utc)
        x = "{year}-{month}-{day}T{hour}:{min}:{sec}Z".format(year=year, month=month, day=day, hour=hour, min=min, sec="00")
        
        return x

    # convert_to_utc("14 Nov 2023, 20:12")
    
    id = 0
    
    objects = []
    while True:
        line = sys.stdin.readline()
        if line == "":
            break
        
        obj = json.loads(line)
        obj["type"] = "track"
        
        obj["id"] = str(id)
        id += 1

        obj["publishedAt"] = convert_to_utc(obj.get("publishedAt"))
        
        for child in obj["lyrics"]:
            child["type"] = "lyric_section"
            
            if "title" in child:
                child["title_s"] = child["title"]
                del child["title"]
                
            if "content" in child:
                child["content_t"] = child["content"]
                del child["content"]
            
            child["id"] = str(id)
            id += 1
            
            
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