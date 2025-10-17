import streamlit as st
import pandas as pd
import numpy as np
import json
from lightfm import LightFM
from lightfm.data import Dataset

# ===============================
# 1. Load data & train model (cached)
# ===============================
@st.cache_resource
def train_model():
    clients = pd.read_csv("clients.csv")
    plans = pd.read_csv("plans.csv")
    subscriptions = pd.read_csv("subscriptions.csv")
    usage = pd.read_csv("usage.csv")

    # Aggregate usage by client
    usage_agg = usage.groupby("client_id").agg({
        "data_used_GB": "mean",
        "call_minutes": "mean",
        "sms_sent": "mean"
    }).reset_index()

    # Merge client features
    clients = clients.merge(usage_agg, on="client_id", how="left")
    clients.fillna(0, inplace=True)

    # Get last plan per client
    latest_sub = subscriptions.sort_values("end_date").groupby("client_id").tail(1)
    latest_sub = latest_sub[["client_id", "plan_id"]]

    # Build interactions
    interactions_df = latest_sub.merge(clients, on="client_id")
    interactions_df = interactions_df.merge(plans, on="plan_id")

    # Build dataset
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

    (interactions, _) = dataset.build_interactions([
        (str(row["client_id"]), str(row["plan_id"])) for _, row in interactions_df.iterrows()
    ])
    user_features = dataset.build_user_features([
        (str(row["client_id"]), [row["segment"]]) for _, row in clients.iterrows()
    ])
    item_features = dataset.build_item_features([
        (str(row["plan_id"]), [row["plan_type"]]) for _, row in plans.iterrows()
    ])

    # Train model
    model = LightFM(loss="warp")
    model.fit(interactions, user_features=user_features,
              item_features=item_features, epochs=10, num_threads=4)

    return model, dataset, clients, plans, user_features, item_features

model, dataset, clients, plans, user_features, item_features = train_model()

# Reverse plan mapping
reverse_item_map = {v: k for k, v in dataset.mapping()[2].items()}
plan_map = {str(row["plan_id"]): row.to_dict() for _, row in plans.iterrows()}
n_items = len(plan_map)

# ===============================
# 2. Streamlit UI
# ===============================
st.title("📱 LightFM Telco Recommender")

st.sidebar.header("Options")
mode = st.sidebar.radio("Choose mode:", ["Existing Client", "New Client (Cold Start)"])

# ---- Existing Client
if mode == "Existing Client":
    client_id = st.selectbox("Select Client ID:", options=clients["client_id"].astype(str).tolist())
    if st.button("Recommend"):
        uid = dataset.mapping()[0][str(client_id)]
        scores = model.predict(uid, np.arange(n_items), user_features=user_features, item_features=item_features)
        top_items = np.argsort(-scores)[:3]

        st.subheader("Top 3 Recommended Plans")
        for idx in top_items:
            plan_id = reverse_item_map[idx]
            st.json(plan_map[plan_id])

# ---- Cold Start
elif mode == "New Client (Cold Start)":
    uploaded_file = st.file_uploader("Upload new_clients.json", type="json")

    if uploaded_file is not None:
        new_clients = pd.DataFrame(json.load(uploaded_file))
        if 'segment' not in new_clients.columns:
            new_clients['segment'] = 'default'

        new_user_features = dataset.build_user_features([
            (str(row["client_id"]), [row["segment"]]) for _, row in new_clients.iterrows()
        ])

        st.subheader("Cold Start Recommendations")
        for _, row in new_clients.iterrows():
            user_id = str(row["client_id"])
            uid = dataset.mapping()[0].get(user_id, len(dataset.mapping()[0]))
            scores = model.predict(uid, np.arange(n_items),
                                   user_features=new_user_features,
                                   item_features=item_features)
            top_items = np.argsort(-scores)[:3]

            st.markdown(f"### New Client {user_id}")
            for idx in top_items:
                plan_id = reverse_item_map[idx]
                st.json(plan_map[plan_id])
