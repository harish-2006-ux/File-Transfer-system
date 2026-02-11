import requests
import time

BASE_URL = "http://localhost:5000"

def test_login():
    # Test login page
    response = requests.get(f"{BASE_URL}/login")
    print(f"Login page status: {response.status_code}")
    assert response.status_code == 200

    # Test invalid login
    data = {"username": "test", "password": "wrong"}
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    print(f"Invalid login status: {response.status_code}")
    assert response.status_code == 200  # Renders login page again

    # Test signup
    response = requests.get(f"{BASE_URL}/signup")
    print(f"Signup page status: {response.status_code}")
    assert response.status_code == 200

    # Create a test user
    data = {"username": "testuser", "email": "test@example.com", "password": "testpass"}
    response = requests.post(f"{BASE_URL}/signup", data=data, allow_redirects=False)
    print(f"Signup status: {response.status_code}")
    assert response.status_code == 302

    # Login with test user
    data = {"username": "testuser", "password": "testpass"}
    session = requests.Session()
    response = session.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    print(f"Valid login status: {response.status_code}")
    assert response.status_code == 302

    return session

def test_home(session):
    response = session.get(f"{BASE_URL}/")
    print(f"Home page status: {response.status_code}")
    assert response.status_code == 200
    assert "Welcome testuser" in response.text
    assert "AI Chatbot" in response.text

def test_chatbot(session):
    data = {"message": "Hello"}
    response = session.post(f"{BASE_URL}/chat", json=data)
    print(f"Chatbot status: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    print(f"Chatbot response: {data['response']}")
    assert "response" in data

def test_dashboard(session):
    response = session.get(f"{BASE_URL}/dashboard")
    print(f"Dashboard status: {response.status_code}")
    assert response.status_code == 200

if __name__ == "__main__":
    try:
        session = test_login()
        test_home(session)
        test_chatbot(session)
        test_dashboard(session)
        print("All critical path tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
