from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_CONTEXT):
    # A formatação com ** torna negrito e _ torna itálico
    welcome_message = (
        "**👋 Bem-vindo ao Mystery Store!**\n\n"
        "Aqui você encontra os melhores dados.\n"
        "✅ Entrega rápida\n"
        "✅ Suporte 24h\n"
        "✅ Qualidade garantida\n\n"
        "Escolha uma opção abaixo:"
    )
    
    await update.message.reply_text(welcome_message, parse_mode='MarkdownV2')
