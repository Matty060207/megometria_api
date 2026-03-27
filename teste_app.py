import requests

url = "https://megometria-api.onrender.com/dados"

r = requests.get(url)

print(r.status_code)
print(r.text)