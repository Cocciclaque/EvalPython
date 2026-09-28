import json

def show_dashboard(path:str):
    print("--     Dashboard     --")
    categories = {"suggestion": 0, "bug": 0, "payment": 0, "account": 0, "toxicity": 0, "autre": 0}
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for line in data:
            categories[line["analyse"]["category"]]+=1
        categories = dict(sorted(categories.items(), key=lambda item: item[1]))
        for category in categories.keys() :
            print("Il y a " + str(categories[category]) + " " + category)
        print()
        total = 0
        for line in data:
            total += line["analyse"]["severity"]
        total = total/len(data)
        print("L'urgence moyenne est de " + str(total))
        print()

        severities = []
        for line in data:
            severities.append(line)
        severities = sorted(severities, key = lambda x:x["analyse"]["severity"], reverse=True)

        print("Les 3 tickets les plus urgents sont les tickets " + str(severities[0]["ticket"]["id"]) + ", " + str(severities[1]["ticket"]["id"]) + " et " + str(severities[2]["ticket"]["id"]))
        
show_dashboard("outputs/results.json")