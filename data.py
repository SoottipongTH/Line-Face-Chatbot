import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def find_data(product_name):
    docs = db.collection('new-product').where("name","array_contains",product_name).get()
    for doc in docs: 
        return doc.to_dict()


# print(find_data("น้ำพริกกุ้ง"))




# json_file = open("product.json", 'r', encoding='utf-8')
# json_data = json.load(json_file)
# # for i in json_data['new-product']:
# #     print(i['name'])


# def add_collection():
#     for data in json_data['new-product']:
#         db.collection('new-product').document(data['name'][0]).set(data)
    
# add_collection()



