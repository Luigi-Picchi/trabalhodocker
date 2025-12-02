import requests
import csv
import os
import sys
import argparse
from pathlib import Path
from bs4 import BeautifulSoup

def gerar_relatorio(api_url):
    """
    Gera relatório CSV a partir da API de livros (scraping HTML)
    """
    try:
        print(f"🔍 Conectando à API: {api_url}")
        
        # Fazer requisição à API
        response = requests.get(f"{api_url}/books", timeout=10)
        response.raise_for_status()
        
        # Parse do HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        
        if not table:
            print("⚠️  Tabela de livros não encontrada")
            return False
        
        # Extrair dados da tabela
        livros = []
        rows = table.find_all('tr')[1:]  # Pular o header
        
        for row in rows:
            cols = row.find_all(['th', 'td'])
            if len(cols) >= 4:
                livro = {
                    'id': cols[0].get_text(strip=True),
                    'title': cols[1].get_text(strip=True),
                    'author': cols[2].get_text(strip=True),
                    'description': cols[3].get_text(strip=True)
                }
                livros.append(livro)
        
        print(f"✅ {len(livros)} livros encontrados")
        
        if not livros:
            print("⚠️  Nenhum livro encontrado na tabela")
            return False
        
        # Criar diretório de relatórios
        reports_dir = Path("/reports")
        reports_dir.mkdir(exist_ok=True)
        
        # Caminho do arquivo CSV
        csv_path = reports_dir / "relatorio_livros.csv"
        
        # Escrever CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'author', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for livro in livros:
                writer.writerow(livro)
        
        print(f"✅ Relatório gerado: {csv_path}")
        
        # Validar CSV gerado
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            print(f"✅ Validação: {len(rows)} linhas no CSV")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-url', 
                       default=os.getenv('API_URL', 'http://livros_api:8000'))
    args = parser.parse_args()
    
    print("📊 Iniciando geração de relatório...")
    success = gerar_relatorio(args.api_url)
    
    sys.exit(0 if success else 1)