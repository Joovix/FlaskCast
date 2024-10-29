FlaskCast 🎶📽️
FlaskCast é uma aplicação de código aberto desenvolvida com Flask que permite o download e a conversão de mídia (áudio e vídeo) diretamente do YouTube. Utilizando yt-dlp para downloads e pydub com FFmpeg para conversão de áudio para MP3, o FlaskCast facilita a aquisição de conteúdo multimídia de forma prática e rápida.

Índice
Recursos
Tecnologias Utilizadas
Instalação
Configuração
Uso
Licença
Aviso Legal
Contribuições
Recursos
Download de Vídeos e Áudios 🎬🎧: Baixe vídeos completos ou extraia o áudio de vídeos do YouTube em poucos cliques.
Conversão para MP3 🔊: Converte automaticamente arquivos de áudio para o formato MP3 com alta qualidade.
Configuração Personalizável 🛠️: O diretório de downloads e outras configurações podem ser ajustadas no arquivo config.ini.
Servidor Público com ngrok 🌐: Torne o servidor acessível publicamente com integração ao ngrok.
Responsabilidade do Usuário ⚠️: Os usuários são responsáveis por respeitar direitos autorais, conforme descrito nos Termos de Uso.
Tecnologias Utilizadas
Python 🐍
Flask para a estrutura de servidor web.
yt-dlp para download de mídia do YouTube.
pydub com FFmpeg para conversão de áudio em MP3.
Instalação
Clone este repositório:

bash
Copiar código
git clone https://github.com/seuusuario/FlaskCast.git
cd FlaskCast
Instale as dependências necessárias:

bash
Copiar código
pip install -r requirements.txt
Baixe e instale o FFmpeg e adicione-o ao PATH ou configure o caminho no config.ini.

Configuração
Abra o arquivo config.ini e configure as seguintes variáveis:

base_dir: O caminho onde os arquivos baixados serão salvos.
max_filesize: Tamanho máximo permitido para arquivos de download (em bytes).
ffmpeg_path: Caminho para o executável do FFmpeg.
ttl: Tempo de vida dos arquivos temporários (em segundos).
Exemplo:

ini
Copiar código
[server]
debug = true
host = 0.0.0.0
port = 5000

[download]
base_dir = C:/kaue/downloads
max_filesize = 104857600  # 100 MB

[ffmpeg]
path = C:/path/to/ffmpeg/bin/ffmpeg.exe

[temp_files]
ttl = 600  # Tempo de vida dos arquivos temporários em segundos
Opcionalmente, configure o ngrok para tornar o servidor acessível publicamente. Para isso, adicione seu token de autenticação do ngrok ao arquivo de variáveis de ambiente ou config.ini.

Uso
Para iniciar o servidor, execute o seguinte comando:

bash
Copiar código
python app.py
Acesse http://localhost:5000 em seu navegador para utilizar o FlaskCast.

Para download de mídia:

Insira a URL do vídeo do YouTube ou uma pesquisa por palavra-chave.
Escolha o tipo de mídia (áudio ou vídeo).
Clique em baixar para iniciar o processo.
Licença
Este projeto está licenciado sob a Apache License 2.0 - consulte o arquivo LICENSE para obter mais informações.

Aviso Legal
FlaskCast é uma ferramenta de código aberto destinada ao uso pessoal. O uso para baixar conteúdo protegido por direitos autorais sem permissão é de total responsabilidade do usuário. Consulte os Termos de Uso para mais detalhes.

Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias, correções de bugs ou novos recursos.