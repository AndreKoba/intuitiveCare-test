import requests
from bs4 import BeautifulSoup
import os
import zipfile
import tabula
import pandas as pd
from urllib.parse import urljoin

class ANSScraper:
    def __init__(self):
        self.base_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
        self.output_dir = r"c:\Users\kobay\OneDrive\Documentos\dados2"
        
    def download_pdf(self, url, filename):
        try:
            response = requests.get(url)
            response.raise_for_status()
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filepath
        except Exception as e:
            print(f"Error downloading {filename}: {str(e)}")
            return None

    def find_pdf_links(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            pdf_links = {}
            for link in soup.find_all('a', href=True):
                href = link['href']
                if 'Anexo' in link.text and href.endswith('.pdf'):
                    pdf_links[f"anexo{len(pdf_links)+1}.pdf"] = urljoin(self.base_url, href)
            return pdf_links
        except Exception as e:
            print(f"Error accessing website: {str(e)}")
            return {}

    def create_zip(self, files, zip_name):
        zip_path = os.path.join(self.output_dir, zip_name)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
        return zip_path

    def extract_table_from_pdf(self, pdf_file):
        tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
        df = pd.concat(tables, ignore_index=True)
        return df

    def process_data(self, df):
        replacements = {
            'OD': 'Segmentação Assistencial: Odontológica',
            'AMB': 'Segmentação Assistencial: Ambulatorial'
        }
        
        for col in ['OD', 'AMB']:
            if col in df.columns:
                df[col] = df[col].replace(replacements)
        
        return df

    def run(self):
        
        os.makedirs(self.output_dir, exist_ok=True)

        pdf_links = self.find_pdf_links()
        downloaded_files = []
        
        for filename, url in pdf_links.items():
            filepath = self.download_pdf(url, filename)
            if filepath:
                downloaded_files.append(filepath)

        if downloaded_files:
            anexos_zip = self.create_zip(downloaded_files, 'anexos.zip')
            print(f"Created annexes ZIP: {anexos_zip}")

        if downloaded_files:
            anexo1_path = next((f for f in downloaded_files if 'anexo1' in f.lower()), None)
            if anexo1_path:
                df = self.extract_table_from_pdf(anexo1_path)
                
                df = self.process_data(df)
                csv_path = os.path.join(self.output_dir, 'extracted_data.csv')
                df.to_csv(csv_path, index=False)

                final_zip = self.create_zip([csv_path], 'Test_Gov.zip')
                print(f"Created final ZIP: {final_zip}")

if __name__ == "__main__":
    scraper = ANSScraper()
    scraper.run()