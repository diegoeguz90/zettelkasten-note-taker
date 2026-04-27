import requests
import sys

BASE_URL = "http://localhost:8003/api"

def test_api():
    print("Starting API validation...")

    # 1. Health Check
    try:
        resp = requests.get("http://localhost:8003/health")
        resp.raise_for_status()
        print("✅ Health check passed")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)

    # 2. Settings / API Key
    try:
        resp = requests.get(f"{BASE_URL}/settings/api-key")
        resp.raise_for_status()
        api_key = resp.json().get("api_key")
        print(f"✅ Settings API retrieved (Key: {api_key[:8]}...)")
    except Exception as e:
        print(f"❌ Settings API failed: {e}")
        sys.exit(1)

    # 3. Create Note
    note_data = {
        "title": "Automated Test Note",
        "content": "This note was created by the validation script.",
        "connected_to_note_ids": []
    }
    try:
        resp = requests.post(f"{BASE_URL}/notes/", json=note_data)
        resp.raise_for_status()
        note_id = resp.json().get("id")
        print(f"✅ Note creation passed (ID: {note_id})")
    except Exception as e:
        print(f"❌ Note creation failed: {e}")
        sys.exit(1)

    # 4. Get Note Detail
    try:
        resp = requests.get(f"{BASE_URL}/notes/{note_id}")
        resp.raise_for_status()
        if resp.json().get("title") == note_data["title"]:
            print("✅ Note retrieval passed")
        else:
            print("❌ Note retrieval content mismatch")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Note retrieval failed: {e}")
        sys.exit(1)

    # 5. Graph Check
    try:
        resp = requests.get(f"{BASE_URL}/graph/")
        resp.raise_for_status()
        nodes = resp.json().get("nodes", [])
        if any(n["id"] == note_id for n in nodes):
            print(f"✅ Graph API passed (Found {len(nodes)} nodes)")
        else:
            print("❌ Graph API failed: Note not found in graph")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Graph API failed: {e}")
        sys.exit(1)

    print("\n🚀 All API validations passed successfully!")

if __name__ == "__main__":
    test_api()
