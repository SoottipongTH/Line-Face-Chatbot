from pythainlp import word_tokenize
from pythainlp.util.trie import Trie
from data import find_data
import json
from pathlib import Path
import keras
import numpy as np
import pickle
import random

model_path = Path("Model/evaluate/sequential")
data_path = Path("data.pickle")
intents_path = Path("newIntents.json")


with open(intents_path, "r", encoding="utf-8") as f:
    intents = json.load(f)

model = keras.models.load_model(model_path)

with open(data_path, "rb") as file:
    words, labels, training, output = pickle.load(file)

with open(Path("product.json"), "r", encoding="utf-8") as f:
    products = json.load(f)

product_list = []

for product in products['new-product']:
    for i in product['name']:
        product_list.append(i)

trie = Trie(product_list)
context = {}

def process(user_input):
    tokens = word_tokenize(user_input, custom_dict=trie,
                           engine="deepcut", keep_whitespace=False)
    for token in tokens:
        if token in product_list:
            data = find_data(token)
            return data
    else:
        bag = [0]*len(words)
        for stem in tokens:
            for i, w in enumerate(words):
                if w == stem:
                    bag[i] = 1
        return np.array([bag])

def context_initializer(userID):
    if userID not in context:
        # print("enter bot context init")
        context[userID] = 'bot'


def response(user_input, userID):
    data = process(user_input)
    context_initializer(userID)
    

    if type(data) == dict:
        if context[userID] == 'admin':
            return None
        return_data = 'ชื่อสินค้า : {}\n'.format(data['name'][0])
        if 'alter' in data:
            for alter in data['alter']:
                return_data += 'ปริมาณ : {} ราคา : {}\n'.format(
                    alter['description'], alter['price'])
            return return_data
        else:
            return 'ชื่อสินค้า : {}\nปริมาณ : {} \nราคา : {}'.format(data['name'][0], data['description'], data['price'])

    else:
        res = predict(user_input, userID)
        return res


def predict(user_input, userID):
    results = model.predict(process(user_input))
    results_index = np.argmax(results)
    tag = labels[results_index]
    context_initializer(userID)
    # print(context)
    # print(results[0, results_index])
    for i in intents['intents']:
        if tag == i['tag']:
            if 'context_set' in i:
                # print("context changed")
                context[userID] = i['context_set']
            if not 'context_filter' in i or \
                    (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                response = random.choice(i['response'])
                # print(context)
                if type(response) == None:
                    return False
                if results[0, results_index] >= 0.5:
                    return response
                else:
                    return "ขอโทษครับ ไม่เข้าใจคำถาม หากต้องการติดต่อแอดมิน สามารถพิมพ์ 'แอดมิน' ได้เลยครับ"


while (True):
    user_input = input("enter message : ")
    if user_input == "exit":
        break
    print(response(user_input, userID="123"))
