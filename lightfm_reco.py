import pandas as pd
import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
import json

clients = pd.read_csv("clients.csv")
plans = pd.read_csv("plans.csv")
subscriptions = pd.read_csv("subscriptions.csv")
usage = pd.read_csv("usage.csv")

# ===============================
# 2. Preprocessing
# ===============================
# Aggregate usage by client
usage_agg = usage.groupby("client_id").agg({
    "data_used_GB": "mean",
    "call_minutes": "mean",
    "sms_sent": "mean"
}).reset_index()

# Merge client features
clients = clients.merge(usage_agg, on="client_id", how="left")
clients.fillna(0, inplace=True)

# Get last plan per client from subscriptions
latest_sub = subscriptions.sort_values("end_date").groupby("client_id").tail(1)
latest_sub = latest_sub[["client_id", "plan_id"]]

# Build interaction dataframe
interactions_df = latest_sub.merge(clients, on="client_id")
interactions_df = interactions_df.merge(plans, on="plan_id")

# ===============================
# 3. Build LightFM Dataset
# ===============================
dataset = Dataset()
dataset.fit(
    (str(x) for x in interactions_df["client_id"]),
    (str(x) for x in interactions_df["plan_id"])
)

dataset.fit_partial(
    users=(str(x) for x in interactions_df["client_id"]),
    user_features=(str(x) for x in clients["segment"].unique())
)

dataset.fit_partial(
    items=(str(x) for x in interactions_df["plan_id"]),
    item_features=(str(x) for x in plans["plan_type"].unique())
)

(interactions, weights) = dataset.build_interactions([
    (str(row["client_id"]), str(row["plan_id"])) for _, row in interactions_df.iterrows()
])

user_features = dataset.build_user_features([
    (str(row["client_id"]), [row["segment"]]) for _, row in clients.iterrows()
])

item_features = dataset.build_item_features([
    (str(row["plan_id"]), [row["plan_type"]]) for _, row in plans.iterrows()
])

# ===============================
# 4. Train LightFM Model
# ===============================
model = LightFM(loss="warp")
model.fit(interactions, user_features=user_features, item_features=item_features, epochs=10, num_threads=4)

# ===============================
# 5. Recommend Top 3 Plans for Existing Clients
# ===============================
n_users, n_items = interactions.shape
client_ids = list(dataset.mapping()[0].keys())
plan_ids = list(dataset.mapping()[2].keys())

results = []
for user_id in client_ids:
    uid = dataset.mapping()[0][user_id]
    scores = model.predict(uid, np.arange(n_items), user_features=user_features, item_features=item_features)
    top_items = np.argsort(-scores)[:3]
    for rank, iid in enumerate(top_items, 1):
        plan_str = [k for k, v in dataset.mapping()[2].items() if v == iid][0]
        results.append((user_id, plan_str, rank))

# Save recommendations for existing clients as CSV
pd.DataFrame(results, columns=["client_id", "plan_id", "recommendation_rank"]).to_csv("recommendations.csv", index=False)
print("Recommendations saved to recommendations.csv")



# ===============================
# Cold Start : nouveaux clients (JSON)
# ===============================

import json
import pandas as pd
import numpy as np

# Charger les nouveaux clients
with open("new_clients.json") as f:
    new_clients = pd.DataFrame(json.load(f))

# S'assurer que 'segment' existe
if 'segment' not in new_clients.columns:
    new_clients['segment'] = 'default'

# Construire les features des nouveaux clients
new_user_features = dataset.build_user_features([
    (str(row["client_id"]), [row["segment"]]) for _, row in new_clients.iterrows()
])

n_items = len(plan_ids)

# Préparer un mapping plan_id string -> détails complets
plan_map = {str(row["plan_id"]): row.to_dict() for _, row in plans.iterrows()}

# Inverse mapping LightFM item index -> plan_id string
reverse_item_map = {v: k for k, v in dataset.mapping()[2].items()}

cold_start_recommendations = {}

for _, row in new_clients.iterrows():
    user_id = str(row["client_id"])
    uid = dataset.mapping()[0].get(user_id, len(dataset.mapping()[0]))  # UID temporaire si non vu

    # Prédire les scores pour tous les plans
    scores = model.predict(uid, np.arange(n_items),
                           user_features=new_user_features,
                           item_features=item_features)

    top_items = np.argsort(-scores)[:3]  # Top 3

    recommended_plans = []
    for item_idx in top_items:
        plan_str_id = reverse_item_map[item_idx]
        if plan_str_id in plan_map:
            recommended_plans.append(plan_map[plan_str_id])
        else:
            print(f"[WARN] Plan ID {plan_str_id} non trouvé dans plans.csv")

    cold_start_recommendations[user_id] = recommended_plans

# Sauvegarder en JSON avec tous les détails
with open("cold_start_recommendations.json", "w") as f:
    json.dump(cold_start_recommendations, f, indent=4)

print("Cold start recommendations saved to cold_start_recommendations.json")


