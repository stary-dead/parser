import json
class Product:
    def __init__(self, name, url, image_url, info, properties):
        self.name = name
        self.url = url
        self.image_url = image_url
        self.info = info
        self.properties = properties
    def __str__(self):
        return f"Product(url={self.url}, image_url={self.image_url})"
    def to_dict(self):
        return {
            "name":self.name,
            "url": self.url,
            "image_url": self.image_url,
            "info": self.info,
            "properties": self.properties
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def save(self):
        filename = self.url.split('/')[-1] + ".json"
        with open("results/"+filename, "w") as file:
            file.write(self.to_json())
