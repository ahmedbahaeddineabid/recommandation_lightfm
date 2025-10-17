import json

# Liste des nouveaux clients
new_clients = [
    {
        "client_id": 1,
        "age": 56,
        "gender": "Male",
        "region": "Tunis",
        "income_level": "High",
        "segment": "Professional",
        "device_type": "iOS",
        "tech_usage": "4G"
    },
    {
        "client_id": 2,
        "age": 69,
        "gender": "Female",
        "region": "Gabes",
        "income_level": "Medium",
        "segment": "Retired",
        "device_type": "iOS",
        "tech_usage": "4G"
    },
    {
        "client_id": 3,
        "age": 46,
        "gender": "Female",
        "region": "Kairouan",
        "income_level": "Medium",
        "segment": "Student",
        "device_type": "iOS",
        "tech_usage": "4G"
    },
    {
        "client_id": 4,
        "age": 32,
        "gender": "Female",
        "region": "Monastir",
        "income_level": "Low",
        "segment": "Unemployed",
        "device_type": "iOS",
        "tech_usage": "3G"
    },
    {
        "client_id": 5,
        "age": 60,
        "gender": "Male",
        "region": "Gabes",
        "income_level": "Medium",
        "segment": "Professional",
        "device_type": "Android",
        "tech_usage": "4G"
    },
    {
        "client_id": 6,
        "age": 25,
        "gender": "Female",
        "region": "Bizerte",
        "income_level": "Medium",
        "segment": "Student",
        "device_type": "iOS",
        "tech_usage": "4G"
    },
    {
        "client_id": 7,
        "age": 38,
        "gender": "Female",
        "region": "Sousse",
        "income_level": "Medium",
        "segment": "Student",
        "device_type": "iOS",
        "tech_usage": "4G"
    },
    {
        "client_id": 8,
        "age": 56,
        "gender": "Female",
        "region": "Bizerte",
        "income_level": "Medium",
        "segment": "Retired",
        "device_type": "Android",
        "tech_usage": "4G"
    }
]

# Sauvegarder dans un fichier JSON
with open("new_clients.json", "w") as f:
    json.dump(new_clients, f, indent=4)

print("Fichier new_clients.json créé avec succès !")
