## Description
This project is a Python API designed to register specific models and store them in a MongoDB database. The core of the API is built around a generic `Model` class that allows dynamic and flexible creation and management of MongoDB documents.

- **Dynamic Model Definition:** Models are defined using a YAML file that specifies required and admissible variables.
- **Document Management:** Supports CRUD operations on MongoDB documents.
- **Geolocation:** Integration with the Nominatim API to obtain geographic coordinates from addresses and store them as GeoJSON `Point` objects.

## Project Structure 
- **`model.py`**: Contains the main implementation of the `Model` class and its associated methods.
- **`models.yml`**: YAML file that defines the models and their variables.
- **`queries.py`**: Scripts dedicated to practicing and executing queries on the models in MongoDB.
