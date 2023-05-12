import keras
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import tokenizer_from_json
import json
from googletrans import Translator
translator = Translator()

#import tokenizer
with open('results/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)

#import model
model = keras.models.load_model('results/model.h5')

def predict(txt):
    txt = translator.translate(txt, dest='en')
    word2vec = pad_sequences(tokenizer.texts_to_sequences([txt.text]), maxlen=30)
    predict = model.predict(word2vec)
    return set_sentiment(predict)

def set_sentiment(vector):
    if vector > 0.7:
        return "positive"
    elif vector < 0.4:
        return "negative"
    else:
        return "neural"


#webAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def index(data: dict):
    txt = data.get("txt")
    x = predict(txt)
    return {"txt": x}