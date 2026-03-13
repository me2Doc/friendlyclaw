import os
import asyncio
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)
from core.agent import chat
from core.onboarding import (
    get_onboarding_state, get_current_question,
    process_onboarding_answer, get_welcome_message
)
from memory.memory import (
    init_db, get_memories, get_facts,
    clear_user, save_profile, get_profile
)
from skills.skills import get_skill_prompt, get_help_text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_db()

    state = get_onboarding_state(user_id)
    if state["done"]:
        profile = get_profile(user_id)
        name = profile.get("agent_name", "me")
        await update.message.reply_text(
            f"Hey, I'm here. What's going on?",
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

    # Still onboarding
    if not state["done"]:
        result = process_onboarding_answer(user_id, text)
        if result["done"]:
            agent_name = result.get("agent_name", "Buddy")
            user_name = result.get("user_name", "friend")
            await update.message.reply_text(
                f"Set. I'm *{agent_name}*.\n\n"
                f"Talk to me whenever, {user_name}. "
                f"I remember everything from here on out.\n\n"
                f"Send /help to see what I can do.",
                parse_mode="Markdown"
            )
        else:
            step = result["step"]
            total = result["total"]
            await update.message.reply_text(
                f"[{step}/{total}] {result['next_question']}",
                parse_mode="Markdown"
            )
        return

    # Check for skill triggers
    skill_prompt = None
    clean_text = text
    for cmd in ["/analyze", "/redflag", "/reply", "/opener", "/vent", "/advice"]:
        if text.startswith(cmd):
            skill_prompt = get_skill_prompt(cmd)
            clean_text = text[len(cmd):].strip()
            if not clean_text:
                clean_text = f"User triggered {cmd} skill — ask them what they want to analyze/discuss."
            break

    if skill_prompt:
        message = f"[SKILL ACTIVE: {skill_prompt}]\n\nUser says: {clean_text}"
    else:
        message = text

    await update.message.chat.send_action("typing")
    reply = await chat(user_id, message)
    await update.message.reply_text(reply)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    state = get_onboarding_state(user_id)

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = bytes(await file.download_as_bytearray())

    # If still in onboarding and on visual context step
    if not state["done"]:
        profile = get_profile(user_id)
        step = profile.get("onboarding_step", 0)
        from core.onboarding import QUESTIONS
        if step < len(QUESTIONS) and QUESTIONS[step].get("accepts_photo"):
            result = process_onboarding_answer(user_id, "[photo]", image_bytes=image_bytes)
            if result["done"]:
                await update.message.reply_text(
                    f"Got it. I'll keep that in mind.\n\nSet. Talk to me whenever. Send /help to see commands.",
                )
            else:
                await update.message.reply_text(result["next_question"], parse_mode="Markdown")
            return

    caption = update.message.caption or "Analyze this image and tell me what you see and what I should know."
    await update.message.chat.send_action("typing")
    reply = await chat(user_id, caption, image_bytes=image_bytes)
    await update.message.reply_text(reply)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_help_text(), parse_mode="Markdown")


async def cmd_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    memories = get_memories(user_id)
    facts = get_facts(user_id)

    if not memories and not facts:
        await update.message.reply_text("Nothing stored yet. Talk to me more.")
        return

    text = "*What I remember about you:*\n\n"
    if facts:
        text += "*Facts:*\n"
        for f in facts[:15]:
            text += f"• {f}\n"
    if memories:
        text += "\n*Notes:*\n"
        for m in memories[:10]:
            text += f"• [{m['key']}] {m['value']}\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_forget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    clear_user(user_id)
    await update.message.reply_text(
        "Memory wiped. Profile deleted. Type /start to begin again."
    )


async def cmd_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        current = os.getenv("MODEL_NAME", "gemini-2.0-flash")
        provider = os.getenv("MODEL_PROVIDER", "gemini")
        await update.message.reply_text(
            f"Current model: `{current}` (provider: `{provider}`)\n\n"
            "To switch: `/model [model-name]`\n"
            "Change provider in your `.env` file.",
            parse_mode="Markdown"
        )
        return

    new_model = args[0]
    os.environ["MODEL_NAME"] = new_model
    await update.message.reply_text(f"Model switched to `{new_model}` for this session.\nTo make permanent, update MODEL_NAME in .env", parse_mode="Markdown")


def run_telegram():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("memory", cmd_memory))
    app.add_handler(CommandHandler("forget", cmd_forget))
    app.add_handler(CommandHandler("model", cmd_model))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("FriendlyClaw Telegram bot is live 🟢")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
