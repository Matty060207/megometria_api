import requests

url = "https://megometria-api.onrender.com/dados"

resposta = requests.post(url, json={
    "dispositivo": "teste",
    "valor": 12.5
})

print(resposta.text)