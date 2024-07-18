import requests

url = "http://127.0.0.1:5000/ask"
user_query = "Mewɔ ateetee ne kosii dodo. Dɛn na menyɛ?"

response = requests.post(url, json={"query": user_query})

print(response.json()["response"])
