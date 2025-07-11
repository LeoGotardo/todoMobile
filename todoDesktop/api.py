import requests

BASE_URL = "http://localhost:3000"  # Troque se necessário


def login_api(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def get_todos_api(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/todos", headers=headers)
    if response.status_code == 200:
        return response.json()  # espera-se uma lista
    return []


def add_todo_api(token, description):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/todos", headers=headers, json={"description": description})
    return response.status_code == 201


def delete_todo_api(token, todo_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}", headers=headers)
    return response.status_code == 204


def complete_todo_api(token, todo_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(f"{BASE_URL}/todos/{todo_id}/complete", headers=headers)
    return response.status_code == 200
