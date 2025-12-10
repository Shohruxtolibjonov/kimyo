import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from docx import Document
from docx.shared import Pt, RGBColor
from io import BytesIO
import os

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokeni va Admin ID
BOT_TOKEN = "8349883706:AAHndp5Ps5NfeBniH0XLIskzbYXTLvEOt5M"
ADMIN_ID = 1365319493

# Conversation holatlar
(FISH, MANZIL, SINF, AVVAL_OQIGAN, OTA_ONA, 
 TELEFON, OTA_ONA_TELEFON, MAQSAD) = range(8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Botni boshlash va foydalanuvchini kutib olish"""
    user = update.effective_user
    
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\n\n"
        "🧪 Kimyo kursimizga yozilishingiz uchun so'rovnomalarga "
        "aniq va to'la javob berishingiz kerak.\n\n"
        "📝 Iltimos, to'liq ismingizni kiriting (F.I.SH):",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Foydalanuvchi ma'lumotlarini saqlash uchun
    context.user_data['user_info'] = {
        'telegram_username': user.username or 'Username yo\'q',
        'telegram_id': user.id
    }
    
    return FISH

async def get_fish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """F.I.SH ni qabul qilish"""
    context.user_data['user_info']['fish'] = update.message.text
    
    await update.message.reply_text(
        "📍 Qaysi tuman, qaysi qishloqdansiz?"
    )
    return MANZIL

async def get_manzil(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Manzilni qabul qilish"""
    context.user_data['user_info']['manzil'] = update.message.text
    
    await update.message.reply_text(
        "🎓 Nechanchi sinfsiz yoki bitirganmisiz?"
    )
    return SINF

async def get_sinf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sinf ma'lumotini qabul qilish"""
    context.user_data['user_info']['sinf'] = update.message.text
    
    keyboard = [['Ha', 'Yo\'q']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "📚 Avval kimyo o'qiganmisiz?",
        reply_markup=reply_markup
    )
    return AVVAL_OQIGAN

async def get_avval_oqigan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Avval o'qigan ma'lumotini qabul qilish"""
    context.user_data['user_info']['avval_oqigan'] = update.message.text
    
    keyboard = [['Ha', 'Yo\'q']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "👨‍👩‍👦 Ota-onangiz bormi?",
        reply_markup=reply_markup
    )
    return OTA_ONA

async def get_ota_ona(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ota-ona ma'lumotini qabul qilish"""
    context.user_data['user_info']['ota_ona'] = update.message.text
    
    await update.message.reply_text(
        "📱 O'zingizning telefon raqamingizni kiriting:\n"
        "(Masalan: +998901234567)",
        reply_markup=ReplyKeyboardRemove()
    )
    return TELEFON

async def get_telefon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Telefon raqamni qabul qilish"""
    context.user_data['user_info']['telefon'] = update.message.text
    
    await update.message.reply_text(
        "📞 Ota-onangizning telefon raqamini kiriting:\n"
        "(Masalan: +998901234567)"
    )
    return OTA_ONA_TELEFON

async def get_ota_ona_telefon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ota-ona telefon raqamini qabul qilish"""
    context.user_data['user_info']['ota_ona_telefon'] = update.message.text
    
    await update.message.reply_text(
        "🎯 Kimyo o'qishdan maqsadingiz nima?"
    )
    return MAQSAD

async def get_maqsad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maqsadni qabul qilish va ma'lumotlarni adminga yuborish"""
    context.user_data['user_info']['maqsad'] = update.message.text
    user_info = context.user_data['user_info']
    
    # Word hujjat yaratish
    doc = Document()
    
    # Sarlavha
    title = doc.add_heading('KIMYO KURSI - YANGI TALABA MA\'LUMOTLARI', 0)
    title.alignment = 1  # Center
    
    doc.add_paragraph()
    
    # Ma'lumotlarni qo'shish
    data_pairs = [
        ("👤 F.I.SH:", user_info.get('fish', 'N/A')),
        ("📍 Manzil:", user_info.get('manzil', 'N/A')),
        ("🎓 Sinf:", user_info.get('sinf', 'N/A')),
        ("📚 Avval kimyo o'qiganmi:", user_info.get('avval_oqigan', 'N/A')),
        ("👨‍👩‍👦 Ota-onasi bormi:", user_info.get('ota_ona', 'N/A')),
        ("📱 Telefon raqami:", user_info.get('telefon', 'N/A')),
        ("📞 Ota-ona telefon raqami:", user_info.get('ota_ona_telefon', 'N/A')),
        ("🎯 Maqsadi:", user_info.get('maqsad', 'N/A')),
    ]
    
    for label, value in data_pairs:
        p = doc.add_paragraph()
        p.add_run(label).bold = True
        p.add_run(f" {value}")
    
    doc.add_paragraph()
    doc.add_paragraph("_" * 50)
    
    # Telegram ma'lumotlari
    p = doc.add_paragraph()
    p.add_run("📱 Telegram Username: ").bold = True
    p.add_run(f"@{user_info.get('telegram_username', 'N/A')}")
    
    p = doc.add_paragraph()
    p.add_run("🆔 Telegram ID: ").bold = True
    p.add_run(str(user_info.get('telegram_id', 'N/A')))
    
    # Hujjatni xotiraga saqlash
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    
    # Faylni adminga yuborish
    file_name = f"Ariza_{user_info.get('fish', 'Nomsiz').replace(' ', '_')}.docx"
    
    try:
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=file_stream,
            filename=file_name,
            caption=f"🆕 Yangi ariza keldi!\n\n"
                    f"👤 {user_info.get('fish', 'N/A')}\n"
                    f"📱 @{user_info.get('telegram_username', 'N/A')}"
        )
        
        await update.message.reply_text(
            "✅ Arizangiz muvaffaqiyatli qabul qilindi!\n\n"
            "Ma'lumotlaringiz admin ko'rib chiqish uchun yuborildi. "
            "Tez orada siz bilan bog'lanamiz.\n\n"
            "Rahmat! 🙏"
        )
        
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
        await update.message.reply_text(
            "❌ Arizani yuborishda xatolik yuz berdi. "
            "Iltimos, qaytadan urinib ko'ring yoki admin bilan bog'laning."
        )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """So'rovnomani bekor qilish"""
    await update.message.reply_text(
        "❌ So'rovnoma bekor qilindi.\n"
        "Qayta boshlash uchun /start ni bosing.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Botni ishga tushirish"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fish)],
            MANZIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_manzil)],
            SINF: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sinf)],
            AVVAL_OQIGAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_avval_oqigan)],
            OTA_ONA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ota_ona)],
            TELEFON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_telefon)],
            OTA_ONA_TELEFON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ota_ona_telefon)],
            MAQSAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_maqsad)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    application.add_handler(conv_handler)
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushirildi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()