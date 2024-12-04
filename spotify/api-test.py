import requests

url = "https://api.spotify.com/v1/me/playlists"
headers = {
    "Authorization": "Bearer 73a18a89b2934c40a04fbccefb71934d"
}

response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    data = response.json()
    print("Playlists:", data)
else:
    print("Error:", response.status_code, response.text)
