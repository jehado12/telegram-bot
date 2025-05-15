from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# توكن البوت
TOKEN = "8048112338:AAH27Cqss8UmdZmkV3TvtGyK1leCYLO7gIc"

# يوزر أو معرف مجموعة الدعم (مع @ أو ID)
SUPPORT_CHAT_ID = "@jehado_sy"  # يمكنك أيضاً استخدام ID المجموعة مثل -1001234567890

# رسالة ترحيبية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    welcome_message = f"""مرحباً {user}!

اهلا بك في الدعم الفني السوري كيفا يمكننا مساعدتك الرجاء اختيار المشكلة الذي تواجهك لمساعدتك على حلها _فريق المساعدة السوري_."""
    keyboard = [
        [InlineKeyboardButton("التحقق منimei الهاتف", callback_data="login_issue")],
        [InlineKeyboardButton("تم حظر الوتساب لدي", callback_data="payment_issue")],
        [InlineKeyboardButton(" ظهور اعلانات بشكل متكرر ", callback_data="order_issue")],
        [InlineKeyboardButton("أخرى", callback_data="other_issue")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# التعامل مع الأزرار
async def handle_issue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    issue_type = query.data

    issue_map = {
        "login_issue": "لا يستطيع تسجيل الدخول",
        "payment_issue": "خطأ في الدفع",
        "order_issue": "ظهور اعلانات بشكل متكرر ",
        "other_issue": "مشكلة أخرى"
    }

    issue_text = issue_map.get(issue_type, "مشكلة غير معروفة")

    await query.edit_message_text(f"تم استلام مشكلتك: \"{issue_text}\"\nسيتم تحويلك إلى الدعم الفني الآن...")

    support_message = f"""
🚨 مستخدم بحاجة للمساعدة:

👤 الاسم: {user.full_name}
🔗 اسم المستخدم: @{user.username if user.username else 'بدون يوزر'}
🆘 المشكلة: {issue_text}
📍 رابط المستخدم: tg://user?id={user.id}
"""

    await context.bot.send_message(chat_id=SUPPORT_CHAT_ID, text=support_message)

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_issue))

    print("✅ البوت يعمل كدعم فني...")
    app.run_polling()