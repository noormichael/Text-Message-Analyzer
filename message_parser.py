import requests
import json

r = requests.get("https://graph.facebook.com/v2.3/186957608173966/comments?limit=25&__paging_token=enc_AdDROMkcRsTE08ZAeZAZC0goPHEgAdSiS2XuClMPBqiHdYXGUtILUCkwkTvST10QkWWtGejwZAgmKg2zZBvgVwpeuo2UZA&since=1483568411&__previous=1&access_token=EAACEdEose0cBAEocbeN4HW1NwQAqKiq3ci9wFZCSZB5oxg68tjZAQHPMnI91jZCzZB90YCqrHDZCjVa3OSJRxRicIzZAjG3H58OhKz4OjGZCUFKT9PQVJ4smQ1Num1Iuv0zfnx2I0R5iXnba4TwCCpJ0kslzyu2aehxtJwgt27hL9C4jZCUAvezEmHSluEmaGROMZD")
list_a = []
list_b = []
a_id = ""
b_id = ""
messages = json.loads(r.text)
for data in messages["data"]:
    if "message" not in data.keys():
        continue
    if not list_a:
        a_id = data["from"]["id"]
        list_a.append(data["message"])
        continue
    if not b_id and a_id != data["from"]["id"]:
        b_id = data["from"]["id"]
    if data["from"]["id"] == a_id:
        list_a.append(data["message"])
    else:
        list_b.append(data["message"])
for x in range(40):
    r = requests.get(messages["paging"]["next"])
    messages = json.loads(r.text)
    for data in messages["data"]:
        if "message" not in data.keys():
            continue
        if not list_a:
            a_id = data["from"]["id"]
            list_a.append(data["message"])
            continue
        if not b_id and a_id != data["from"]["id"]:
            b_id = data["from"]["id"]
        if data["from"]["id"] == a_id:
            list_a.append(data["message"])
        else:
            list_b.append(data["message"])
print(list_a)
print("\n\n\n\n")
print(list_b)
