import cv2 #Video okuma, kutu çizme, ekranda gösterme
import json #Veriyi dosyaya kaydetmek ve okumak
import os #.env dosyasını okur, dosya var mı yok mu kontrol eder
import time #API için time sınırlama 15*4=60 
from dotenv import load_dotenv #.env dosyasındaki key'i programa yükler
import google.generativeai as genai #gemini API'i bağlar
from ultralytics import YOLO #nesneyi tanır

#.env dosyasını yükler
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_gemini=genai.GenerativeModel("gemini-2.5-flash")
model_yolo=YOLO("yolov8m.pt")


cache = {}
if os.path.exists("cache.json"):
    with open("cache.json","r") as f:
        cache=json.load(f)



def  ask_gemini(name):
    try:
        response = model_gemini.generate_content(
            f"Is '{name}' dangerous or safe? Answer with exactly one word only: dangerous or safe. No other text."
        )
       
        result=response.text.strip().lower()

        print(f"{name} -> Gemini cevabı: {result}")
        
        if "dangerous" in result:
            return "dangerous"
        else:
            return "safe"
    except:
        print("Error : Connection issues!")
        return "safe"
        

cap=cv2.VideoCapture("demo.mp4") #görüntüyü alır


while True:
    ret, frame=cap.read() #piksel  piksel alır. Başaralı ise ret true değilse false.

    if not ret:
        print("Unable to play video")
        break
    
    results=model_yolo(frame) #tespit edilen nesneleri döndürür
    detections=results[0].boxes #bıçak, kaşık, kitap

    for box  in detections: #nesneleri tek tek alır
        class_id=int(box.cls[0]) #nesnenin sınıf numarasını döndürür
        name=model_yolo.names[class_id] #numarayı nesnenin ismine çevirir

        if name not in cache: #daha önceden nesne tanımlanmadıysa
            cache[name]=ask_gemini(name) #cache["scissors"] = "dangerous" gemini'ye sorar ve cache içine yazar
            with open("cache.json","w") as f: #kalıcı cahce içine yazar
                json.dump(cache,f)
            time.sleep(4)
        
        decision=cache[name] #nesnenin dangerous mu yoksa safe mi döndürür
        if decision == "dangerous": 
            color=(0,0,255) #kırmızı yapar
        else:
            color=(0,225,0) #yeşil yapar

        x1, y1, x2, y2=map(int,box.xyxy[0]) #nesnenin kordinatlarını alır   
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        cv2.putText(frame, f"{name} - {decision}",(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Result",frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break;

cap.release()
cv2.destroyAllWindows()





