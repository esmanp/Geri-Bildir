
# Geri Bildir

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Streamlit App](https://docs.streamlit.io/logo.svg)](https://docs.streamlit.io)


Geri Bildir, tüketicilerin aldıkları ürün veya hizmet karşılığı oluşturduğu geri bildirimlerinin analiz edilerek ilgili sağlayıcılara iletilmesini kolaylaştırmak amacıyla geliştirilmiştir. Tüketiciler ve organizasyonlar arasında bir köprü görevi sağlar.

![uygulama](https://github.com/esmanp/gorengoz2024/blob/main/uygulama.png?raw=true)

## Problem Tanımı

“İnsanların güvenini kaybetmektense para kaybetmeyi tercih ederim!”
Robert Bosch

Müşteri önce şikayetini veya geri bildirimini iletir, ardından şikâyete konu durum belgelendirilir ve şikâyet, işletmenin ilgili birimleri tarafından çözümlenmek üzere yolculuğuna başlar...

Bu sürece en basit haliyle şikâyet yönetimi denir.

## PROJENİN SAĞLADIĞI ÇÖZÜM

##### Hedef kitle
- Kurumsal Şirketler
- Müşteri/ Tüketiciler

##### Çözüm
- Basit ve Kullanışlı Arayüz
- Gizlilik
- Hızlı Geri Bildirim
- Memnuniyet Bildirimi
- ISO 10002 Müşteri Memnuniyeti Yönetim Sistemi Belgesi

## Katkılarımız

### Veri Seti

https://huggingface.co/datasets/Gorengoz/tr-customerreview

### Hugging Face Modeli

#### Geliştirilen Text-Classification Modelleri

https://huggingface.co/Gorengoz/bert-turkish-sentiment-analysis-cased

https://huggingface.co/Gorengoz/bert-turkish-sentiment-analysis-winvoker

#### Geliştirilen NER Modelleri

https://huggingface.co/Gorengoz/bert-based-Turkish-NER

https://huggingface.co/Gorengoz/bert-based-Turkish-NER-wikiann

### Site 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://geri-bildir.streamlit.app/)
  

## Bu web uygulamasını kendi bilgisayarınızda yeniden oluşturmak için aşağıdaki adımları takip edebilirsiniz: 

```bash
  wget https://github.com/esmanp/Geri-Bildir/blob/main/requirements.txt

```

```bash
pip install -r requirements.txt
```

```bash
  wget https://github.com/esmanp/Geri-Bildir/archive/refs/heads/main.zip
```

```bash
 unzip main.zip
```

```bash
 streamlit run app.py
```

Bu proje TEKNOFEST 2024 Türkçe Doğal Dil İşleme Yarışması'na katılmak amacıyla Görengöz ekibi tarafından geliştirilmiştir. #Acikhack2024
    


  
