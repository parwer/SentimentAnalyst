import keras
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import tokenizer_from_json
import json

with open('results/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)

model = keras.models.load_model('results/model.h5')

def predict(txt):
    word2vec = pad_sequences(tokenizer.texts_to_sequences([txt]), maxlen=30)
    predict = model.predict(word2vec)
    return set_sentiment(predict)

def set_sentiment(vector):
    if vector > 0.5:
        return "positive"
    else:
        return "negative"



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