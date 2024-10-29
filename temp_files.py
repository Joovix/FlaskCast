import os
import time
import threading
import logging
from pathlib import Path
from config import BASE_DOWNLOAD_DIR, FILE_TTL  # Importar as variáveis necessárias

# Diretório temporário e tempo de vida dos arquivos
TEMP_DIR = BASE_DOWNLOAD_DIR / "temp"  # Definir TEMP_DIR com base no diretório de download principal

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def init_temp_files():
    """
    Inicializa o gerenciamento de arquivos temporários.
    - Cria o diretório temporário, se necessário.
    - Inicia o thread de limpeza.
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)  # Cria o diretório temporário se não existir
    cleaner_thread = threading.Thread(target=clean_temp_files)
    cleaner_thread.daemon = True
    cleaner_thread.start()

def save_temp_file(buffer, filename):
    """
    Salva um arquivo temporário.
    - Gera um nome único para o arquivo.
    - Salva o conteúdo do buffer no arquivo temporário.
    - Retorna o caminho completo do arquivo temporário.
    """
    temp_filename = f"{filename}-{int(time.time())}.tmp"
    temp_filepath = TEMP_DIR / temp_filename
    with temp_filepath.open('wb') as f:
        f.write(buffer.getbuffer())
    return str(temp_filepath)

def clean_temp_files():
    """
    Limpa arquivos temporários expirados.
    - Percorre o diretório temporário.
    - Remove arquivos que ultrapassaram o tempo de vida configurado.
    """
    # Certifique-se de que o diretório temporário existe antes de tentar limpá-lo
    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        for file in TEMP_DIR.iterdir():
            if file.is_file() and time.time() - file.stat().st_mtime > FILE_TTL:
                try:
                    file.unlink()
                    logger.info(f"Arquivo temporário removido: {file}")
                except OSError as e:
                    logger.error(f"Erro ao remover arquivo: {e}")
        time.sleep(FILE_TTL)