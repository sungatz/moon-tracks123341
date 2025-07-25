# from marat import godmode()
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

conn = sqlite3.connect("budget.db")  
cursor = conn.cursor()

TOKEN = '8128709962:AAExalXg49hPWk3Gg8aTefRQGmX-VTYNCjc'

async def start(update, context):
    await update.message.reply_text("Интересный факт: Морковки полезные. Мои команды: /products; /delete_product имя, количество; /add_product имя, количество,; /otpravit_sungatu_1000000000000000000_dollars")

async def products(update, context):
    cursor.execute('CREATE table IF NOT EXISTS WE_NEED_MONEY( id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, amount INTEGER)')
    cursor.execute('SELECT * FROM WE_NEED_MONEY')
    zap = cursor.fetchall()
    if not zap:
        await update.message.reply_text("ПРОДУКТОВ Нету")
    else:
        text = "\n".join([f"{row[1]}: {row[2]} шт." for row in zap])
        await update.message.reply_text(text)
async def delete_product(update, context,):
    name = context.args[0]
    amount = int(context.args[1])
    cursor.execute('SELECT amount FROM WE_NEED_MONEY WHERE type = ?', (name,)) 
    literally_me = cursor.fetchone()

    if not literally_me:
        await update.message.reply_text('Такого продукта у нас не имеется')
        return
    
    current_amount = literally_me[0]
    
    new_amt = current_amount - amount
    if new_amt > 0:
        cursor.execute('UPDATE WE_NEED_MONEY SET amount = ? WHERE type = ?', (new_amt, name))
    else:
        cursor.execute('DELETE FROM WE_NEED_MONEY WHERE type = ?', (name,))
    conn.commit()
    await update.message.reply_text(f"Обновлено: {name} теперь {max(new_amt, 0)} шт.")

async def add_product(update, context):
    if len(context.args) < 2:
        await update.message.reply_text("Формат: /add_product имя количество")
        return

    name = context.args[0]
    amount = int(context.args[1])

    cursor.execute('SELECT amount FROM WE_NEED_MONEY WHERE type = ?', (name,))
    result = cursor.fetchone()

    if result:
        new_amt = result[0] + amount
        cursor.execute('UPDATE WE_NEED_MONEY SET amount = ? WHERE type = ?', (new_amt, name))
        await update.message.reply_text(f"Обновлено: {name} теперь {new_amt} шт.")
    else:
        cursor.execute('INSERT INTO WE_NEED_MONEY (type, amount) VALUES (?, ?)', (name, amount))
        await update.message.reply_text(f"Добавлено: {name} — {amount} шт.")

    conn.commit()
async def otpravit_sungatu_1000000000000000000_dollars(update, context):
    await update.message.reply_text("Готово 💸 Деньги ушли Сунгату (в мечтах).")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("products", products))
app.add_handler(CommandHandler("delete_product", delete_product))
app.add_handler(CommandHandler("add_product", add_product))
app.add_handler(CommandHandler("otpravit_sungatu_1000000000000000000_dollars", otpravit_sungatu_1000000000000000000_dollars))
app.run_polling()
