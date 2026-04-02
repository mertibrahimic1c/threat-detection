# Threat-detection

## About
This system analyzes video footage in real-time to detect objects and determine whether they are dangerous or safe. Dangerous objects such as knives and scissors are highlighted with a red bounding box, while safe objects like books and cups are marked in green.

The goal is to provide an automated security layer that can be integrated into surveillance systems — for example, detecting dangerous objects in schools, kindergartens, or public areas without requiring manual monitoring.

To minimize API usage, classification results are cached locally. Each unique object is sent to Gemini AI only once, and future detections reuse the stored result — reducing both cost and response time.
 
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
