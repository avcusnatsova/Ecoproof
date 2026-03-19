from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

# Import your modules
from anomaly_model import detect_anomalies
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)

# Initialize blockchain
bc = Blockchain()

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure data folder exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DATA_FILE = os.path.join(DATA_DIR, "sensor_data.csv")


# -------------------------------
# HOME ROUTE
# -------------------------------
@app.route('/')
def home():
    return "EcoProof Backend Running 🚀"


# -------------------------------
# PUBLIC API (GET plant data)
# -------------------------------
@app.route('/public/<plant_id>', methods=['GET'])
def get_plant_data(plant_id):
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "No data available. Upload CSV first."})

    df = pd.read_csv(DATA_FILE)

    # ✅ Fix types
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['timestamp'] = df['timestamp'].astype(str)  # 🔥 FIX NaT issue
    df['plant_id'] = df['plant_id'].astype(str)
    df['plant_name'] = df['plant_name'].astype(str)

    # Apply anomaly detection
    df = detect_anomalies(df)

    # Filter plant
    plant_data = df[
        (df['plant_id'].str.lower() == plant_id.lower()) |
        (df['plant_name'].str.lower() == plant_id.lower())
    ]

    if plant_data.empty:
        return jsonify({"error": "Plant not found"})

    # ✅ PERFORMANCE FIX (handle 3000 rows)
    limit = int(request.args.get("limit", 100))

    plant_data = plant_data.sort_values(by="timestamp", ascending=False)

    latest = plant_data.iloc[0]
    history = plant_data.head(limit)
    anomalies = plant_data[plant_data["anomaly_flag"]].head(limit)

    return jsonify({
        "latest": latest.to_dict(),
        "history": history.to_dict(orient="records"),
        "anomalies": anomalies.to_dict(orient="records")
    })


# -------------------------------
# ADMIN API (UPLOAD CSV)
# -------------------------------
@app.route('/admin/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file uploaded"})

    try:
        df = pd.read_csv(file)

        # ✅ Fix types
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df['timestamp'] = df['timestamp'].astype(str)  # 🔥 FIX NaT
        df['plant_id'] = df['plant_id'].astype(str)
        df['plant_name'] = df['plant_name'].astype(str)

        # Apply anomaly detection
        df = detect_anomalies(df)

        # ✅ SAVE DATA
        df.to_csv(DATA_FILE, index=False)

        new_blocks = 0

        # ✅ PERFORMANCE FIX (limit blockchain load)
        for _, row in df.head(500).iterrows():
            row_dict = row.to_dict()

            # 🔥 FIX NaT JSON issue
            for key, value in row_dict.items():
                if pd.isna(value):
                    row_dict[key] = None

            if not bc.is_row_logged(row_dict):
                bc.add_block(row_dict)
                new_blocks += 1

        return jsonify({
            "message": "File processed and saved successfully",
            "rows": len(df),
            "blocks_added": new_blocks
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------------------
# EXTRA API (Get all plants)
# -------------------------------
@app.route('/plants', methods=['GET'])
def get_all_plants():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "No data available"})

    df = pd.read_csv(DATA_FILE)

    plants = df[['plant_id', 'plant_name']].drop_duplicates()

    return jsonify(plants.to_dict(orient="records"))


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)