"""Plant disease labels, descriptions, and localized UI copy."""

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
