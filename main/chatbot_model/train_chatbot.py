import json, random, pickle, numpy as np, os
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')  # Para WordNet
nltk.download('punkt_tab')  # ← Este es el que está pidiendo


lemmatizer = WordNetLemmatizer()
words, classes, documents = [], [], []
ignore_letters = ['?', '!', '.', ',']

with open("main/chatbot_model/data/intents.json", encoding="utf-8") as file:
    intents = json.load(file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        documents.append((tokens, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(set([lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]))
classes = sorted(set(classes))

pickle.dump(words, open("main/chatbot_model/data/words.pkl", 'wb'))
pickle.dump(classes, open("main/chatbot_model/data/classes.pkl", 'wb'))


training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = [1 if w in [lemmatizer.lemmatize(w_.lower()) for w_ in doc[0]] else 0 for w in words]
    output_row = output_empty[:]
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)
train_x, train_y = list(training[:, 0]), list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=SGD(0.01, 1e-6, 0.9), metrics=['accuracy'])
model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save("main/chatbot_model/models/chat_model.h5")
print("✅ Modelo entrenado y guardado correctamente.")
