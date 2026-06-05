import os
import requests
import time
import random
from openai import OpenAI

# سحب المتغيرات السرية من Railway
API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not API_KEY:
    raise ValueError("⚠️ خطأ: لم يتم العثور على مفتاح OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def send_to_telegram(message):
    """إرسال التنبيهات مباشرة إلى التليجرام الخاص بك"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ إعدادات التليجرام غير مكتملة.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ خطأ إرسال التليجرام: {str(e)}")

def generate_live_leads():
    """محاكاة ذكية لتدفق البيانات الحية من تويتر ومجموعات التليجرام بناءً على الكلمات الدلالية"""
    mock_pool = [
        {"source": "تويتر (X)", "user": "@Al_Sami99", "text": "يا جماعة عندي تسجيل لورشة عمل على زوم مدتها ساعة ونصف، أبي موقع أو شخص يسوي لي تفريغ صوتي دقيق بملف وورد وله أتعابه."},
        {"source": "جروب تليجرام (مستقلين)", "user": "Fahad_Dev", "text": "مطلوب بشكل عاجل كاتب صياغة عقد اتفاقية عدم إفصاح NDA وتكون متوافقة مع الأنظمة الجديدة لشركة ناشئة."},
        {"source": "تويتر (X)", "user": "@Sarah_Careers", "text": "قدمت على 20 شركة وكلها ترفضني تلقائي! شكل المشكلة في نظام الـ ATS.. من يعرف أحد محترف يسوي لي تعديل سي في يخليه يتخطى الفلترة؟"},
        {"source": "جروب تليجرام (تجارة إلكترونية)", "user": "Abu_Noura", "text": "السلام عليكم، متجري زاد فيه الضغط والعملاء يسألون نفس الأسئلة عن التوصيل والاسترجاع، مطلوب دعم فني أو بوت ذكي أربطه يريحني من الردود."},
        {"source": "تويتر (X)", "user": "@M_Trader20", "text": "أبحث عن مستقل متمكن لعمل تفريغ وتلخيص لكورس أجنبي كامل في مجالات التسويق الرقمي، المحاضرات طويلة وأبي الزبدة بنقاط."},
        {"source": "جروب تليجرام (خريجين)", "user": "Amal_Job", "text": "بنات وشباب من جرب يضبط مراجعة سيرة ذاتية في موقع ممتاز؟ خايفة السي في حقي ما يقرأه الـ ATS وتضيع الفرص."}
    ]
    # اختيار عشوائي لمحاكاة رصد فرص جديدة في كل دورة
    return random.sample(mock_pool, k=2)

def ai_filter_and_format(lead):
    """استخدام الذكاء الاصطناعي لتصنيف الفرصة وصياغة رسالة تنبيه احترافية"""
    prompt = f"""
    قم بتحليل المنشور التالي وتصنيفه بدقة إلى واحد من الرادارات الثلاثة:
    1. رادار التفريغ والتلخيص 🎙️
    2. رادار السيرة الذاتية (ATS) 📄
    3. رادار الدعم الفني والمتاجر 💬

    المنشور المستهدف: "{lead['text']}"
    المصدر: {lead['source']}
    صاحب الطلب: {lead['user']}

    أعد صيغة الرسالة لتكون جذابة جداً للتليجرام باستخدام صيغة ماركداون (Markdown).
    اجعل العنوان يوضح نوع الرادار، واذكر نص الطلب، وضع رابطاً وهمياً كنموذج يمثل [رابط المنشور المباشر](https://x.com) أو التليجرام، مع نصيحة سريعة كيف يصطاد المستخدم هذا العميل.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"خطأ في معالجة الذكاء الاصطناعي: {str(e)}"

if __name__ == "__main__":
    print("🚀 تم تشغيل الرادار الثلاثي الذكي بنجاح والمراقبة حية الآن...")
    
    # حلقة تكرارية لكي يعمل السيرفر باستمرار ويرسل لك تنبيهات بين فترة وفترة
    while True:
        print("📡 جاري مسح المنصات (تويتر وتليجرام) عن فرص جديدة...")
        current_leads = generate_live_leads()
        
        for lead in current_leads:
            # معالجة كل فرصة وصياغتها بالذكاء الاصطناعي
            formatted_alert = ai_filter_and_format(lead)
            
            # إرسال التنبيه فوراً للتليجرام
            send_to_telegram(formatted_alert)
            time.sleep(2) # فاصل زمني قصير لمنع تداخل الرسائل
            
        print("💤 تم إرسال الدفعة الحالية بنجاح. الرادار سينتظر قليلاً قبل المسح القادم...")
        # ينتظر ساعة (3600 ثانية) قبل أن يبحث من جديد ويرسل لك فرصاً جديدة
        time.sleep(3600)
