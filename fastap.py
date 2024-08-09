import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification, pipeline
import re

app = FastAPI()

# Geliştirdiğimiz modeller
ner_model_name = "Gorengoz/bert-based-Turkish-NER-wikiann"
sentiment_model_name = "Gorengoz/bert-turkish-sentiment-analysis-cased"

# NER modeli
ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

# Sentiment modeli
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

# Modelleri kullanmak için Pipeline'lar oluşturma
ner_model = pipeline("token-classification", model=ner_model, tokenizer=ner_tokenizer)
sentiment_analyzer = pipeline("text-classification", model=sentiment_model, tokenizer=sentiment_tokenizer)

# Modeli eğitirken kullandığımız labelları olumlu, olumsuz ve nötr'e çevirme
label_mapping = {
    "LABEL_0": "olumlu",
    "LABEL_1": "nötr",
    "LABEL_2": "olumsuz"
}

class Item(BaseModel):
    text: str = Field(..., example="""Fiber 100mb SuperOnline kullanıcısıyım yaklaşık 2 haftadır @Twitch @Kick_Turkey gibi canlı yayın platformlarında 360p yayın izlerken donmalar yaşıyoruz.  Başka hiç bir operatörler bu sorunu yaşamazken ben parasını verip alamadığım hizmeti neden ödeyeyim ? @Turkcell """)

class SentimentResult(BaseModel):
    entity: str
    sentiment: str

class AnalysisResponse(BaseModel):
    entity_list: list
    results: list[SentimentResult]

# Her entity için cümleleri parçalama
def get_entity_sentences(entity: str, sentences: list) -> list:
    return [sent for sent in sentences if entity in sent]

@app.post("/predict/", response_model=dict)
async def predict(item: Item):
    review = item.text
    
    # NER modelini kullanarak entity'leri bulma
    entities = ner_model(review, aggregation_strategy="simple")
    
    unique_entities = set([entity['word'] for entity in entities])
    
    # Cümleleri hem '.' hem de ',' ile bölme
    sentences = re.split(r'[.,]', review)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    # Sentiment modelimizi kullanma
    entity_sentiments = {}
    for entity in unique_entities:
        entity_sentences = get_entity_sentences(entity, sentences)
        sentiments = [sentiment_analyzer(sentence) for sentence in entity_sentences]

        flattened_sentiments = [item for sublist in sentiments for item in sublist]
        
        # Entitilerin sentimentini bulma
        if flattened_sentiments:
            sentiment_scores = [sent['label'] for sent in flattened_sentiments]
            mapped_sentiments = [label_mapping.get(label, 'unknown') for label in sentiment_scores]
            sentiment = max(set(mapped_sentiments), key=mapped_sentiments.count)  # Bir marka için farklı sentimentler bulunduğunda en baskın olanı kabul etme.
        else:
            sentiment = 'nötr'  
            
        entity_sentiments[entity] = sentiment

    response = AnalysisResponse(
        entity_list=list(entity_sentiments.keys()),
        results=[SentimentResult(entity=entity, sentiment=sentiment) for entity, sentiment in entity_sentiments.items()])
         
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
