Q1 = [{"$match": {"university": {"$in": ["Harvard", "UAM"]}}}]

Q2 = [{"$match": {"address": "Madrid"}}, {"$group": {"_id": "$university"}}]

Q3 = [{"$match": {"description": {"$regex": "Artificial Intelligence", "$options": "i"}}}]

Q4 = [{"$match": {"graduationYear": {"$gte": 2017}}}]

Q5 = [
    {"$match": {"company": "Microsoft"}},
    {"$group": {"_id": None, "totalStudies": {"$sum": "$numStudents"}, "totalPeople": {"$sum": 1}}},
    {"$project": {"_id": 0, "avgNum": {"$divide": ["$totalStudies", "$totalPeople"]}}}
]

Q6 = [
    {"$match": {"company": "Google"}},
    {
        "$geoNear": {
            "near": {"type": "Point", "coordinates": [-3.686101, 40.420008]},
            "distanceField": "workDistance",
            "spherical": True
        }
    },
    {"$group": {"_id": None, "avgDistance": {"$avg": "$workDistance"}}}
]

Q7 = [
    {"$match": {"university": {"$exists": True}}},
    {"$group": {"_id": "$university", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 3}
]

Q8 = [
    {"$group": {"_id": "$university", "totalPeople": {"$sum": 1}}},
    {"$sort": {"totalPeople": -1}}
]

Q9 = [
    {"$match": {"age": {"$gte": 20, "$lte": 30}}},
    {"$project": {"name": 1, "age": 1, "university": 1}}
]

Q10 = [
    {"$match": {"numEmployees": {"$gt": 100}}},
    {"$project": {"name": 1, "numEmployees": 1}}
]

Q11 = [
    {"$match": {"numStudents": {"$gte": 500}}},
    {"$project": {"name": 1, "numStudents": 1}}
]

Q12 = [
    {"$match": {"graduationYear": 2020}},
    {"$project": {"name": 1, "graduationYear": 1, "university": 1}}
]

Q13 = [
    {"$group": {"_id": "$name", "averageStudies": {"$avg": "$numStudy"}}},
    {"$sort": {"averageStudies": -1}}
]

Q14 = [
    {"$match": {"description": {"$regex": "engineer", "$options": "i"}}},
    {"$project": {"name": 1, "description": 1, "university": 1}}
]

Q15 = [
    {"$group": {"_id": "$company", "totalPeople": {"$sum": 1}}},
    {"$sort": {"totalPeople": -1}}
]
