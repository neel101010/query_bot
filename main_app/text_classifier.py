import pickle
import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from pathlib import Path

temp = Path(__file__).resolve().parent.parent
temp = str(temp)
BASE_DIR = ""
for i in temp:
    if(i=='\\'):
        BASE_DIR = BASE_DIR + '/'
    else:
        BASE_DIR = BASE_DIR + i


model = load_model(BASE_DIR + "/main_app/001", compile = True)
# loading tokenizer
with open( BASE_DIR + '/main_app/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

print("Text Classifer Done")

def do_prediction(question):
    questions_list = []
    questions_list.append(question)
    sequence = tokenizer.texts_to_sequences(questions_list)
    test = pad_sequences(sequence, maxlen=200)
    predictions = model.predict(test)
    prediction_value = np.around(predictions, decimals=0).argmax(axis=1)
    if prediction_value[0] == 0 : 
        print("General conversation")
        return 0
    
    if prediction_value[0] == 1 :
        print("Topic specific conversation")
        return 1

    print("Something went wrong")
    return "Error"
