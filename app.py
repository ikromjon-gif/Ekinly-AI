# ===================================================
# Ekinly AI — Plant Disease Detection
# Author: Tojiboev Ikromjon Makhkamboy Ugli
# Copyright (c) 2026. All rights reserved.
# ===================================================
#╔══════════════════════════════════════════════════════════════════╗
#║  🌱 Ekinly AI — Plant Disease Detection System                  ║
#║  ═══════════════════════════════════════════════════════════════ ║
#║  Author:      Tojiboev Ikromjon Makhkamboy Ugli                 ║
#║  Copyright:   © 2026 Tojiboev Ikromjon. All rights reserved.    ║
#║  License:     All rights reserved - See LICENSE file            ║
#║  Thesis:      Chonnam National University                       ║
#║  Department:  Computer Engineering                              ║
#╚══════════════════════════════════════════════════════════════════╝
#"""

import gradio as gr
import numpy as np
from PIL import Image, ImageEnhance
import os
import base64
import google.generativeai as genai
import json
from datetime import datetime
from tensorflow.keras.applications.efficientnet import preprocess_input

# ==================== JSON MA'LUMOTLAR BAZASI ====================
DATA_FILE = "diseases_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"predictions": [], "next_id": 1}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_disease_prediction(disease_name, confidence, plant_type, latitude=None, longitude=None):
    data = load_data()
    new_prediction = {
        "id": data["next_id"],
        "disease_name": disease_name,
        "confidence": confidence,
        "latitude": latitude,
        "longitude": longitude,
        "plant_type": plant_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["predictions"].append(new_prediction)
    data["next_id"] += 1
    save_data(data)
    print(f"✅ Ma'lumot saqlandi! ID: {new_prediction['id']}")
    return new_prediction["id"]

def get_disease_history(limit=50):
    data = load_data()
    predictions = sorted(data["predictions"], key=lambda x: x["timestamp"], reverse=True)
    return predictions[:limit]

def get_statistics():
    data = load_data()
    predictions = data["predictions"]
    if not predictions:
        return {"total": 0, "by_disease": {}, "by_plant": {}}
    by_disease = {}
    by_plant = {}
    for p in predictions:
        disease = p["disease_name"]
        plant = p["plant_type"]
        by_disease[disease] = by_disease.get(disease, 0) + 1
        by_plant[plant] = by_plant.get(plant, 0) + 1
    return {"total": len(predictions), "by_disease": by_disease, "by_plant": by_plant}

def get_disease_locations():
    data = load_data()
    locations = []
    for p in data["predictions"]:
        if p.get("latitude") and p.get("longitude"):
            locations.append({
                "latitude": p["latitude"],
                "longitude": p["longitude"],
                "disease_name": p["disease_name"],
                "confidence": p["confidence"],
                "plant_type": p["plant_type"],
                "timestamp": p["timestamp"]
            })
    return locations

def get_disease_list_html():
    history = get_disease_history(limit=20)
    if not history:
        return "<p>No disease reports yet.</p>"
    html = '<div style="max-height: 300px; overflow-y: auto;"><table style="width:100%; border-collapse: collapse;"><tr style="background:#2c5e2e; color:white;"><th style="padding:8px;">Disease</th><th style="padding:8px;">Confidence</th><th style="padding:8px;">Time</th></tr>'
    for p in history[:20]:
        html += f'<tr style="border-bottom:1px solid #ddd;"><td style="padding:8px;">{p["disease_name"]}</td><td style="padding:8px;">{p["confidence"]}%</td><td style="padding:8px;">{p["timestamp"][:16]}</td></tr>'
    html += '</table></div>'
    return html
# ==================== OPENCV ====================
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# ==================== TENSORFLOW ====================
print("🔧 Loading TensorFlow...")
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TENSORFLOW_OK = True
except Exception as e:
    print(f"❌ TensorFlow error: {e}")
    TENSORFLOW_OK = False

# ==================== MODEL ====================
MODEL_FILE = "proposed_hybrid_finetuned_final.keras"
MODEL_LOADED = False
model = None

if TENSORFLOW_OK and os.path.exists(MODEL_FILE):
    try:
        model = load_model(MODEL_FILE, compile=False)
        MODEL_LOADED = True
        print(f"✅ Model loaded!")
    except Exception as e:
        print(f"❌ Model error: {e}")
else:
    print(f"❌ Model file not found: {MODEL_FILE}")

# ==================== GEMINI (XAVFSIZ VERSIYA) ====================
print("🔧 Loading Gemini...")
GEMINI_OK = False
gemini_model = None

try:
    # Faqat environment o'zgaruvchisidan olish
    API_KEY = os.environ.get("GEMINI_API_KEY")
    
    if not API_KEY:
        print("⚠️ GEMINI_API_KEY not found!")
        print("   Please add it in: Hugging Face Space -> Settings -> Repository secrets")
        print("   Name: GEMINI_API_KEY")
        print("   Value: Your Google API key")
        GEMINI_OK = False
    else:
        genai.configure(api_key=API_KEY)
        gemini_model = genai.GenerativeModel('models/gemini-2.0-flash')
        GEMINI_OK = True
        print("✅ Gemini loaded successfully!")
        
except Exception as e:
    print(f"❌ Gemini error: {e}")
    GEMINI_OK = False
    gemini_model = None

# ==================== LOGO ====================
def get_logo_base64():
    logo_paths = ["logo.png", "static/logo.png"]
    for path in logo_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

LOGO_BASE64 = get_logo_base64()
LOGO_HTML = '<div style="font-size:50px; text-align:center;">🌿</div>'
if LOGO_BASE64:
    LOGO_HTML = f'<img src="data:image/png;base64,{LOGO_BASE64}" style="width:80px; display:block; margin:0 auto 10px auto;">'

# ==================== RASMNI QAYTA ISHLASH ====================
def enhance_image(image):
    try:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        return image
    except:
        return image

def preprocess_image(image):
    enhanced = enhance_image(image)
    resized = enhanced.resize((224, 224))
    return resized

# ==================== TARJIMA ====================
TRANSLATIONS = {
    "Apple": {"english": "Apple", "korean": "사과", "uzbek": "Olma"},
    "Grape": {"english": "Grape", "korean": "포도", "uzbek": "Uzum"},
    "Tomato": {"english": "Tomato", "korean": "토마토", "uzbek": "Pomidor"},
    "Pepper bell": {"english": "Pepper bell", "korean": "고추", "uzbek": "Qalampir"},
    "healthy": {"english": "healthy", "korean": "건강함", "uzbek": "sog'lom"},
}

def translate_text(text, lang):
    if lang == "english":
        return text
    words = text.split(" - ")
    if len(words) == 2:
        plant, disease = words[0], words[1]
        for key, trans in TRANSLATIONS.items():
            if key.lower() in plant.lower():
                plant = trans.get(lang, plant)
                break
        return f"{plant} - {disease}"
    return text

def translate_description(desc, lang):
    if lang == "english":
        return desc
    trans_dict = {
        "🍇 Black lesions on grape leaves.": {"korean": "🍇 포도 잎에 검은 병변.", "uzbek": "🍇 Uzum barglarida qora yaralar."},
        "🍅 Dark leaf spots on tomato.": {"korean": "🍅 토마토 잎에 어두운 반점.", "uzbek": "🍅 Pomidor barglarida qora dog'lar."},
        "🍅 Target-like spots on tomato.": {"korean": "🍅 토마토에 표적 같은 반점.", "uzbek": "🍅 Pomidorda nishonga o'xshash dog'lar."},
        "🫑 Dark spots on pepper leaves.": {"korean": "🫑 고추 잎에 어두운 반점.", "uzbek": "🫑 Qalampir barglarida qora dog'lar."},
    }
    if desc in trans_dict:
        return trans_dict[desc].get(lang, desc)
    return desc

# ==================== 3 TIL MATNLARI ====================
TEXTS = {
    "english": {
        "title": "🌱 Ekinly AI",
        "developed_by": "Developed by: Tojiboev Ikromjon Makhkamboy Ugli",
        "master": "Master Student – Computer Engineering, Chonnam National University",
        "plant_leaf": "🌿 Upload Leaf Image",
        "detect_btn": "🔍 Detect Disease",
        "clear_btn": "🗑 Clear",
        "upload_rules": "📸 Image Upload Guidelines:",
        "rule1": "• Leaf should be clearly visible in the center",
        "rule2": "• Disease symptoms should be close and clear",
        "rule3": "• Avoid dark or blurry images",
        "rule4": "• Capture a single leaf",
        "auto_leaf_note": "✨ AI will analyze the leaf for diseases",
        "supported_title": "📋 Supported Plants",
        "supported_text": "🍎 Apple | 🫐 Blueberry | 🍒 Cherry | 🌽 Corn | 🍇 Grape | 🍊 Orange | 🍑 Peach | 🫑 Pepper | 🥔 Potato | 🍇 Raspberry | 🫘 Soybean | 🎃 Squash | 🍓 Strawberry | 🍅 Tomato",
        "welcome_title": "Welcome to Ekinly AI",
        "welcome_text": "Upload a leaf image to get started",
        "click_text": "Click 'Detect Disease' to analyze",
        "diagnosis_title": "🔬 Diagnosis Results",
        "top_results": "Top 3 disease predictions with confidence scores",
        "ai_doctor": "👨‍⚕️ AI Doctor's Advice",
        "accuracy_text": "🌿 Model accuracy: 98.90%",
        "footer": "Chonnam National University",
        "error_model_title": "⚠️ Model Not Loaded",
        "error_model_text": "Please check proposed_hybrid_finetuned_final.keras",
        "error_general": "❌ Error",
        "advice_unavailable": "⚠️ AI assistant unavailable",
        "advice_error": "⚠️ Could not get AI advice",
        "model_ready": "✅ Model Ready",
        "model_not_ready": "❌ Model Not Loaded",
        "gemini_active": "🤖 Gemini AI Active",
        "gemini_inactive": "🤖 Gemini AI Inactive",
        "gps_button": "📍 Share My Location",
        "gps_status": "📍 Click 'Share My Location' to enable GPS"
    },
    "korean": {
        "title": "🌱 에킨리 AI",
        "developed_by": "개발자: Tojiboev Ikromjon",
        "master": "석사 과정 – 컴퓨터공학과, 전남대학교",
        "plant_leaf": "🌿 잎 이미지 업로드",
        "detect_btn": "🔍 질병 진단",
        "clear_btn": "🗑 초기화",
        "upload_rules": "📸 이미지 업로드 가이드:",
        "rule1": "• 잎이 중앙에 명확하게",
        "rule2": "• 질병 증상이 선명하게",
        "rule3": "• 어둡거나 흐릿한 이미지 피함",
        "rule4": "• 하나의 잎만 촬영",
        "auto_leaf_note": "✨ AI가 질병을 분석합니다",
        "supported_title": "📋 지원 식물",
        "supported_text": "🍎 사과 | 🫐 블루베리 | 🍒 체리 | 🌽 옥수수 | 🍇 포도 | 🍊 오렌지 | 🍑 복숭아 | 🫑 고추 | 🥔 감자 | 🍇 라즈베리 | 🫘 대두 | 🎃 호박 | 🍓 딸기 | 🍅 토마토",
        "welcome_title": "에킨리 AI 식물 질병 진단",
        "welcome_text": "잎 이미지를 업로드하세요",
        "click_text": "'질병 진단' 클릭",
        "diagnosis_title": "🔬 진단 결과",
        "top_results": "상위 3개 질병 예측",
        "ai_doctor": "👨‍⚕️ AI 의사 조언",
        "accuracy_text": "🌿 모델 정확도: 98.90%",
        "footer": "전남대학교",
        "error_model_title": "⚠️ 모델 없음",
        "error_model_text": "파일 확인",
        "error_general": "❌ 오류",
        "advice_unavailable": "⚠️ AI 사용 불가",
        "advice_error": "⚠️ 조언 없음",
        "model_ready": "✅ 모델 준비됨",
        "model_not_ready": "❌ 모델 없음",
        "gemini_active": "🤖 Gemini AI 활성화",
        "gemini_inactive": "🤖 Gemini AI 비활성화",
        "gps_button": "📍 내 위치 공유",
        "gps_status": "📍 '내 위치 공유' 버튼을 클릭하세요"
    },
    "uzbek": {
        "title": "🌱 Ekinly AI",
        "developed_by": "Ishlab chiquvchi: Tojiboev Ikromjon",
        "master": "Magistr – Kompyuter injiniringi, Chonnam Milliy Universiteti",
        "plant_leaf": "🌿 Barg rasmini yuklash",
        "detect_btn": "🔍 Kasallikni aniqlash",
        "clear_btn": "🗑 Tozalash",
        "upload_rules": "📸 Rasm yuklash qoidalari:",
        "rule1": "• Barg aniq ko'rinishi kerak",
        "rule2": "• Kasallik joyi yaqin bo'lsin",
        "rule3": "• Qorong'i yoki xira bo'lmasin",
        "rule4": "• Bitta bargni suratga oling",
        "auto_leaf_note": "✨ AI kasalliklarni tahlil qiladi",
        "supported_title": "📋 Qo'llab-quvvatlanadigan o'simliklar",
        "supported_text": "🍎 Olma | 🫐 Ko'k meva | 🍒 Gilos | 🌽 Makkajo'xori | 🍇 Uzum | 🍊 Apelsin | 🍑 Shaftoli | 🫑 Qalampir | 🥔 Kartoshka | 🍇 Malina | 🫘 Soya | 🎃 Qovoq | 🍓 Qulupnay | 🍅 Pomidor",
        "welcome_title": "Ekinly AI — O'simlik Kasalliklarini Aniqlash",
        "welcome_text": "Barg rasmini yuklang",
        "click_text": "Aniqlash tugmasini bosing",
        "diagnosis_title": "🔬 Aniqlash natijalari",
        "top_results": "Eng yuqori 3 ta kasallik",
        "ai_doctor": "👨‍⚕️ AI Shifokor maslahati",
        "accuracy_text": "🌿 Model aniqligi: 98.90%",
        "footer": "Chonnam Milliy Universiteti",
        "error_model_title": "⚠️ Model yuklanmadi",
        "error_model_text": "Faylni tekshiring",
        "error_general": "❌ Xatolik",
        "advice_unavailable": "⚠️ AI yordamchi ishlamayapti",
        "advice_error": "⚠️ Maslahat olinmadi",
        "model_ready": "✅ Model tayyor",
        "model_not_ready": "❌ Model yo'q",
        "gemini_active": "🤖 Gemini AI faol",
        "gemini_inactive": "🤖 Gemini AI faol emas",
        "gps_button": "📍 Joylashuvimni ulashish",
        "gps_status": "📍 GPS ni yoqish uchun tugmani bosing"
    }
}

# ==================== KLASSLAR ====================
class_names = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry___Powdery_mildew", "Cherry___healthy",
    "Corn___Cercospora_leaf_spot", "Corn___Common_rust", "Corn___Northern_Leaf_Blight", "Corn___healthy",
    "Grape___Black_rot", "Grape___Esca", "Grape___Leaf_blight", "Grape___healthy",
    "Orange___Haunglongbing", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper_bell___Bacterial_spot", "Pepper_bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
    "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
]

