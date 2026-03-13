import os
import json
import asyncio
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)
from core.agent import chat
from core.onboarding import (
    get_onboarding_state, get_current_question,
    process_onboarding_answer, get_welcome_message
)
from memory.memory import (
    init_db, get_memories, get_facts,
    clear_user, save_profile, get_profile,
    get_pending_action, delete_pending_action
)
from skills.skills import get_skill_prompt, get_help_text, get_all_skills

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_db()

    state = get_onboarding_state(user_id)
    if state["done"]:
        await update.message.reply_text(
            "Hey, I'm here. What's going on?",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await update.message.reply_text(
        get_welcome_message(),
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text or ""
    state = get_onboarding_state(user_id)

    if not state["done"]:
        result = process_onboarding_answer(user_id, text)
        if result["done"]:
            agent_name = result.get("agent_name", "Buddy")
            await update.message.reply_text(
                f"Set. I'm *{agent_name}*.\nTalk to me whenever. Send /help to see commands.",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(f"[{result['step']}/{result['total']}] {result['next_question']}")
        return

    # Check for skill triggers
    skill_prompt = None
    all_skills = get_all_skills()
    for skill_name, skill in all_skills.items():
        trigger = skill.get("trigger")
        if trigger and text.startswith(trigger) and not skill.get("system"):
            skill_prompt = get_skill_prompt(trigger)
            text = text[len(trigger):].strip() or f"User triggered {trigger}."
            break

    message = f"[SKILL: {skill_prompt}]\n\n{text}" if skill_prompt else text
    await process_chat_request(update, user_id, message)

async def process_chat_request(update: Update, user_id: str, message: str, confirmed_action: dict = None):
    await update.effective_chat.send_action("typing")
    result = await chat(user_id, message, confirmed_action=confirmed_action)

    if "action_required" in result:
        action_req = result["action_required"]
        action_id = action_req["action_id"]

        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data=f"conf_{action_id}"),
                InlineKeyboardButton("❌ Cancel", callback_data=f"can_{action_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.effective_message.reply_text(
            f"🛡️ *Security Intercept*\n{action_req['display']}",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        reply = result.get("reply", "No response.")
        await update.effective_message.reply_text(reply)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = str(update.effective_user.id)
    
    if data.startswith("conf_"):
        action_id = data[5:]
        pending = get_pending_action(action_id)
        if pending:
            delete_pending_action(action_id)
            await query.edit_message_text(f"✅ Executing: {pending['action']['parameters'].get('command', 'Action')}")
            await process_chat_request(update, user_id, pending["message"], confirmed_action=pending["action"])
        else:
            await query.edit_message_text("❌ Action expired or already processed.")
            
    elif data.startswith("can_"):
        action_id = data[5:]
        delete_pending_action(action_id)
        await query.edit_message_text("❌ Action cancelled.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = bytes(await file.download_as_bytearray())
    
    caption = update.message.caption or "Analyze this image."
    await update.effective_chat.send_action("typing")
    result = await chat(user_id, caption, image_bytes=image_bytes)
    await update.message.reply_text(result.get("reply", "Done."))

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_help_text(), parse_mode="Markdown")

async def cmd_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    facts = get_facts(user_id)
    text = "*Long-Term Context:*\n\n" + "\n".join([f"• {f}" for f in facts[:10]])
    await update.message.reply_text(text, parse_mode="Markdown")

async def cmd_forget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_user(str(update.effective_user.id))
    await update.message.reply_text("Memory wiped.")

async def cmd_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from memory.memory import get_user_tasks
    user_id = str(update.effective_user.id)
    tasks = get_user_tasks(user_id)
    if not tasks:
        await update.message.reply_text("No active tasks.")
        return
    text = "*Strategic Task Board:*\n\n"
    for t in tasks:
        emoji = "⏳" if t['status'] == "pending" else "⚙️" if t['status'] == "running" else "✅" if t['status'] == "completed" else "❌"
        text += f"{emoji} *#{t['id']}*: {t['objective'][:50]}... ({t['status']})\n"
    await update.message.reply_text(text, parse_mode="Markdown")

async def cmd_synthesize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from memory.memory import get_task
    if not context.args:
        await update.message.reply_text("Usage: `/synthesize [task_id]`")
        return
    task_id = context.args[0]
    task = get_task(task_id)
    if not task or not task['result']:
        await update.message.reply_text("Task not found or result not ready.")
        return
    await update.message.reply_text(f"*Result for Task #{task_id}:*\n\n{task['result']}", parse_mode="Markdown")

async def cmd_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        os.environ["MODEL_NAME"] = context.args[0]
        await update.message.reply_text(f"Model: {context.args[0]}")

def run_telegram():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token: raise ValueError("TELEGRAM_BOT_TOKEN missing")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("memory", cmd_memory))
    app.add_handler(CommandHandler("forget", cmd_forget))
    app.add_handler(CommandHandler("tasks", cmd_tasks))
    app.add_handler(CommandHandler("synthesize", cmd_synthesize))
    app.add_handler(CommandHandler("model", cmd_model))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("FriendlyClaw Telegram Live 🟢")
    app.run_polling()
