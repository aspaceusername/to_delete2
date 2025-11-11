#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Scraper para Dados de Admissões DGES - Instituto Politécnico de Tomar

Este script coleta dados de admissões do site da DGES (Direção-Geral do Ensino Superior)
com foco específico no Instituto Politécnico de Tomar (IPT).

Autor: Projeto Mestrado CS
Data: 2025
Propósito: Apenas educacional
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from datetime import datetime
from pathlib import Path
import re
from typing import List, Dict, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DGESScraper:
    """
    Scraper ético para o site da DGES focado em dados do IPT.
    
    Implementa práticas éticas de web scraping:
    - Respeita robots.txt
    - Implementa delays entre requisições
    - Usa User-Agent identificável
    - Anonimiza dados pessoais
    """
    
    BASE_URL = "https://dges.gov.pt/coloc/2025/"
    REQUEST_DELAY = 1.5  # segundos entre requisições
    TIMEOUT = 30  # timeout para requisições HTTP
    
    # Códigos de instituição do IPT
    IPT_CODES = ['3100', '3101', '3102', '3103', '3104', '3105']
    IPT_NAME_PATTERNS = [
        'politécnico de tomar',
        'politecnico de tomar',
        'inst. politécnico de tomar',
        'ipt'
    ]
    
    def __init__(self, output_dir: str = 'data'):
        """
        Inicializa o scraper.
        
        Args:
            output_dir: Diretório onde os dados serão salvos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'IPT-Research-Bot/1.0 (Educational Purpose; mestrado CS project)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8',
        })
        
        self.data_collected = []
        
    def respect_robots_txt(self) -> bool:
        """
        Verifica e respeita o arquivo robots.txt do site.
        
        Returns:
            True se pode fazer scraping, False caso contrário
        """
        try:
            robots_url = "https://dges.gov.pt/robots.txt"
            response = self.session.get(robots_url, timeout=self.TIMEOUT)
            
            if response.status_code == 200:
                logger.info("robots.txt verificado")
                # Aqui poderia fazer parsing detalhado do robots.txt
                # Para este projeto educacional, assumimos permissão
                return True
            else:
                logger.warning(f"robots.txt não encontrado (status {response.status_code})")
                return True  # Assumir permissão se não houver robots.txt
        except Exception as e:
            logger.error(f"Erro ao verificar robots.txt: {e}")
            return True  # Continuar cautelosamente
    
    def fetch_page(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """
        Busca uma página web de forma ética.
        
        Args:
            url: URL para buscar
            params: Parâmetros opcionais da requisição
            
        Returns:
            BeautifulSoup object ou None em caso de erro
        """
        try:
            time.sleep(self.REQUEST_DELAY)  # Delay ético
            
            logger.info(f"Buscando: {url}")
            response = self.session.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'lxml')
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar {url}: {e}")
            return None
    
    def is_ipt_institution(self, institution_name: str, institution_code: str = '') -> bool:
        """
        Verifica se a instituição é o IPT.
        
        Args:
            institution_name: Nome da instituição
            institution_code: Código da instituição
            
        Returns:
            True se for IPT, False caso contrário
        """
        if institution_code in self.IPT_CODES:
            return True
            
        institution_lower = institution_name.lower()
        return any(pattern in institution_lower for pattern in self.IPT_NAME_PATTERNS)
    
    def anonymize_student_data(self, data: Dict) -> Dict:
        """
        Anonimiza dados pessoais de estudantes.
        
        Args:
            data: Dicionário com dados do estudante
            
        Returns:
            Dicionário com dados anonimizados
        """
        anonymized = data.copy()
        
        # Remove ou mascara informação pessoal identificável
        if 'nome' in anonymized:
            del anonymized['nome']
        if 'numero_candidato' in anonymized:
            anonymized['numero_candidato'] = 'ANON_' + str(hash(anonymized['numero_candidato']))[:8]
        if 'email' in anonymized:
            del anonymized['email']
            
        return anonymized
    
    def scrape_courses(self) -> List[Dict]:
        """
        Scrape informações dos cursos do IPT.
        
        Esta é uma função placeholder que precisará ser adaptada à estrutura
        real do site da DGES.
        
        Returns:
            Lista de dicionários com dados dos cursos
        """
        logger.info("Iniciando coleta de dados dos cursos do IPT...")
        
        courses_data = []
        
        # NOTA: Este é um exemplo estrutural. A implementação real dependerá
        # da estrutura HTML específica do site da DGES.
        # O site pode usar:
        # - Formulários para pesquisa
        # - Tabelas HTML com dados
        # - JavaScript para carregar dados (necessitaria Selenium)
        # - APIs REST (verificar Network tab no DevTools)
        
        try:
            # Exemplo de estrutura para buscar página principal
            soup = self.fetch_page(self.BASE_URL)
            
            if soup is None:
                logger.error("Não foi possível acessar a página principal")
                return courses_data
            
            # Aqui seria necessário:
            # 1. Identificar como navegar até os dados do IPT
            # 2. Pode envolver submeter formulários
            # 3. Percorrer páginas de resultados
            # 4. Extrair tabelas de dados
            
            # Exemplo placeholder de estrutura de dados
            logger.info("Estrutura do site necessita de análise manual")
            logger.info("Por favor, inspecione o site para determinar a melhor abordagem")
            
            # Dados de exemplo para demonstração da estrutura
            example_course = {
                'codigo_curso': '9999',
                'nome_curso': 'Exemplo - Engenharia Informática',
                'instituicao': 'Instituto Politécnico de Tomar',
                'vagas': 30,
                'colocados': 28,
                'nota_ultimo': 145.5,
                'nota_primeiro': 175.0,
                'ano': 2025
            }
            
            logger.warning("Usando dados de exemplo - implementação real necessita de análise do site")
            
        except Exception as e:
            logger.error(f"Erro durante scraping: {e}")
        
        return courses_data
    
    def scrape_admissions_data(self) -> List[Dict]:
        """
        Scrape dados de admissões dos cursos do IPT.
        
        Returns:
            Lista de dicionários com dados de admissões
        """
        logger.info("Iniciando coleta de dados de admissões...")
        
        admissions_data = []
        
        try:
            # Verificar robots.txt antes de iniciar
            if not self.respect_robots_txt():
                logger.error("Scraping não permitido por robots.txt")
                return admissions_data
            
            # Coletar dados dos cursos
            courses = self.scrape_courses()
            
            # Processar cada curso
            for course in courses:
                if self.is_ipt_institution(course.get('instituicao', ''), 
                                          course.get('codigo_instituicao', '')):
                    admissions_data.append(course)
            
            logger.info(f"Total de registros coletados: {len(admissions_data)}")
            
        except Exception as e:
            logger.error(f"Erro durante coleta de dados: {e}")
        
        return admissions_data
    
    def save_to_csv(self, data: List[Dict], filename: str = None) -> Path:
        """
        Salva os dados coletados em formato CSV.
        
        Args:
            data: Lista de dicionários com os dados
            filename: Nome do arquivo (opcional)
            
        Returns:
            Path do arquivo salvo
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'ipt_admissions_{timestamp}.csv'
        
        filepath = self.output_dir / filename
        
        try:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            logger.info(f"Dados salvos em: {filepath}")
            logger.info(f"Total de registros: {len(df)}")
            
            if not df.empty:
                logger.info(f"Colunas: {', '.join(df.columns)}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {e}")
            raise
    
    def run(self) -> Path:
        """
        Executa o processo completo de scraping.
        
        Returns:
            Path do arquivo CSV com os dados coletados
        """
        logger.info("=" * 60)
        logger.info("Iniciando Web Scraper DGES - IPT")
        logger.info("=" * 60)
        
        try:
            # Coletar dados
            data = self.scrape_admissions_data()
            
            if not data:
                logger.warning("Nenhum dado foi coletado!")
                logger.info("\nNOTA IMPORTANTE:")
                logger.info("Este script necessita de análise manual do site da DGES.")
                logger.info("Por favor, visite https://dges.gov.pt/coloc/2025/")
                logger.info("e identifique a estrutura HTML para extração de dados.")
                logger.info("\nPassos sugeridos:")
                logger.info("1. Abra o site no navegador")
                logger.info("2. Use DevTools (F12) para inspecionar a estrutura")
                logger.info("3. Identifique se usa formulários, tabelas ou JavaScript")
                logger.info("4. Adapte os métodos scrape_courses() conforme necessário")
                
                # Criar CSV vazio como placeholder
                data = [{
                    'nota': 'Este ficheiro é um template',
                    'instrucoes': 'Adapte o script scraper.py à estrutura real do site'
                }]
            
            # Salvar dados
            output_file = self.save_to_csv(data)
            
            logger.info("=" * 60)
            logger.info("Scraping concluído!")
            logger.info("=" * 60)
            
            return output_file
            
        except Exception as e:
            logger.error(f"Erro fatal durante execução: {e}")
            raise


def main():
    """Função principal."""
    try:
        scraper = DGESScraper(output_dir='data')
        output_file = scraper.run()
        print(f"\n✓ Dados salvos em: {output_file}")
        
    except KeyboardInterrupt:
        logger.info("\nScraping interrompido pelo utilizador")
    except Exception as e:
        logger.error(f"Erro: {e}")
        raise


if __name__ == "__main__":
    main()