def get_pretty_name(class_name):
    return class_name.replace("___", " - ").replace("_", " ")

descriptions = {
    "Apple___Apple_scab": "🍎 Fungal disease causing dark scabby lesions on apple leaves.",
    "Apple___Black_rot": "🍎 Fungal disease causing black rot on apple leaves.",
    "Apple___Cedar_apple_rust": "🍎 Fungal disease causing orange spots on apple leaves.",
    "Apple___healthy": "🍎 The apple leaf appears healthy.",
    "Blueberry___healthy": "🫐 Blueberry leaf appears healthy.",
    "Cherry___Powdery_mildew": "🍒 White powdery fungus on cherry leaves.",
    "Cherry___healthy": "🍒 Cherry leaf appears healthy.",
    "Corn___Cercospora_leaf_spot": "🌽 Gray leaf spots on corn.",
    "Corn___Common_rust": "🌽 Reddish pustules on corn leaves.",
    "Corn___Northern_Leaf_Blight": "🌽 Long gray lesions on corn leaves.",
    "Corn___healthy": "🌽 Corn leaf appears healthy.",
    "Grape___Black_rot": "🍇 Black lesions on grape leaves.",
    "Grape___Esca": "🍇 Trunk disease affecting grape plants.",
    "Grape___Leaf_blight": "🍇 Leaf blight on grapes.",
    "Grape___healthy": "🍇 Grape leaf appears healthy.",
    "Orange___Haunglongbing": "🍊 Citrus greening disease.",
    "Peach___Bacterial_spot": "🍑 Dark spots on peach leaves.",
    "Peach___healthy": "🍑 Peach leaf appears healthy.",
    "Pepper_bell___Bacterial_spot": "🫑 Dark spots on pepper leaves.",
    "Pepper_bell___healthy": "🫑 Pepper leaf appears healthy.",
    "Potato___Early_blight": "🥔 Dark concentric rings on leaves.",
    "Potato___Late_blight": "🥔 Leaf decay and rot on potato.",
    "Potato___healthy": "🥔 Potato leaf appears healthy.",
    "Raspberry___healthy": "🍇 Raspberry leaf appears healthy.",
    "Soybean___healthy": "🫘 Soybean leaf appears healthy.",
    "Squash___Powdery_mildew": "🎃 White powdery growth on squash.",
    "Strawberry___Leaf_scorch": "🍓 Red spots on strawberry leaves.",
    "Strawberry___healthy": "🍓 Strawberry leaf appears healthy.",
    "Tomato___Bacterial_spot": "🍅 Dark leaf spots on tomato.",
    "Tomato___Early_blight": "🍅 Brown concentric rings on leaves.",
    "Tomato___Late_blight": "🍅 Dark lesions on tomato leaves.",
    "Tomato___Leaf_Mold": "🍅 Yellow patches on tomato leaves.",
    "Tomato___Septoria_leaf_spot": "🍅 Small circular spots on tomato.",
    "Tomato___Spider_mites": "🍅 Yellow speckled leaves from mites.",
    "Tomato___Target_Spot": "🍅 Target-like spots on tomato.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "🍅 Leaf curl and yellowing.",
    "Tomato___Tomato_mosaic_virus": "🍅 Mosaic pattern on tomato leaves.",
    "Tomato___healthy": "🍅 Tomato leaf appears healthy."
}

