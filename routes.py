from flask import render_template, request, send_file, send_from_directory, current_app
from validation import validate_request
from download_manager import process_download
from config import BASE_DOWNLOAD_DIR, FILE_TTL  # E outras variáveis necessárias
import logging

logger = logging.getLogger(__name__)

def configure_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/favicon.ico')
    def favicon():
        """Serve o favicon se solicitado pelo navegador."""
        return send_from_directory(current_app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/baixar', methods=['POST'])
    @validate_request
    def baixar():
        try:
            entrada = request.form['entrada']
            tipo = request.form['tipo']
            download_request = {'url': entrada, 'tipo': tipo, 'filename': ''}
            buffer, filename, mimetype = process_download(download_request)
            return send_file(buffer, as_attachment=True, download_name=filename, mimetype=mimetype)
        except Exception as e:
            logger.error(f"Erro ao processar download: {str(e)}")
            return str(e), 400
