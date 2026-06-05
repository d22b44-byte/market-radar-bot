import os
import requests
from openai import OpenAI

# سحب المتغيرات السرية بأمان من سيرفر Railway
API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not API_KEY:
    raise ValueError("⚠️ خطأ: لم يتم العثور على مفتاح OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def send_to_telegram(message):
    """دالة مخصصة لإرسال التقرير مباشرة إلى حسابك في تليجرام"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ تحذير: إعدادات التليجرام غير مكتملة في الـ Variables، سيتم الطباعة في السيرفر فقط.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ تم إرسال تقرير رادار السوق إلى تليجرام بنجاح!")
        else:
            print(f"❌ فشل إرسال التليجرام. كود الخطأ: {response.status_code}")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاتصال بالتليجرام: {str(e)}")

def analyze_market_data(raw_data):
    system_instruction = (
        "أنت خبير محترف ومحلل بيانات متقدم في أبحاث السوق والمشاريع الناشئة (SaaS). "
        "مهمتك هي تحليل البيانات الخام واستخراج أفضل 10 خدمات رقمية عليها أعلى نسبة طلب. "
        "ركز على الخدمات التي يمكن أتمتتها بالكامل عبر بوت ذكاء اصطناعي دون تدخل بشري. "
        "نظم التقرير في نقاط تفصيلية واضحة تشمل: اسم الخدمة، نسبة الطلب، وسهولة الأتمتة من 10 مع السبب، والتوصية الاستراتيجية."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"إليك البيانات الخام للتحليل الشامل:\n\n{raw_data}"}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"حدث خطأ في الـ API: {str(e)}"

sample_scraped_data = """
- تغريدة 1: يا جماعة أبي أحد يترجم لي هذا الملف الإنجليزي لغة عربية احترافية بدون ترجمة جوجل ركيكة، ضروري اليوم.
- مستخدم في مستقل: مطلوب كاتب محتوى يجهز لي خطة تسويقية وتغريدات وسكريبتات تيك توك لمتجر عطور بشكل أسبوعي.
- تغريدة 2: كيف أقدر أعبي نموذج الجوازات الجديد حق التابعين؟ كل شوية يطلع لي خطأ وأنا أعبي البيانات يدوياً.
- تعليق تيك توك: أنا عندي اجتماع زوم ساعتين وأبي أحد يفرغه لي ويفرز لي النقاط المهمة لأن ما عندي وقت أسمعه كله.
- تغريدة 3: مطلوب مصمم لوقو (شعار) سريع وبسيط لمقهى جديد، الميزانية محدودة والتسليم فوري.
- مستخدم في خمسات: أبحث عن شخص يعدل لي السيرة الذاتية حقتي لتتوافق مع نظام الـ ATS للشركات الكبيرة.
- تغريدة 4: كيف أصيغ عقد اتفاقية عدم إفصاح (NDA) بيني وبين مبرمج شغال معي عن بعد؟ أبي صيغة جاهزة ومنظمة.
"""

if __name__ == "__main__":
    print("⏳ جاري تحليل السوق واكتشاف الفرص بالذكاء الاصطناعي...")
    market_report = analyze_market_data(sample_scraped_data)
    
    # تنسيق الرسالة النهائية للتليجرام
    final_message = (
        "📈 *تقرير رادار السوق الاحترافي (أفضل 10 فرص)* 📈\n\n"
        f"{market_report}"
    )
    
    # إرسال التقرير فوراً لجوالك
    send_to_telegram(final_message)
