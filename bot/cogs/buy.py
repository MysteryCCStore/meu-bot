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
                btn = InlineKeyboardButton(f"💳 {bandeira} {numero}", callback_data=f'view_{cc_id}')
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
        # Mensagem de negado (mantenha a original ou use esta)
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')


def cancelar_compra(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')]]
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cancelled_purchase, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


def comprar(update: Update, context: CallbackContext):
    results = asyncio.run(all_ccs())

    q = len(results)
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])
    if check_status(user_id):
        nome = str(user_info['first_name'])
        asyncio.run(registrar_usuario(user_id, nome))
        asyncio.run(name_update(user_id, nome))
        user = asyncio.run(pesquisar_id(str(user_id)))
        saldo = user[1]

        if not q == 0:
            if q > 2:
                r = randint(0, q-1)
            else:
                r = 0
                
            bandeira = results[r][5]
            bin_num = results[r][1][:6]
            banco = results[r][7]

            if bandeira.strip() == '':
                bandeira = scheme_search_default

            if bin_num.strip() == '':
                bin_num = bin_search_default

            if banco.strip() == '':
                banco = bank_search_default

        else:
            bandeira = scheme_search_default
            bin_num = bin_search_default
            banco = bank_search_default

        keyboard = [
            [InlineKeyboardButton(f'💳 {button_unitary_card}', callback_data='unitaria'),
            InlineKeyboardButton(f'🎲 {button_random_card}', callback_data='aleatoria'),],
            [InlineKeyboardButton(f'🔃 {button_mix}', callback_data='mix'),
            InlineKeyboardButton(f'🔎 Pesquisar', callback_data='search')],
            [InlineKeyboardButton(f'◀︎ {button_main}', callback_data='main')]]
        
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=stock_status.format(saldo, q), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=denied_text(user_id), parse_mode='Markdown')


