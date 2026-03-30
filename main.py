import cv2 
import json 
import os 
import time 
from dotenv import load_dotenv 
import google.generativeai as genai 
from ultralytics import YOLO 


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
        

cap=cv2.VideoCapture("demo.mp4") 


while True:
    ret, frame=cap.read() 

    if not ret:
        print("Unable to play video")
        break
    
    results=model_yolo(frame) 
    detections=results[0].boxes 

    for box  in detections: 
        class_id=int(box.cls[0]) 
        name=model_yolo.names[class_id] 

        if name not in cache: 
            cache[name]=ask_gemini(name) 
            with open("cache.json","w") as f: 
                json.dump(cache,f)
            time.sleep(4)
        
        decision=cache[name] 
        if decision == "dangerous": 
            color=(0,0,255) 
        else:
            color=(0,225,0) 

        x1, y1, x2, y2=map(int,box.xyxy[0])   
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        cv2.putText(frame, f"{name} - {decision}",(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Result",frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break;

cap.release()
cv2.destroyAllWindows()





