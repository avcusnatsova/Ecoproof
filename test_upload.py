import requests

url = "http://127.0.0.1:5000/admin/upload"

files = {
    "file": open("data/sensor_data.csv", "rb")
}

response = requests.post(url, files=files)

print(response.json())