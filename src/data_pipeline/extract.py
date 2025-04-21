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

def fetch_all_data():
    """
    Fetch data from all endpoints and return a dict of raw responses.
    """
    return {
        "tracks": requests.get(f"{BASE_URL}/tracks").json(),
        "users": requests.get(f"{BASE_URL}/users").json(),
        "listen_history": requests.get(f"{BASE_URL}/listen_history").json()
    }

if __name__ == "__main__":
    test_endpoints()