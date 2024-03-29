from pathlib import Path
import pickle
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from pythainlp import word_tokenize
from matplotlib import pyplot as plt


import json
import numpy as np

def sequential_model():
    data_path = Path("../data.pickle")
    model_path = Path("evaluate/sequential")

    with open(data_path, "rb") as file:
        words, labels, training, output = pickle.load(file)

    tf.compat.v1.reset_default_graph()
    #define model
    model = Sequential()
    model.add(Dense(16, activation="relu" , input_shape=(len(training[0]),)))
    model.add(Dense(8, activation="relu")) 
    model.add(Dense(len((output[0])), activation="softmax"))
    
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    history = model.fit(training,output, epochs=40, batch_size=8)
    
     # accuracy and epoch
    plt.plot(history.history["accuracy"])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.show()

    # loss and epoc
    plt.plot(history.history["loss"])
    plt.title("model loss")
    plt.ylabel("loss")
    plt.xlabel("epoch")
    plt.show()
    
    
    model.save(model_path)

def create_bag_of_words():
    intents_path = Path("../newIntents.json")
    pickle_path = Path("../data.pickle")

    with open(intents_path, "r", encoding="utf-8") as file:
        data = json.load(file)


    words = []
    labels = []
    docs_x = []
    docs_y = []
    
    for intent in data["intents"]:
        print(intent)
        for pattern in intent["patterns"]:
            print(pattern)
            tokens = word_tokenize(pattern.lower(), engine="deepcut", keep_whitespace=False)
            for token in tokens:
                if token not in words:
                    words.append(token)
            docs_x.append(tokens)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
            
  

    words = sorted(list(set(words)))

    labels = sorted(labels)

    print(docs_x)
    print("--------------------")
    print(words,"length", len(words))
    print(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        for w in words:
            if w in doc:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)
        
    training = np.array(training)
    output = np.array(output)

    with open(pickle_path, "wb") as file:
        pickle.dump((words, labels, training, output), file)
        