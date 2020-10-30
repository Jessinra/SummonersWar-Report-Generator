import json

result = {}
with open("bestiary.json", ) as f:
    bestiary = json.load(f)
    for m in bestiary:

        id = m['com2us_id']
        if str(id)[3] == "0":  # unawakened
            id = int(str(id)[:3])

        result[id] = m['name']

with open("formatted_bestiary.json", "w") as f:
    json.dump(result, f)
