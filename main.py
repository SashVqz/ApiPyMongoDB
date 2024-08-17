import os
import json
from model import initApp
from queries import Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15

# Dictionary mapping model names to their respective JSON files
fileMap = {
    "person": "people.json",
    "company": "companies.json",
    "educationalInstitution": "institutions.json"
}

def getDataFilePath(file: str) -> str:
    """Constructs the full file path for a given file name located in the 'data' directory."""
    return os.path.join(os.path.dirname(__file__), 'data', file)

def loadJsonData(collectionName: str, file: str):
    filePath = getDataFilePath(file)
    print(filePath)

    if not os.path.exists(filePath):
        print(f"Error: File not found: {filePath}.")
        return
    
    with open(filePath, 'r') as file:
        data = json.load(file)
    
    modelClass = globals().get(collectionName)
    if modelClass:
        for entry in data:
            modelInstance = modelClass(**entry)
            modelInstance.save()
    else:
        print(f"Error: Model class not found for collection: {collectionName}.")

def insertData():
    for modelName, jsonFile in fileMap.items():
        loadJsonData(modelName, jsonFile)

def executeQuery(query, model):
    if model:
        results = model.aggregate(query)
        for result in results:
            print(result)
    else:
        print(f"Error: Model class not found for executing query.")

def main():
    initApp()
    insertData()
    
    print("Results for Q1:")
    executeQuery(Q1, globals().get("person"))

    print("Results for Q2:")
    executeQuery(Q2, globals().get("person"))

    print("Results for Q3:")
    executeQuery(Q3, globals().get("person"))

    print("Results for Q4:")
    executeQuery(Q4, globals().get("person"))

    print("Results for Q5:")
    executeQuery(Q5, globals().get("person"))

    print("Results for Q6:")
    executeQuery(Q6, globals().get("company"))

    print("Results for Q7:")
    executeQuery(Q7, globals().get("educationalInstitution"))

    print("Results for Q8:")
    executeQuery(Q8, globals().get("person"))

    print("Results for Q9:")
    executeQuery(Q9, globals().get("person"))

    print("Results for Q10:")
    executeQuery(Q10, globals().get("company"))

    print("Results for Q11:")
    executeQuery(Q11, globals().get("educationalInstitution"))

    print("Results for Q12:")
    executeQuery(Q12, globals().get("person"))

    print("Results for Q13:")
    executeQuery(Q13, globals().get("company"))

    print("Results for Q14:")
    executeQuery(Q14, globals().get("person"))

    print("Results for Q15:")
    executeQuery(Q15, globals().get("company"))

if __name__ == '__main__':
    main()
