# main.py
import sys
import os
import logging

# Adiciona o diretório raiz ao path para garantir imports corretos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.cogs.modules.create_dirs import create_dirs
from bot.cogs.modules.create_flags import create_flags
from bot.cogs.modules.database import conn
from bot.cogs.modules.patch_fix import fix_bins, fix_compradas
import asyncio

def setup_environment():
    """Configurações iniciais síncronas"""
    try:
        create_dirs(['temp', 'config/cert'])
        create_flags()
        
        # Executa as funções de fixação em um loop de evento isolado
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(fix_bins())
            loop.run_until_complete(fix_compradas())
        finally:
            loop.close()
            
        print("Ambiente configurado com sucesso.")
    except Exception as e:
        logging.error(f"Falha na configuração inicial: {e}")
        raise

def run_bot():
    """Executa o bot principal"""
    try:
        from bot.bot import main
        main()
    except KeyboardInterrupt:
        print('\nBot encerrado pelo usuário!')
    except Exception as e:
        logging.error(f'Erro crítico no bot: {e}')
        raise
    finally:
        # Garante o fechamento da conexão do banco
        if 'conn' in globals() and conn:
            try:
                conn.close()
            except:
                pass

if __name__ == '__main__':
    setup_environment()
    run_bot()
