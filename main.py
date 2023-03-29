# from pathlib import Path
# import pickle
# import json

# import numpy as np
# from pythainlp import word_tokenize
# import keras
# from data import find_data

# model_path = Path("model")
# data_path = Path("data.pickle")
# intents_path = Path("intents.json")


# with open(intents_path, "r", encoding="utf-8") as f:
#     intents = json.load(f)

# model = keras.models.load_model(model_path)

# with open(data_path, "rb") as file:
#     words, labels, training, output = pickle.load(file)




# context = {}


# def chat(user_input, userID):
#     results = model.predict(clean(user_input))
#     results_index = np.argmax(results)
#     tag = labels[results_index]
    
#     for i in intents['intents']:
#         if tag == i['tag']:
#             if 'context_set' in i:
#                 context[userID] = i['context_set']
#             if not 'context_filter' in i or \
#                     (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
#                 response = find_data(tag)
#                 print(context)
#                 return response
            

# print(chat("นมข้าวโพดไหม", 123))


from pythainlp import word_tokenize
from pythainlp.util.trie import Trie
from data import find_data


#todo
product = []
with open('product.txt', 'r',encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        product.append(line.strip())
#todo
    

trie = Trie(product)


def process(user_input):
    tokens = word_tokenize(user_input,custom_dict=trie, engine="newmm")
    for token in tokens:
        if token in product:
            data = find_data(token)
            return data
        else:
            data = "ไม่พบสินค้าที่ท่านต้องการ"
            return data




# print(process("น้ำพริกกุ้ง"))



def response(user_input):
    data = process(user_input)

    if type(data) == dict:
        return_data = {
            "ชื่อสินค้า": data['name'][0],
            "ปริมาณ": data['quantity'],
            "ราคา" : data['price']
        }
        return return_data
    else:
        return data

# print(response("น้ำพริกกุ้ง"))    

# ชื่อสินค้า: Name
# ราคา: Price
# ขนาด: quantity
    













# def find_product(input_str):
#     for i in product:
#         if i in input_str: 
#             product_name = i
#         else:
#             return False
#         return product_name

# def clean(input_str):
    















# while(True):
#     user_input = input("You : ")
    
#     if user_input == "exit":
#         break

#     print(find_product(user_input))
