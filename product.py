import json
from utils import format_size
import time

class Product:
    def __init__(self, name, url, image_url, info, properties, type, table):
        self.name = name
        self.url = url
        self.image_url = image_url
        if info:
            self.info, self.active = format_size(info, table)

        else:
            self.info = []
            self.active = False
        self.properties = properties
        self.type = type
        self.table = table

    def __str__(self):
        return f"Product(url={self.url}, image_url={self.image_url})"

    def to_dict(self):

        return {
            "name": self.name,
            "url": self.url,
            "image_url": self.image_url,
            "info": self.info,
            "properties": self.properties,
            "created": int(time.time()),
            "last_update": int(time.time()),
            "active": self.active,
            "type": self.type,
            "table": json.dumps(self.table)
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def save(self):
        if not self.active or self.info == [] or self.name is None:
            return False
        for item in self.info:
            if "formatted_size" not in item or not item["formatted_size"]:
                self.info, self.active = format_size(self.info, self.table)
                break

        filename = self.url.split('/')[-1] + ".json"
        with open("results/"+self.type+"/"+filename, "w+") as file:
            file.write(self.to_json())
        
        return True
