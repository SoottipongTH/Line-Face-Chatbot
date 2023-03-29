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
import json
from pathlib import Path


#todo
# with open('product.txt', 'r',encoding='utf-8') as f:
#     lines = f.readlines()
#     for line in lines:
#         product.append(line.strip())
#todo
with open(Path("product.json"), "r", encoding="utf-8") as f:
    products = json.load(f)

product_list = []

for product in products['new-product']:
    for i in product['name']:
        product_list.append(i)

trie = Trie(product_list)


def process(user_input):
    tokens = word_tokenize(user_input,custom_dict=trie, engine="newmm")
    for token in tokens:
        if token in product_list:
            data = find_data(token)
            return data
        else:
            data = "ไม่พบสินค้าที่ท่านต้องการ"
            return data




def response(user_input):
    data = process(user_input)
    return_data = 'ชื่อสินค้า : {}\n'.format(data['name'][0])
    if type(data) == dict:
        if 'alter' in data:
            for alter in data['alter']:
                return_data += 'ปริมาณ : {} ราคา : {}\n'.format(alter['description'],alter['price']) 
            return return_data   
        else:
            return 'ชื่อสินค้า : {}\nปริมาณ : {} \nราคา : {}'.format(data['name'][0],data['description'],data['price'])
    else:
        return data
    
print(response("ข้าวเนียว"))



# while(True):
#     user_input = input("You : ")
    
#     if user_input == "exit":
#         break

#     print(find_product(user_input))