# ==================== GEMINI MASLAHAT ====================
def get_disease_advice(disease_name, lang):
    t = TEXTS[lang]
    if not GEMINI_OK or gemini_model is None:
        return t["advice_unavailable"]
    lang_prompt = {"english": "Answer in English.", "korean": "Answer in Korean.", "uzbek": "Answer in Uzbek."}
    prompt = f"Agricultural expert: Plant disease is {disease_name}\n{lang_prompt[lang]}\n\nShort advice:"
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except:
        return t["advice_error"]

# ==================== PREDICT ====================
def predict(image, language):
    t = TEXTS[language]
    
    if image is None:
        return f'<div style="text-align:center;padding:50px;background:linear-gradient(135deg,#f5f7fa,#c3cfe2);border-radius:20px;"><div style="font-size:60px;">🌿</div><h2>{t["welcome_title"]}</h2><p>{t["welcome_text"]}</p><p>{t["click_text"]}</p></div>'
    
    if not MODEL_LOADED:
        return f'<div style="text-align:center;padding:50px;background:#fee;"><h2>{t["error_model_title"]}</h2><p>{t["error_model_text"]}</p></div>'
    
    try:
        processed = preprocess_image(image)
        arr = np.array(processed)
        arr = preprocess_input(arr)
        arr = np.expand_dims(arr, axis=0)
        pred = model.predict(arr, verbose=0)[0]
        top3 = pred.argsort()[-3:][::-1]
        
        results = []
        for idx in top3:
            eng_name = get_pretty_name(class_names[idx])
            results.append({
                "name": translate_text(eng_name, language),
                "prob": round(pred[idx] * 100, 2),
                "desc": translate_description(descriptions[class_names[idx]], language)
            })
        
        # Ma'lumotlarni saqlash
        try:
            top_disease_name = results[0]["name"]
            plant_type = top_disease_name.split(" - ")[0] if " - " in top_disease_name else top_disease_name
            save_disease_prediction(
                disease_name=top_disease_name,
                confidence=results[0]["prob"],
                plant_type=plant_type,
                latitude=None,
                longitude=None
            )
        except Exception as e:
            print(f"⚠️ Ma'lumot saqlashda xatolik: {e}")
        
        advice = get_disease_advice(results[0]["name"], language)
        colors = ["#4caf50", "#ff9800", "#f44336"]
        icons = ["🥇", "🥈", "🥉"]
        
        html = f'<div style="background:#f0f7f0;padding:25px;border-radius:20px;">'
        html += f'<div style="text-align:center;"><div style="font-size:50px;">🔬</div><h2>{t["diagnosis_title"]}</h2><p>{t["top_results"]}</p></div>'
        
        for i, r in enumerate(results):
            html += f'<div style="background:white;border-radius:15px;padding:15px;margin:10px 0;border-left:5px solid {colors[i]};">'
            html += f'<div><span style="font-size:24px;">{icons[i]}</span> <strong>{r["name"]}</strong> <span style="background:{colors[i]};color:white;padding:2px 10px;border-radius:20px;float:right;">{r["prob"]}%</span></div>'
            html += f'<div style="background:#ddd;height:10px;margin:10px 0;"><div style="background:{colors[i]};width:{r["prob"]}%;height:10px;"></div></div>'
            html += f'<p style="font-size:13px;">📝 {r["desc"]}</p></div>'
        
        html += f'<div style="background:linear-gradient(135deg,#1a5f7a,#0d3b4f);border-radius:15px;padding:20px;color:white;margin-top:15px;"><h3>👨‍⚕️ {t["ai_doctor"]}</h3><div>{advice.replace(chr(10),"<br>")}</div></div>'
        html += f'<div style="text-align:center;margin-top:15px;"><p>{t["accuracy_text"]}</p></div></div>'
        
        return html
        
    except Exception as e:
        return f'<div style="text-align:center;padding:50px;background:#fee;"><h2>{t["error_general"]}</h2><p>{str(e)}</p></div>'

