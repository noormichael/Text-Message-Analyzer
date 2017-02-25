#!/usr/bin/env python3

# ANGAD

import requests
import json

key_num = '421941424606546'

r = requests.get("https://graph.facebook.com/v2.3/" + key_num + "/comments?limit=25&__paging_token=enc_AdDROMkcRsTE08ZAeZAZC0goPHEgAdSiS2XuClMPBqiHdYXGUtILUCkwkTvST10QkWWtGejwZAgmKg2zZBvgVwpeuo2UZA&since=1483568411&__previous=1&access_token=EAACEdEose0cBAEocbeN4HW1NwQAqKiq3ci9wFZCSZB5oxg68tjZAQHPMnI91jZCzZB90YCqrHDZCjVa3OSJRxRicIzZAjG3H58OhKz4OjGZCUFKT9PQVJ4smQ1Num1Iuv0zfnx2I0R5iXnba4TwCCpJ0kslzyu2aehxtJwgt27hL9C4jZCUAvezEmHSluEmaGROMZD")
list_a = []
list_b = []
a_id = ""
b_id = ""
a_name = ""
b_name = ""
messages = json.loads(r.text)
for data in messages["data"]:
    if "message" not in data.keys():
        continue
    if not list_a:
        a_id = data["from"]["id"]
        a_name = data["from"]["name"]
        list_a.append(data["message"])
        continue
    if not b_id and a_id != data["from"]["id"]:
        b_id = data["from"]["id"]
        b_name = data["from"]["name"]
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

# NOOR

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

a_messages = list_a
b_messages = list_b

print("A's name: ", a_name)
print("B's name: ", b_name)

'''
import xml.etree.ElementTree as ET

root = ET.parse('sms_corpus.xml').getroot()

# lists of messages
a_messages = [m.find('text').text for m in root if int(m.attrib['id']) % 2 == 0]
b_messages = [m.find('text').text for m in root if int(m.attrib['id']) % 2 == 1]
'''

sid = SentimentIntensityAnalyzer()

'''
Compound: Intensity
Pos/Neg/Neu: Polarity
'''

a_scores = [sid.polarity_scores(m) for m in a_messages]
b_scores = [sid.polarity_scores(m) for m in b_messages]

a_total_scores = {k: sum([s[k] for s in a_scores]) for k in set(a_scores[0])}
b_total_scores = {k: sum([s[k] for s in b_scores]) for k in set(b_scores[0])}

# Total amount of pos/neg

A_TOTAL_POS = a_total_scores['pos']
B_TOTAL_POS = b_total_scores['pos']
A_TOTAL_NEG = a_total_scores['neg']
B_TOTAL_NEG = b_total_scores['neg']

if A_TOTAL_POS > B_TOTAL_POS and B_TOTAL_NEG > A_TOTAL_NEG:
	print("A likes B but B doesn't like A")
elif A_TOTAL_POS < B_TOTAL_POS and B_TOTAL_NEG < A_TOTAL_NEG:
	print("B likes A but A doesn't like B")

print("A Total POS: ", A_TOTAL_POS)
print("B Total POS: ", B_TOTAL_POS)
print("A Total NEG: ", A_TOTAL_NEG)
print("B Total NEG: ", B_TOTAL_NEG)

# Total number of pos/neg/neu

A_NUM_POS = len([s for s in a_scores if s['pos'] > s['neg']])
B_NUM_POS = len([s for s in b_scores if s['pos'] > s['neg']])

A_NUM_NEG = len([s for s in a_scores if s['pos'] < s['neg']])
B_NUM_NEG = len([s for s in b_scores if s['pos'] < s['neg']])

A_NUM_NEU = len([s for s in a_scores if s['neu'] == 1.0])
B_NUM_NEU = len([s for s in b_scores if s['neu'] == 1.0])

print("A Num POS: ", A_NUM_POS)
print("A Num NEG: ", A_NUM_NEG)
print("A Num NEU: ", A_NUM_NEU)
print("B Num POS: ", B_NUM_POS)
print("B Num NEG: ", B_NUM_NEG)
print("B Num NEU: ", B_NUM_NEU)

# Weighted total amount of pos/neg

a_weighted_pos = sum([s['pos']*s['compound'] for s in a_scores if s['pos'] > 0])/len(a_scores)
a_weighted_neg = sum([-1*s['neg']*s['compound'] for s in a_scores if s['neg'] > 0])/len(a_scores)

b_weighted_pos = sum([s['pos']*s['compound'] for s in b_scores if s['pos'] > 0])/len(b_scores)
b_weighted_neg = sum([-1*s['neg']*s['compound'] for s in b_scores if s['neg'] > 0])/len(b_scores)

print("A Weighted POS: ", a_weighted_pos)
print("A Weighted NEG: ", a_weighted_neg)
print("B Weighted POS: ", b_weighted_pos)
print("B Weighted NEG: ", b_weighted_neg)

# Neutral Ratios

print("A Neutral Ratio", A_NUM_NEU/len(a_scores))
print("B Neutral Ratio", B_NUM_NEU/len(b_scores))