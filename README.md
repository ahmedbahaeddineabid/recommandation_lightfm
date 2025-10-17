# 📦 LightFM Recommendation System for Telecom Operators

This project implements a **hybrid recommendation system** using [LightFM](https://making.lyst.com/lightfm/docs/home.html), designed for **telecom operators** to automatically suggest the most suitable mobile plans to clients — based on their usage patterns and similarities with other users.

---

## 🚀 Features

* ✅ Hybrid recommendation system (collaborative + content-based)
* 📊 Personalized plan suggestions for each client
* 🧠 Handles **cold-start** for new clients via JSON input
* 💿 Fully **Dockerized setup** — no local Python install needed
* 🧩 Outputs both CSV and JSON recommendation files

---

## 🧮 Project Structure

```
📁 recommandation_lightfm/
 ┣ 📜 Dockerfile
 ┣ 📜 requirements.txt
 ┣ 📜 lightfm_reco.py
 ┣ 📜 clients.csv
 ┣ 📜 plans.csv
 ┣ 📜 subscriptions.csv
 ┣ 📜 usage.csv
 ┣ 📜 new_clients.json
 ┗ 📜 README.md
```

---

## ⚙️ How to Run This Project (with Docker)

### 1️⃣ Clone or Download the Repository

```bash
git clone https://github.com/ahmedbahaeddineabid/recommandation_lightfm.git
cd recommandation_lightfm
```

—or download the ZIP and open a terminal (PowerShell, CMD, or VS Code) inside the project folder.

---

### 2️⃣ Build the Docker Image

```bash
docker build -t recommandation_lightfm .
```

---

### 3️⃣ Run the Container

```bash
docker run --rm -v ${PWD}:/app recommandation_lightfm
```

💡 This mounts your current folder into the container, so the generated result files will appear locally in the same directory.

---

## 🗂️ Output Files

After running, two new files will be generated automatically:

* `recommendations.csv` → top plan recommendations for **existing clients**
* `cold_start_recommendations.json` → top plan recommendations for **new clients** (from `new_clients.json`)

---

## 📊 Dataset Overview

| File                  | Description                                              |
| --------------------- | -------------------------------------------------------- |
| **clients.csv**       | Basic client data including segments and demographics    |
| **plans.csv**         | Available mobile plans (IDs, names, prices, types, etc.) |
| **subscriptions.csv** | Client subscriptions linking clients to plans            |
| **usage.csv**         | Aggregated client usage data (data, calls, SMS)          |
| **new_clients.json**  | Input file for cold-start predictions                    |

---

## 🧩 Requirements

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
* No need for local Python or libraries — **everything runs inside Docker**

---

## 👨‍💻 Author

**Ahmed Baha Eddine Abid**
📧 [ahmed.baha.eddine.abid@gmail.com](mailto:ahmed.baha.eddine.abid@gmail.com)
🧠 Data Science & BI | Machine Learning | Telecom Analytics