# ==================== UI FUNKSIYALARI ====================
def get_status_html(lang):
    t = TEXTS[lang]
    status = t["model_ready"] if MODEL_LOADED else t["model_not_ready"]
    gemini = t["gemini_active"] if GEMINI_OK else t["gemini_inactive"]
    color = "#4caf50" if MODEL_LOADED else "#f44336"
    return f'<div style="background:{color};padding:8px;border-radius:10px;text-align:center;color:white;">{status} | {gemini}</div>'

def get_header_html(lang):
    t = TEXTS[lang]
    return f'<div style="text-align:center;padding:20px 0;">{LOGO_HTML}<h1>{t["title"]}</h1><p>{t["developed_by"]}<br>{t["master"]}</p>{get_status_html(lang)}</div>'

def get_upload_rules_html(lang):
    t = TEXTS[lang]
    return f'<div style="background:#fff8e1;padding:15px;border-radius:10px;margin:15px 0;"><h4>{t["upload_rules"]}</h4><p>{t["rule1"]}</p><p>{t["rule2"]}</p><p>{t["rule3"]}</p><p>{t["rule4"]}</p><p>✨ {t["auto_leaf_note"]}</p></div>'

def get_supported_html(lang):
    t = TEXTS[lang]
    return f'<div style="background:#e8f5e9;padding:12px;border-radius:10px;margin-bottom:15px;"><h4>{t["supported_title"]}</h4><p>{t["supported_text"]}</p></div>'

