import requests
import time
api_key=""
city="37.386051%2C-122.083855" # Mountain View
city="37.352390%2C-121.953079" # Santa Clara
radius="15000" # 15 km
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=church&key={api_key}".format(radius=radius, api_key=api_key, location=city)
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
places = []
while response.json()["status"] == "OK":
	response_json = response.json()
	results = response.json()["results"]
	print(len(results))
	for place in results:
		places.append({"place_id": place["place_id"], "name": place["name"]})
	if "next_page_token" in response_json:
		url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={api_key}&pagetoken={page_token}".format(page_token=response_json["next_page_token"], api_key=api_key)
		time.sleep(3)
		response = requests.request("GET", url, headers=headers, data=payload)
		continue
	else:
		break

for place in places:
	url = "https://maps.googleapis.com/maps/api/place/details/json?fields=website,formatted_address&place_id={place}&key={key}".format(place=place["place_id"],key=api_key)
	response = requests.request("GET", url, headers=headers, data=payload)
	time.sleep(2)
	if "result" in response.json():
		if "formatted_address" in response.json()["result"]:
			place["formatted_address"] = response.json()["result"]["formatted_address"]
		if "website" in response.json()["result"]:
			place["website"] = response.json()["result"]["website"]

print(places)
