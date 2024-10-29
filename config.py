import os
import configparser
from pathlib import Path
from pydub import AudioSegment

# Inicializar o ConfigParser e ler o arquivo de configuração
config = configparser.ConfigParser()
config.read('config.ini')

# Configurações do Servidor
DEBUG = config.getboolean('server', 'debug', fallback=False)
HOST = config.get('server', 'host', fallback='0.0.0.0')
PORT = config.getint('server', 'port', fallback=5000)

# Configurações de Download
BASE_DOWNLOAD_DIR = Path(config.get('download', 'base_dir', fallback='C:/kaue/downloads'))
MAX_FILE_SIZE = config.getint('download', 'max_filesize', fallback=1024 * 1024 * 100)

# Configuração do FFmpeg
FFMPEG_PATH: Path = Path(config.get('ffmpeg', 'path', fallback='C:\\ffmpeg-7.1\\ffmpeg-2024-10-21-git-baa23e40c1-essentials_build\\bin\\ffmpeg.exe'))
AudioSegment.converter = str(FFMPEG_PATH)

# Configurações de Arquivos Temporários
FILE_TTL = config.getint('temp_files', 'ttl', fallback=600)

# Configurações de Segurança
SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')

# Configurações opcionais para ngrok
NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN', None)

def validate_config():
    try:
        if not BASE_DOWNLOAD_DIR.exists():
            raise FileNotFoundError(f"O diretório de downloads '{BASE_DOWNLOAD_DIR}' não existe.")
        if not FFMPEG_PATH.exists():
            raise FileNotFoundError(f"O caminho para o FFmpeg '{FFMPEG_PATH}' não é válido.")
    except Exception as e:
        print(f"Erro ao validar configurações: {str(e)}")
        exit(1)

validate_config()
