import pymongo
import yaml
import os
import time
from typing import Generator, Any, Self
from geojson import Point
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def getLocationPoint(address: str) -> Point:
    geolocator = Nominatim(user_agent=f"geoapiExercises_{time.time()}")
    location = None

    while location is None:
        try:
            time.sleep(1)
            location = geolocator.geocode(address)
        except GeocoderTimedOut:
            print(f"Error: geocode failed for address {address}. Retrying...")
            continue

    return Point((location.longitude, location.latitude)) if location else None

class Model:
    requiredVars: set[str]
    admissibleVars: set[str]
    db: pymongo.collection.Collection

    def __init__(self, **kwargs: dict[str, str or dict]):
        missingVars = self.requiredVars - kwargs.keys()
        if missingVars:
            raise ValueError(f"Missing required variables: {missingVars}")

        extraVars = kwargs.keys() - (self.requiredVars | self.admissibleVars)
        if extraVars:
            raise ValueError(f"Unallowed variables: {extraVars}")

        self.__dict__.update(kwargs)

    def __setattr__(self, name: str, value: str or dict) -> None:
        if name not in self.requiredVars and name not in self.admissibleVars:
            raise ValueError(f'Variable "{name}" is neither required nor allowed')
        super().__setattr__(name, value)

    def save(self) -> None:
        if 'address' in self.__dict__:
            point = getLocationPoint(self.__dict__['address'])
            if point:
                self.__dict__['location'] = {
                    'type': 'Point',
                    'coordinates': list(point['coordinates'])
                }

        if '_id' in self.__dict__:
            docUpdated = {
                key: value for key, value in self.__dict__.items()
                if value != self.db.find_one({"_id": self._id}).get(key)
            }

            self.db.update_one({"_id": self._id}, {"$set": docUpdated})
        else:
            self._id = self.db.insert_one(self.__dict__).inserted_id

    def delete(self) -> None:
        if '_id' in self.__dict__:
            self.db.delete_one({"_id": self._id})
        else:
            raise ValueError("Cannot delete a document without '_id'.")

    @classmethod
    def find(cls, filter: dict[str, str or dict]) -> Any:
        return ModelCursor(cls, cls.db.find(filter))

    @classmethod
    def aggregate(cls, pipeline: list[dict]) -> pymongo.command_cursor.CommandCursor:
        return cls.db.aggregate(pipeline)

    @classmethod
    def findById(cls, id: str) -> Self | None:
        return cls(**cls.db.find_one({"_id": id}))

    @classmethod
    def initClass(cls, dbCollection: pymongo.collection.Collection, requiredVars: set[str], admissibleVars: set[str]) -> None:
        cls.db = dbCollection
        cls.requiredVars = requiredVars
        cls.admissibleVars = admissibleVars

class ModelCursor:
    def __init__(self, modelClass: Model, cursor: pymongo.cursor.Cursor):
        self.model = modelClass
        self.cursor = cursor

    def __iter__(self) -> Generator:
        while self.cursor.alive:
            yield self.model(**next(self.cursor))

# mongoUri no definite --> https://www.mongodb.com
def initApp(definitionsPath: str = os.path.join(os.path.dirname(__file__), 'models.yml'), mongodbUri="...", dbName="mongoDBByPython") -> None:
    client = pymongo.MongoClient(mongodbUri)
    db = client[dbName]

    with open(definitionsPath, 'r') as yml:
        definitionsYaml = yaml.safe_load(yml)

    # Initialize the models
    for name, arg in definitionsYaml.items():
        model = type(name.capitalize(), (Model,), {})
        model.initClass(
            dbCollection=db[name],
            requiredVars=set(arg.get("requiredVars", [])),
            admissibleVars=set(arg.get("admissibleVars", []))
        )
        globals()[name] = model
    
    print("App initialized.")
