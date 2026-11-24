from telegram.ext import Updater, InlineQueryHandler, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from bot.cogs.modules.database import *
from bot.cogs.modules.pix_authentication import *
from bot.cogs.modules.pix_key_check import *
from bot.cogs.estatisticas import *
from bot.cogs.ban import *
from bot.cogs.add_cc import *
from bot.cogs.troca import *
from bot.cogs.tools import *
from bot.cogs.add_credits import *
from bot.cogs.add_pix_config import *
from bot.cogs.afilliate import *
from bot.cogs.add_groups import *
from bot.cogs.buy import *
from bot.cogs.cc_main import *
from bot.cogs.delete_account import *
from bot.cogs.dynamic_buttons import *
from bot.cogs.gift import *
from bot.cogs.history import *
from bot.cogs.mix import *
from bot.cogs.profile import *
from bot.cogs.scheduled_tasks import *
from bot.cogs.search import *
from bot.cogs.send import *
from bot.cogs.start import *
from bot.cogs.add_admin import *
from bot.cogs.flags import *
from bot.cogs.users import *
from bot.cogs.delete_card import *
from bot.cogs.backup import *
import json, logging, time, os

# Configuração de Log para ver erros no Discloud
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        with open('config/config.json', 'r', encoding="utf8") as file:
            config = json.loads(file.read())
            token_bot = config['token_bot']
    except Exception as e:
        logger.error(f"Erro ao ler config: {e}")
        return

    print('\nIniciando Bot...')
    
    # Criação única do Updater
    updater = Updater(token_bot, use_context=True)
    dp = updater.dispatcher

    # --- REGISTRO DE HANDLERS ---

    # Admins
    for command in add_admin_command:
        dp.add_handler(CommandHandler(command, add_admin, run_async=True))
    for command in remove_admin_command:
        dp.add_handler(CommandHandler(command, remove_admin, run_async=True))

    # Comandos Principais
    for command in send_command:
        dp.add_handler(CommandHandler(command, send, run_async=True))
        
    for command in start_command:
        # GARANTIA: O handler start está sendo registrado aqui explicitamente
        dp.add_handler(CommandHandler(command, start, run_async=True))

    for command in add_credits:
        dp.add_handler(CommandHandler(command, recarregar, run_async=True))
        
    for command in add_cc:
        dp.add_handler(CommandHandler(command, adicionar_cc, run_async=True))
        
    for command in card:
        dp.add_handler(CommandHandler(command, cartao, run_async=True))

    for command in edit_prices:
        dp.add_handler(CommandHandler(command, editar_precos, run_async=True))

    for command in gift_add:
        dp.add_handler(CommandHandler(command, adicionar_gift, run_async=True))
        
    for command in gift_gen_command:
        dp.add_handler(CommandHandler(command, gerar_gift, run_async=True))
        
    for command in create_table:
        dp.add_handler(CommandHandler(command, criar_mix, run_async=True))
        
    for command in menu_pix_command:
        dp.add_handler(CommandHandler(command, menu_pix, run_async=True))

    # Comandos Avulsos
    dp.add_handler(CommandHandler('configuracoes', flags))
    dp.add_handler(CommandHandler('notificaraqui', add_groups))
    dp.add_handler(CommandHandler('chk', chk))
    dp.add_handler(CommandHandler('separador', separador))
    dp.add_handler(CommandHandler('baixarusuarios', baixar_usuarios))
    dp.add_handler(CommandHandler('resaldo', resaldo))
    dp.add_handler(CommandHandler('deletarcartoes', delete_all_cards))
    dp.add_handler(CommandHandler('deletarccs', delete_all_cards))
    dp.add_handler(CommandHandler('backup', download_backup))
    dp.add_handler(CommandHandler('estatisticas', estatisticas))
    dp.add_handler(CommandHandler('perfil', profile))
    dp.add_handler(CommandHandler('trocar_pix', trocar_pix))
    dp.add_handler(CommandHandler('pix_key', pix_key_check))
    dp.add_handler(CommandHandler('afiliados', afil_start))
    dp.add_handler(CommandHandler('history', history))
    dp.add_handler(CommandHandler('mix', mix_menu))
    dp.add_handler(CommandHandler('delete_account', delete_account))
    dp.add_handler(CommandHandler('send', send))
    dp.add_handler(CommandHandler('users', users))
    dp.add_handler(CommandHandler('add_admin', add_admin))
    dp.add_handler(CommandHandler('remove_admin', remove_admin))
    dp.add_handler(CommandHandler('add_cc', adicionar_cc))
    dp.add_handler(CommandHandler('add_credits', recarregar))
    dp.add_handler(CommandHandler('edit_prices', editar_precos))
    dp.add_handler(CommandHandler('gift_add', adicionar_gift))
    dp.add_handler(CommandHandler('gift_gen', gerar_gift))
    dp.add_handler(CommandHandler('create_table', criar_mix))
    dp.add_handler(CommandHandler('menu_pix', menu_pix))
    dp.add_handler(CommandHandler('flags', flags))
    dp.add_handler(CommandHandler('add_groups', add_groups))
    dp.add_handler(CommandHandler('chk', chk))
    dp.add_handler(CommandHandler('separador', separador))
    dp.add_handler(CommandHandler('baixarusuarios', baixar_usuarios))
    dp.add_handler(CommandHandler('resaldo', resaldo))
    dp.add_handler(CommandHandler('deletarcartoes', delete_all_cards))
    dp.add_handler(CommandHandler('deletarccs', delete_all_cards))
    dp.add_handler(CommandHandler('backup', download_backup))
    dp.add_handler(CommandHandler('estatisticas', estatisticas))
    dp.add_handler(CommandHandler('perfil', profile))
    dp.add_handler(CommandHandler('trocar_pix', trocar_pix))
    dp.add_handler(CommandHandler('pix_key', pix_key_check))
    dp.add_handler(CommandHandler('afiliados', afil_start))
    dp.add_handler(CommandHandler('history', history))
    dp.add_handler(CommandHandler('mix', mix_menu))
    dp.add_handler(CommandHandler('delete_account', delete_account))
    dp.add_handler(CommandHandler('send', send))
    dp.add_handler(CommandHandler('users', users))
    
    # Adiciona handlers extras se existirem nas listas definidas nos outros módulos
    # Ajuste conforme necessário baseado no que você tem em cada cog
    
    # --- HANDLERS DE BOTÃO (CALLBACKS) ---
    
    # Handler principal de callbacks (para botões como m1, m2, etc.)
    dp.add_handler(CallbackQueryHandler(dynamic_buttons, pattern='^m[0-9]+$'))
    
    # Handler para comprar cartão por ID (usando backticks)
    dp.add_handler(CallbackQueryHandler(cartao, pattern='^`.*'))
    
    # Handler para cancelar compra
    dp.add_handler(CallbackQueryHandler(cancelar_compra, pattern='^cancelar_compra$'))
    
    # Handler para remover cartão (apenas donos)
    dp.add_handler(CallbackQueryHandler(remove_card, pattern='^remove_.*'))
    
    # *** ADICIONADO AQUI: Handler para ver detalhes do cartão na lista aleatória ***
    dp.add_handler(CallbackQueryHandler(ver_cartao, pattern='^ver_.*'))

    # --- INICIAR BOT ---
    updater.start_polling()
    print("Bot rodando...")
    updater.idle()

if __name__ == '__main__':
    main()
