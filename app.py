from flask import Flask
from pyngrok import ngrok
import logging
import threading
from config import DEBUG, HOST, PORT, NGROK_AUTH_TOKEN  # Importar variáveis do config
from routes import configure_routes
from temp_files import init_temp_files

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração e inicialização do Flask
app = Flask(__name__)

# Configuração das rotas
configure_routes(app)

def run_flask():
    app.run(
        debug=DEBUG,
        use_reloader=False,
        host=HOST,
        port=PORT
    )

if __name__ == '__main__':
    init_temp_files()
    threading.Thread(target=run_flask).start()
    if NGROK_AUTH_TOKEN:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(PORT)
    logger.info(f"Ngrok public URL: {public_url}")