def get_welcome_html(lang):
    t = TEXTS[lang]
    return f'<div style="text-align:center;padding:50px;background:linear-gradient(135deg,#f5f7fa,#c3cfe2);border-radius:20px;"><div style="font-size:60px;">🌿</div><h2>{t["welcome_title"]}</h2><p>{t["welcome_text"]}</p><p>{t["click_text"]}</p></div>'

def get_footer_html(lang):
    t = TEXTS[lang]
    return f'<hr><div style="text-align:center;padding:15px;color:#888;"><p>{t["accuracy_text"]}</p><p>{t["footer"]}</p></div>'

# ==================== GPS JAVASCRIPT ====================
GPS_JAVASCRIPT = """
<script>
function getLocation() {
    const statusDiv = document.getElementById('location-status');
    if (statusDiv) statusDiv.innerHTML = '<div style="text-align:center;padding:10px;">📍 Getting your location...</div>';
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                if (statusDiv) statusDiv.innerHTML = '<div style="text-align:center;padding:10px;color:green;">✅ Location: ' + lat.toFixed(4) + ', ' + lng.toFixed(4) + '</div>';
            },
            (error) => {
                let msg = "❌ Could not get location";
                if (error.code === 1) msg = "❌ Location permission denied";
                else if (error.code === 2) msg = "❌ Location unavailable";
                else if (error.code === 3) msg = "❌ Location timeout";
                if (statusDiv) statusDiv.innerHTML = '<div style="text-align:center;padding:10px;color:red;">' + msg + '</div>';
            }
        );
    } else {
        if (statusDiv) statusDiv.innerHTML = '<div style="text-align:center;padding:10px;color:red;">❌ Geolocation not supported</div>';
    }
}
</script>
"""

