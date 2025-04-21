import requests

BASE_URL = "http://localhost:8000"
ENDPOINTS = ["tracks", "users", "listen_history"]

def test_endpoints():
    for endpoint in ENDPOINTS:
        url = f"{BASE_URL}/{endpoint}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✅ {endpoint} returned 200 OK")
            else:
                print(f"❌ {endpoint} returned status {response.status_code}")
        except requests.RequestException as e:
            print(f"🔥 Error reaching {endpoint}: {e}")

if __name__ == "__main__":
    test_endpoints()