#writefile app.py
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification, pipeline
import re
from pydantic import BaseModel, Field
from PIL import Image

ner_model_name = "Gorengoz/bert-based-Turkish-NER-wikiann"
sentiment_model_name = "Gorengoz/bert-turkish-sentiment-analysis-cased"

# Initialize tokenizers and models for NER
ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

# Initialize tokenizers and models for Sentiment Analysis
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

# Create pipelines for NER and Sentiment Analysis
ner_pipeline = pipeline("token-classification", model=ner_model, tokenizer=ner_tokenizer)
sentiment_pipeline = pipeline("text-classification", model=sentiment_model, tokenizer=sentiment_tokenizer)


label_mapping = {
    "LABEL_0": "olumlu",
    "LABEL_1": "nötr",
    "LABEL_2": "olumsuz"
}

class SentimentResult(BaseModel):
    entity: str
    sentiment: str

class AnalysisResponse(BaseModel):
    entity_list: list
    sentiment_list: list
# Her entity için cümleleri parçalama
def get_entity_sentences(entity: str, sentences: list) -> list:
    return [sent for sent in sentences if entity in sent]

def predict(review): 
    # NER modelini kullanarak entity'leri bulma
    entities = ner_pipeline(review, aggregation_strategy="simple")
    
    unique_entities = set([entity['word'] for entity in entities])
    
    # Cümleleri hem '.' hem de ',' ile bölme
    sentences = re.split(r'[.,]', review)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    # Sentiment modelimizi kullanma
    entity_sentiments = {}
    for entity in unique_entities:
        entity_sentences = get_entity_sentences(entity, sentences)
        sentiments = [sentiment_pipeline(sentence) for sentence in entity_sentences]

        flattened_sentiments = [item for sublist in sentiments for item in sublist]
        
        # Entitilerin sentimentini bulma
        if flattened_sentiments:
            sentiment_scores = [sent['label'] for sent in flattened_sentiments]
            mapped_sentiments = [label_mapping.get(label, 'unknown') for label in sentiment_scores]
            sentiment = max(set(mapped_sentiments), key=mapped_sentiments.count)  # Bir marka için farklı sentimentler bulunduğunda en baskın olanı kabul etme.
        else:
            sentiment = 'nötr'  
            
        entity_sentiments[entity] = sentiment

        entity_list=list(entity_sentiments.keys())
        sentiment_list=list(entity_sentiments.values())

    return entity_list, sentiment_list


def send_email(to_address, subject, body):
    # Configure email details
    from_address = 'gorengozun@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'gorengozun@gmail.com'
    smtp_password = 'jtbb gfbd rfix thoe'  

    # Create email message
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_address, to_address, msg.as_string())

def send_customer_response(customer_email, sentiment):
    if sentiment == "olumlu":
        subject = "Geri Bildiriminiz İçin Teşekkürler"
        body = (f"Merhaba,\n\n"
                f"Geri bildiriminiz tarafımıza ulaştı ve olumlu değerlendirildi.\n\n"
                f"Memnuniyetiniz için teşekkür ederiz. Düşünceleriniz bizim için çok değerlidir ve bu tür olumlu yorumlar bizi motive eder. Size en iyi hizmeti sunmak için sürekli olarak çalışıyoruz.\n\n"
                f"Herhangi bir ek bilgiye ihtiyacınız olursa, lütfen bizimle iletişime geçin.\n\n"
                f"Saygılarımızla,\n")
    else:
        subject = "Şikayetiniz Alındı ve Üzerinde Çalışıyoruz"
        body = (f"Merhaba,\n\n"
                f"Şikayetiniz tarafımıza ulaştı ve değerlendirilmek üzere alındı.\n\n"
                f"Şikayetinizle ilgili olarak size geri dönüş yapacağız ve sorunun çözümü için gerekli adımları atacağız.\n\n"
                f"Herhangi bir ek bilgiye ihtiyacınız olursa, lütfen bizimle iletişime geçin.\n\n"
                f"İlginiz için teşekkür ederiz.\n\n"
                f"Saygılarımızla,\n")

    send_email(customer_email, subject, body)


def process_complaints(complaint):
        organizations, sentiment = predict(complaint)
        for org in organizations:
            # Construct email subject and body
            subject = f"{org} Hakkında Müşteri Geri Bildirimi"
            body = (f"Merhaba {org} Ekibi,\n\n"
                    f"Müşterilerimizden gelen aşağıdaki yorum tarafımıza iletilmiştir:\n\n"
                    f"Yorum: {complaint}\n\n"
                    f"Analiz: {sentiment[organizations.index(org)]}\n\n"
                    f"Geri bildirimleri ele alıp değerlendirdiğiniz için teşekkür ederiz. Bu konuda gerekli aksiyonları alacağınızdan eminiz. Herhangi bir ek bilgiye "
                    f"ihtiyacınız olursa lütfen bizimle iletişime geçin.\n\n"
                    f"İyi çalışmalar dileriz.\n\n"
                    f"Saygılarımızla,\n")
            # Use the fixed brand email address
            to_address = "marka.eposta@gmail.com"
            send_email(to_address, subject, body)

        # Sending response to the customer
        send_customer_response(customer_email, sentiment)

# Streamlit application
col1, col2, col3 = st.columns(3)
# Merkezi konumlandırma için bir sütun düzeni kullanma
col1, col2, col3 = st.columns([1, 3, 2])  # Oranları isteğinize göre ayarlayabilirsiniz

with col1:
    st.write(" ")
with col2:
    image = Image.open('gg.png')
    st.image(image, width=400)
with col3:
    st.write(" ")

st.title('Müşteri Geri Bildirim Yönetimi')

# st.header('Yorum Bildir')
st.write("Müşteri/Tüketici Geri Bildirimi Yönetim Sistemi ile memnuniyet veya şikâyetlerinizi tarafımıza bildirebilirsiniz. ")
st.write("E-posta bilgilerinizi girerek 'Şikayet Gönder' butonuna tıklamanız dahilinde form verileri doğrulanır. ")
st.write("Geri bildirimizde belirttiğiniz her bir organizasyona memnuniyet veya şikâyetiniz iletildikten sonra; tarafınıza mail yoluyla bilgilendirme yapılır.")
with st.form(key='complaint_form'):
    complaint_text = st.text_area("Yorum Metni")
    customer_email = st.text_input("Müşteri E-Posta Adresi")
    submit_button = st.form_submit_button(label='Gönder')

if submit_button:
    if complaint_text and customer_email:
        process_complaints(complaint_text)
        st.success('Geri bildirim başarıyla işlendi ve e-postalar gönderildi.')
    else:
        st.error('Lütfen tüm alanları doldurduğunuzdan emin olun.')


# Trendyol sitesinden aldığım ürünü çok beğendim. Ancak kargolama berbattı @ArasKargo
