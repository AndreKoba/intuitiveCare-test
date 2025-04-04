
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile

# URL da página-alvo
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Pasta para salvar os arquivos PDF
download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

# Função para baixar arquivos PDF
def download_pdf(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = os.path.join(folder, url.split("/")[-1])
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"Arquivo baixado: {file_name}")
        return file_name
    else:
        print(f"Falha ao baixar o arquivo: {url}")
        return None

# Função para compactar arquivos em um arquivo ZIP
def create_zip(files, zip_name):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            if file and os.path.exists(file):
                zipf.write(file, os.path.basename(file))
                print(f"Adicionado ao ZIP: {file}")
    print(f"Arquivo ZIP criado: {zip_name}")

# Acessa a página e extrai os links dos anexos
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    pdf_links = []

    # Procura por links que terminam com ".pdf"
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".pdf"):
            full_url = urljoin(url, href)
            pdf_links.append(full_url)

    # Baixa os arquivos PDF
    downloaded_files = []
    for pdf_url in pdf_links:
        file_path = download_pdf(pdf_url, download_folder)
        if file_path:
            downloaded_files.append(file_path)

    # Compacta os arquivos baixados em um arquivo ZIP
    if downloaded_files:
        zip_file_name = "anexos.zip"
        create_zip(downloaded_files, zip_file_name)
    else:
        print("Nenhum arquivo PDF foi baixado.")
else:
    print(f"Falha ao acessar a página: {url}")