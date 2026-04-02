# threat-detection

## Hakkında
Bu sistem, video görüntülerini gerçek zamanlı olarak analiz ederek nesneleri tespit eder ve tehlikeli mi güvenli mi olduğuna karar verir. Bıçak, makas gibi tehlikeli nesneler kırmızı kutu ile, kitap, bardak gibi güvenli nesneler yeşil kutu ile gösterilir.

Amaç, güvenlik sistemlerine entegre edilebilecek otomatik bir tehdit algılama katmanı sunmaktır. Örneğin anaokulları, okullar veya kamu alanlarındaki güvenlik kameralarına entegre edilerek manuel izleme ihtiyacı olmadan tehlikeli nesneler tespit edilebilir.

API kullanımını minimize etmek için sonuçlar JSON dosyasına kaydedilir. Her nesne Gemini AI'ya yalnızca bir kez sorulur, sonraki tespitlerde cache'den okunur. Bu sayede hem maliyet hem de yanıt süresi azaltılır.
 
# AI-Driven Threat Detection System

Real-time threat detection system using YOLOv8 and Google Gemini AI.

## How it works
- YOLOv8 detects objects in video frames
- Gemini AI classifies each object as dangerous or safe
- Results are cached in JSON to minimize API calls
- Dangerous objects → Red box, Safe objects → Green box

## Installation
```bash
pip install -r requirements.txt
```

## Setup
1. Get a free API key at [aistudio.google.com](https://aistudio.google.com)
2. Create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage
```bash
python main.py
```
