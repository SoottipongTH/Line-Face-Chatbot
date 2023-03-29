# from pathlib import Path
# import pickle
# import tensorflow as tf
# from keras.optimizers import Adam
# from keras import Sequential
# from keras.layers import Bidirectional, Dense
# from pythainlp import word_tokenize
# from matplotlib import pyplot as plt


# import json
# import numpy as np
# import pandas as pd

# def Bilstm_model():
#     data_path = Path("data.pickle")
#     model_path = Path("Evaluate/BILSTM")

#     with open(data_path, "rb") as file:
#         words, labels, training, output = pickle.load(file)

#     tf.compat.v1.reset_default_graph()
#     #define model
#     model = Sequential()
#     model.add(Bidirectional(64, input_shape=(len(training[0]),)))
#     model.add(Bidirectional(32, activation="relu")) 
#     model.add(Dense(len((output[0])), activation="softmax"))
    

#     optimizer = Adam(learning_rate=0.001)
#     model.compile(loss="categorical_crossentropy", metrics=["accuracy"])
#     history = model.fit(training,output, epochs=120, batch_size=8)
    
#      # accuracy and epoch
#     plt.plot(history.history["accuracy"])
#     plt.title("model accuracy")
#     plt.ylabel("accuracy")
#     plt.xlabel("epoch")
#     plt.show()

#     # loss and epoc
#     plt.plot(history.history["loss"])
#     plt.title("model loss")
#     plt.ylabel("loss")
#     plt.xlabel("epoch")
#     plt.show()
    
    
#     model.save(model_path)

# def create_bag_of_words():
#     intents_path = Path("intents.json")
#     pickle_path = Path("data.pickle")

#     with open(intents_path, "r", encoding="utf-8") as file:
#         data = json.load(file)


#     words = []
#     labels = []
#     docs_x = []
#     docs_y = []
    
#     for intent in data["intents"]:
#         for pattern in intent["patterns"]:
#             tokens = word_tokenize(pattern.lower(), engine="newmm", keep_whitespace=False)
#             words.extend(tokens)
#             docs_x.append(tokens)
            
#             docs_y.append(intent["tag"])
            
#         if intent["tag"] not in labels:
#             labels.append(intent["tag"])
            
#     print(docs_x)
#     print(words)

#     words = sorted(list(set(words)))
    

#     labels = sorted(labels)

#     training = []
#     output = []

#     out_empty = [0 for _ in range(len(labels))]

#     for x, doc in enumerate(docs_x):
#         bag = []

#         for w in words:
#             if w in doc:
#                 bag.append(1)
#             else:
#                 bag.append(0)
#         output_row = out_empty[:]
#         output_row[labels.index(docs_y[x])] = 1
        
#         training.append(bag)
#         output.append(output_row)
        
#     training = np.array(training)
#     output = np.array(output)

#     with open(pickle_path, "wb") as file:
#         pickle.dump((words, labels, training, output), file)
        