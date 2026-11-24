from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from random import randint
from bot.cogs.ban import *
from bot.cogs.modules.adm_list import adm_list
import asyncio


def is_null(content):
    if content.strip() == '' or content.strip() == 'None':
        return 'N/A'
    else:
        return content


def cartao(update: Update, context: CallbackContext):
    # Mantém sua função original de compra por texto/id
    query = update.message
    user_info = query.from_user
    user_id = str(user_info['id'])
    
    if check_status(user_id):
        try:
            donos = adm_list()
            cc_id = query.text.split()[1]
            if '|' in cc_id:
                cc_id, tipo_p = cc_id.split('|')
            else:
                tipo_p = ''
            row = asyncio.run(pesquisar_cc_id(cc_id))
            numero = row[1][:6]
            expiracao = is_null(row[2])
            tipo = is_null(row[4])
            bandeira = is_null(row[5])
            categoria = is_null(row[6])
            banco = is_null(row[7])
            preco_cc = is_null(asyncio.run(precos(categoria)))
            
            keyboard = [
                [InlineKeyboardButton(f'✅ {button_buy}', callback_data='`'+str(cc_id)+tipo_p)],
                [InlineKeyboardButton(f'❌ {button_cancel}', callback_data='cancelar_compra')],]
            
            if user_id in donos:
                keyboard.append([InlineKeyboardButton(f'🗑️ Deletar CC', callback_data=f'remove_{cc_id}')])
            
            update.message.reply_text(text=cc_info_buy.format(numero, expiracao, bandeira, tipo, categoria, banco, preco_cc), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        except:
            update.message.reply_text(text=card_id_error, parse_mode='Markdown')

    else:
        update.message.reply_text(text=denied_text(user_id), parse_mode='Markdown')


def aleatoria(update: Update, context: CallbackContext):
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])
    
    # Verifica se tem permissão
    if check_status(user_id):
        try:
            # Busca todos os cartões cadastrados no banco
            rows = asyncio.run(all_ccs())
            
            # Se não tiver nenhum cartão
            if not rows:
                keyboard2 = [[InlineKeyboardButton("◀︎ Voltar", callback_data='m1')]]
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="📦 Estoque vazio.", reply_markup=InlineKeyboardMarkup(keyboard2))
                return

            # Cria a lista de botões para cada cartão
            keyboard = []
            for row in rows:
                cc_id = row[0]
                numero = row[1][:6] + "****" # Mostra só os 6 primeiros números
                bandeira = is_null(row[5])
                
                # Cria o botão visualmente bonito
                # IMPORTANTE: Usamos 'ver_' para diferenciar de outros callbacks
                btn = InlineKeyboardButton(f"💳 {bandeira} {numero}", callback_data=f'ver_{cc_id}')
                keyboard.append([btn])
            
            # Adiciona o botão de voltar no final
            keyboard.append([InlineKeyboardButton("◀︎ Voltar", callback_data='m1')])
            
            # Atualiza a tela com a lista
            context.bot.edit_message_text(
                chat_id=query.message.chat_id, 
                message_id=query.message.message_id, 
                text="📋 **GGs Disponíveis:**\n\nSelecione um card:", 
                parse_mode='Markdown', 
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        except Exception as e:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f"⚠️ Erro: {e}")
    else:
        # Mensagem de negado
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')


def ver_cartao(update: Update, context: CallbackContext):
    """
    Função chamada quando clica em um cartão da lista aleatória.
    Reutiliza a lógica de exibição do cartao(), mas lendo o callback_data.
    """
    query = update.callback_query
    query.answer() # Remove o spinner
    
    user_info = query.from_user
    user_id = str(user_info['id'])
    
    if check_status(user_id):
        try:
            # Pega o ID do botão clicado (ex: 'ver_123' -> pega '123')
            data = query.data
            cc_id = data.replace('ver_', '')
            
            # Se houver tipo de pagamento junto (opcional, dependendo do seu sistema)
            if '|' in cc_id:
                cc_id, tipo_p = cc_id.split('|')
            else:
                tipo_p = ''

            # Busca os dados no banco
            row = asyncio.run(pesquisar_cc_id(cc_id))
            if not row:
                query.edit_message_text("Card não encontrado.")
                return

            numero = row[1][:6]
            expiracao = is_null(row[2])
            tipo = is_null(row[4])
            bandeira = is_null(row[5])
            categoria = is_null(row[6])
            banco = is_null(row[7])
            preco_cc = is_null(asyncio.run(precos(categoria)))
            
            donos = adm_list()
            
            keyboard = [
                [InlineKeyboardButton(f'✅ {button_buy}', callback_data='`'+str(cc_id)+tipo_p)],
                [InlineKeyboardButton(f'❌ {button_cancel}', callback_data='cancelar_compra')],]
            
            if user_id in donos:
                keyboard.append([InlineKeyboardButton(f'🗑️ Deletar CC', callback_data=f'remove_{cc_id}')])
            
            # Usa o mesmo formato de mensagem da função cartao original
            query.edit_message_text(
                text=cc_info_buy.format(numero, expiracao, bandeira, tipo, categoria, banco, preco_cc), 
                parse_mode='Markdown', 
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        except Exception as e:
            query.edit_message_text(text=f"Erro ao carregar card: {e}")

    else:
        query.edit_message_text(text=denied_text(user_id), parse_mode='Markdown')
