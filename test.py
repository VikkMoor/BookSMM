import requests

print("Python requests → pu.vk.com")

try:
    response = requests.get(
        "https://pu.vk.com",
        timeout=10
    )

    print("STATUS:", response.status_code)
    print("SERVER:", response.headers.get("Server"))

except Exception as e:
    print("ОШИБКА:", type(e).__name__)
    print(e)