# ==================== GRADIO UI ====================
with gr.Blocks(title="🌱 Ekinly AI", theme=gr.themes.Soft(primary_hue="green")) as demo:
    current_lang = gr.State("english")
    
    header = gr.HTML(get_header_html("english"))
    
    with gr.Row():
        eng_btn = gr.Button("🇬🇧 English", variant="primary")
        kor_btn = gr.Button("🇰🇷 한국어", variant="secondary")
        uzb_btn = gr.Button("🇺🇿 O'zbek", variant="secondary")
    
    with gr.Tabs():
        # ========== TAB 1: Detect Disease ==========
        with gr.TabItem("🔍 Detect Disease"):
            supported = gr.HTML(get_supported_html("english"))
            upload_rules = gr.HTML(get_upload_rules_html("english"))
            with gr.Row():
                with gr.Column(scale=1, min_width=500):
                    img_input = gr.Image(type="pil", label="🌿 Upload Leaf Image", height=350)
                    with gr.Row():
                        predict_btn = gr.Button("🔍 Detect Disease", variant="primary", size="lg")
                        clear_btn = gr.Button("🗑 Clear", variant="secondary", size="lg")
                with gr.Column(scale=1, min_width=500):
                    output = gr.HTML(get_welcome_html("english"))
        
        # ========== TAB 2: History & Statistics ==========
        with gr.TabItem("📊 History & Statistics"):
            stats = get_statistics()
            history = get_disease_history(50)
            gr.Markdown(f"""
            <div style="background:#f0f7f0; padding:15px; border-radius:10px; margin-bottom:20px;">
                <h3>📈 Overview</h3>
                <p><strong>Total Predictions:</strong> {stats['total']}</p>
                <p><strong>Different Diseases:</strong> {len(stats['by_disease'])}</p>
                <p><strong>Plant Types:</strong> {len(stats['by_plant'])}</p>
            </div>
            """)
            gr.Markdown("### 📋 By Disease")
            disease_text = ""
            for disease, count in sorted(stats['by_disease'].items(), key=lambda x: x[1], reverse=True):
                disease_text += f"- **{disease}**: {count} time(s)\n"
            gr.Markdown(disease_text)
            gr.Markdown("### 🌱 By Plant Type")
            plant_text = ""
            for plant, count in sorted(stats['by_plant'].items(), key=lambda x: x[1], reverse=True):
                plant_text += f"- **{plant}**: {count} time(s)\n"
            gr.Markdown(plant_text)
            gr.Markdown("## 📋 Recent Disease History")
            if history:
                table_data = [[p['id'], p['disease_name'], f"{p['confidence']}%", p['plant_type'], p['timestamp']] for p in history]
                gr.Dataframe(value=table_data, headers=["ID", "Disease Name", "Confidence", "Plant Type", "Date & Time"], label="Disease History", interactive=False, wrap=True)
            else:
                gr.Markdown("_No predictions yet._")
        
        # ========== TAB 3: Disease Map ==========
        with gr.TabItem("🗺️ Disease Map"):
            gr.Markdown("## 🗺️ Disease Location Map")
            gr.Markdown("Share your location to help track disease spread.")
            location_status = gr.HTML(f'<div id="location-status" style="text-align:center;padding:10px;">{TEXTS["english"]["gps_status"]}</div>')
            with gr.Row():
                location_btn = gr.Button(TEXTS["english"]["gps_button"], variant="primary", size="lg", elem_id="share-location-btn")
            gr.Markdown("### 📋 Recent Disease Reports")
            disease_reports = gr.HTML(get_disease_list_html())
            gr.Markdown("### 📊 Statistics")
            stats2 = get_statistics()
            gr.Markdown(f"""
            <div style="background:#f0f7f0; padding:15px; border-radius:10px;">
                <p><strong>Total Predictions:</strong> {stats2['total']}</p>
                <p><strong>Different Diseases:</strong> {len(stats2['by_disease'])}</p>
                <p><strong>Plant Types:</strong> {len(stats2['by_plant'])}</p>
            </div>
            """)
            gr.Markdown("### 💡 How GPS Works")
            gr.Markdown("""
            1. Click **'Share My Location'** button above
            2. Allow location access when prompted by your browser
            3. Your location will be displayed on screen
            4. Future updates will show disease locations on a map
            """)
            gr.HTML(GPS_JAVASCRIPT)
    
    footer = gr.HTML(get_footer_html("english"))

    # ==================== UPDATE FUNCTIONS (Blocks ichida) ====================
    def update_english():
        lang = "english"
        t = TEXTS[lang]
        return (
            lang,
            get_header_html(lang),
            get_supported_html(lang),
            get_upload_rules_html(lang),
            None,
            t["plant_leaf"],
            t["detect_btn"],
            t["clear_btn"],
            get_welcome_html(lang),
            get_footer_html(lang),
            gr.update(value="🇬🇧 English", variant="primary"),
            gr.update(value="🇰🇷 한국어", variant="secondary"),
            gr.update(value="🇺🇿 O'zbek", variant="secondary")
        )

    def update_korean():
        lang = "korean"
        t = TEXTS[lang]
        return (
            lang,
            get_header_html(lang),
            get_supported_html(lang),
            get_upload_rules_html(lang),
            None,
            t["plant_leaf"],
            t["detect_btn"],
            t["clear_btn"],
            get_welcome_html(lang),
            get_footer_html(lang),
            gr.update(value="🇬🇧 English", variant="secondary"),
            gr.update(value="🇰🇷 한국어", variant="primary"),
            gr.update(value="🇺🇿 O'zbek", variant="secondary")
        )

    def update_uzbek():
        lang = "uzbek"
        t = TEXTS[lang]
        return (
            lang,
            get_header_html(lang),
            get_supported_html(lang),
            get_upload_rules_html(lang),
            None,
            t["plant_leaf"],
            t["detect_btn"],
            t["clear_btn"],
            get_welcome_html(lang),
            get_footer_html(lang),
            gr.update(value="🇬🇧 English", variant="secondary"),
            gr.update(value="🇰🇷 한국어", variant="secondary"),
            gr.update(value="🇺🇿 O'zbek", variant="primary")
        )

    def clear_all(lang):
        t = TEXTS[lang]
        return None, get_welcome_html(lang)

    # ==================== EVENT HANDLERS ====================
    eng_btn.click(
        update_english,
        outputs=[
            current_lang, header, supported, upload_rules,
            img_input, img_input, predict_btn, clear_btn,
            output, footer, eng_btn, kor_btn, uzb_btn
        ]
    )

    kor_btn.click(
        update_korean,
        outputs=[
            current_lang, header, supported, upload_rules,
            img_input, img_input, predict_btn, clear_btn,
            output, footer, eng_btn, kor_btn, uzb_btn
        ]
    )

    uzb_btn.click(
        update_uzbek,
        outputs=[
            current_lang, header, supported, upload_rules,
            img_input, img_input, predict_btn, clear_btn,
            output, footer, eng_btn, kor_btn, uzb_btn
        ]
    )

    predict_btn.click(fn=predict, inputs=[img_input, current_lang], outputs=output)
    clear_btn.click(fn=clear_all, inputs=[current_lang], outputs=[img_input, output])

    # GPS tugmasi uchun JavaScript
    location_btn.click(None, None, None, js="() => { getLocation(); }")

# ==================== LAUNCH ====================
demo.launch()
