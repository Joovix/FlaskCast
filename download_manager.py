from yt_dlp import YoutubeDL
from pathlib import Path
import io
import re
import logging
from config import BASE_DOWNLOAD_DIR, MAX_FILE_SIZE, FFMPEG_PATH
from pydub import AudioSegment
from temp_files import save_temp_file

logger = logging.getLogger(__name__)

# Definir o caminho do FFmpeg para o AudioSegment
AudioSegment.converter = str(FFMPEG_PATH)

def normalize_filename(filename: str) -> str:
    """Normaliza o nome do arquivo removendo caracteres especiais."""
    filename = re.sub(r'[^\w\s-]', '', filename).strip()
    filename = re.sub(r'[\s]+', '_', filename)
    return filename

def get_yt_dlp_opts(download_path: Path, tipo: str) -> dict:
    """Define as opções para yt-dlp com base no tipo de download."""
    return {
        'format': 'bestaudio/best' if tipo == 'musica' else 'bestvideo+bestaudio/best',
        'outtmpl': str(download_path / '%(title)s.%(ext)s'),
        'noprogress': True,
        'quiet': False,
        'restrictfilenames': True,
        'nocheckcertificate': True,
        'noplaylist': True,
        'max_filesize': MAX_FILE_SIZE,
        'verbose': True  # Ativar o modo verbose
    }

def convert_to_mp3(input_path: Path, output_path: Path):
    """Converte arquivo de áudio para MP3."""
    try:
        audio = AudioSegment.from_file(str(input_path))
        audio.export(str(output_path), format="mp3")
    except Exception as e:
        logger.error(f"Erro na conversão para MP3: {e}")
        raise Exception(f"Erro na conversão do arquivo: {str(e)}")

def process_download(download_request) -> tuple[io.BytesIO, str, str]:
    """Processa o download e retorna o buffer com o arquivo."""
    download_dir = BASE_DOWNLOAD_DIR / download_request['tipo']
    download_dir.mkdir(parents=True, exist_ok=True)  # Garante que o diretório existe

    ydl_opts = get_yt_dlp_opts(download_dir, download_request['tipo'])
    search_url = f"ytsearch1:{download_request['url']}" if 'youtube.com' not in download_request['url'] else download_request['url']
    logger.info(f"URL de pesquisa: {search_url}")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=True)
        logger.info(f"Info extraído: {info}")

        if 'entries' in info:
            info = info['entries'][0]

        # Diretamente pegar o caminho do arquivo do resultado do yt-dlp
        downloaded_path = Path(info['requested_downloads'][0]['filepath'])
        logger.info(f"Arquivo baixado: {downloaded_path}")

        if not downloaded_path.exists():
            logger.error("Erro: Arquivo não encontrado após o download.")
            raise FileNotFoundError("Arquivo não encontrado após o download.")

        # Se for música, converta para MP3
        if download_request['tipo'] == 'musica':
            mp3_path = downloaded_path.with_suffix('.mp3')
            convert_to_mp3(downloaded_path, mp3_path)
            downloaded_path.unlink()  # Remove o arquivo original
            final_path = mp3_path
        else:
            final_path = downloaded_path

        # Prepara o buffer para envio
        buffer = io.BytesIO(final_path.read_bytes())
        buffer.seek(0)
        final_path.unlink()  # Remove o arquivo após a leitura
        return buffer, final_path.name, 'audio/mpeg' if download_request['tipo'] == 'musica' else 'video/mp4'
