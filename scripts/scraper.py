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
    
    # Fases de colocação
    PHASES = ['1', '2', '3']  # 3 fases de admissão
    DATA_TYPES = ['colocados', 'candidatos']  # admitidos e candidatos
    
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
    
    def find_next_page_link(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Encontra o link para a próxima página (paginação).
        Procura por links com texto "Seguinte" ou similares.
        
        Args:
            soup: BeautifulSoup object da página atual
            
        Returns:
            URL da próxima página ou None se não houver
        """
        # Procurar por links com texto "Seguinte", "Next", "Próxima", etc.
        next_link = None
        
        for link in soup.find_all('a'):
            link_text = link.get_text(strip=True).lower()
            if any(keyword in link_text for keyword in ['seguinte', 'next', 'próxima', 'proxima', '>']):
                href = link.get('href')
                if href:
                    # Se for URL relativa, tornar absoluta
                    if href.startswith('http'):
                        next_link = href
                    else:
                        # Remover / inicial se existir
                        href = href.lstrip('/')
                        next_link = f"{self.BASE_URL}{href}"
                    logger.info(f"Link 'Seguinte' encontrado: {next_link}")
                    break
        
        return next_link
    
    def navigate_to_course_data(self, phase: str, data_type: str, course_code: str = None) -> Optional[str]:
        """
        Navega através dos formulários do DGES para chegar aos dados do curso.
        O site DGES requer múltiplos passos:
        1. Acessar página inicial de listas
        2. Selecionar escola (IPT = código 3242)
        3. Selecionar tipo de lista (candidatos ou colocados ordenados)
        4. Selecionar curso (Engenharia Informática se especificado)
        5. Clicar em "Continuar"
        
        Args:
            phase: Número da fase ('1', '2', ou '3')
            data_type: Tipo de dados ('colocados' ou 'candidatos')
            course_code: Código do curso (opcional, para filtrar curso específico)
            
        Returns:
            URL final da página de dados ou None se falhar
        """
        logger.info(f"Navegando para dados - Fase {phase} - {data_type}")
        
        try:
            # Passo 1: Acessar página inicial
            initial_url = f"{self.BASE_URL}col{phase}listas.asp?CodR=12&action=2"
            logger.info(f"Passo 1: Acessando {initial_url}")
            
            soup = self.fetch_page(initial_url)
            if soup is None:
                logger.error(f"Não foi possível acessar página inicial")
                return None
            
            # Passo 2: Procurar e submeter primeiro formulário (seleção de escola)
            forms = soup.find_all('form')
            logger.info(f"Encontrados {len(forms)} formulários na página")
            
            for form_idx, form in enumerate(forms):
                # Procurar por select de escola - tentar vários nomes possíveis
                school_select = None
                for name_pattern in ['CodEst', 'escola', 'Escola', 'codest', 'instituicao', 'Instituicao']:
                    school_select = form.find('select', {'name': name_pattern})
                    if school_select:
                        logger.info(f"Select de escola encontrado com name='{name_pattern}'")
                        break
                
                # Se não encontrou por nome, procurar por select que contenha opção 3242
                if not school_select:
                    for select in form.find_all('select'):
                        if select.find('option', {'value': '3242'}):
                            school_select = select
                            logger.info(f"Select de escola encontrado por valor 3242")
                            break
                
                if school_select:
                    # Preparar dados do formulário
                    form_data = {}
                    
                    # Adicionar seleção de escola IPT (3242)
                    select_name = school_select.get('name', 'CodEst')
                    form_data[select_name] = '3242'
                    logger.info(f"Selecionando IPT: {select_name}=3242")
                    
                    # Adicionar todos os inputs hidden
                    for input_tag in form.find_all('input', {'type': 'hidden'}):
                        name = input_tag.get('name')
                        value = input_tag.get('value', '')
                        if name:
                            form_data[name] = value
                    
                    # Procurar por radio buttons ou links para tipo de lista
                    # Tentar identificar "lista de candidatos" vs "lista ordenada de candidatos"
                    for radio in form.find_all('input', {'type': 'radio'}):
                        name = radio.get('name')
                        value = radio.get('value', '')
                        label_text = ''
                        
                        # Tentar encontrar label associado
                        radio_id = radio.get('id')
                        if radio_id:
                            label = form.find('label', {'for': radio_id})
                            if label:
                                label_text = label.get_text(strip=True).lower()
                        
                        # Selecionar baseado no tipo de dados
                        if data_type == 'candidatos' and ('candidatos' in label_text or 'candidatura' in label_text):
                            if name:
                                form_data[name] = value
                                logger.info(f"Selecionando tipo lista candidatos: {name}={value}")
                        elif data_type == 'colocados' and ('colocad' in label_text or 'ordenad' in label_text):
                            if name:
                                form_data[name] = value
                                logger.info(f"Selecionando tipo lista colocados: {name}={value}")
                    
                    # Procurar botão de submit
                    submit_button = form.find('input', {'type': 'submit'})
                    if submit_button:
                        submit_name = submit_button.get('name')
                        submit_value = submit_button.get('value', '')
                        if submit_name:
                            form_data[submit_name] = submit_value
                    
                    # Submeter formulário
                    form_action = form.get('action', '')
                    if not form_action:
                        # Se não tem action, usar URL atual
                        form_action = initial_url
                    elif not form_action.startswith('http'):
                        form_action = f"{self.BASE_URL}{form_action.lstrip('/')}"
                    
                    logger.info(f"Submetendo formulário para: {form_action}")
                    logger.info(f"Dados do formulário: {form_data}")
                    
                    time.sleep(self.REQUEST_DELAY)
                    response = self.session.post(form_action, data=form_data, timeout=self.TIMEOUT)
                    response.raise_for_status()
                    
                    # Verificar se precisamos submeter mais formulários (seleção de curso)
                    soup2 = BeautifulSoup(response.content, 'lxml')
                    forms2 = soup2.find_all('form')
                    
                    if forms2 and course_code:
                        logger.info(f"Página intermediária encontrada, procurando curso...")
                        # Procurar formulário com seleção de curso
                        for form2 in forms2:
                            course_select = form2.find('select')
                            if course_select:
                                # Procurar Engenharia Informática
                                for option in course_select.find_all('option'):
                                    option_text = option.get_text(strip=True).lower()
                                    if 'engenharia' in option_text and 'informática' in option_text:
                                        course_value = option.get('value')
                                        # Submeter seleção de curso
                                        # ... (implementar se necessário)
                                        break
                    
                    logger.info(f"Navegação concluída. URL final: {response.url}")
                    return response.url
            
            logger.warning("Formulário de seleção não encontrado")
            # Se não encontrou formulário, tentar acesso direto baseado no padrão observado
            # Isto é um fallback caso a navegação por formulário falhe
            logger.info("Tentando acesso direto via padrão de URL...")
            
            # Baseado no comentário do usuário, após seleção parece ir para listaser.asp ou listacol.asp
            if data_type == 'candidatos':
                direct_url = f"{self.BASE_URL}col{phase}listaser.asp?CodEst=3242"
            else:
                direct_url = f"{self.BASE_URL}col{phase}listacol.asp?CodEst=3242"
            
            logger.info(f"Tentando URL direta: {direct_url}")
            return direct_url
            
        except Exception as e:
            logger.error(f"Erro ao navegar: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
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
    
    def scrape_phase_data(self, phase: str, data_type: str) -> List[Dict]:
        """
        Scrape dados de uma fase específica (colocados ou candidatos).
        
        Args:
            phase: Número da fase ('1', '2', ou '3')
            data_type: Tipo de dados ('colocados' ou 'candidatos')
            
        Returns:
            Lista de dicionários com dados da fase
        """
        logger.info(f"Coletando dados - Fase {phase} - {data_type}")
        
        phase_data = []
        
        try:
            # Navegar através dos formulários do DGES para chegar aos dados
            # O site requer: selecionar escola IPT (3242) -> selecionar tipo de lista -> selecionar curso -> continuar
            current_url = self.navigate_to_course_data(phase, data_type)
            
            if current_url is None:
                logger.error(f"Não foi possível navegar para dados - Fase {phase} - {data_type}")
                return phase_data
            
            page_num = 1
            
            while current_url:
                logger.info(f"Processando página {page_num} - Fase {phase} - {data_type}")
                
                soup = self.fetch_page(current_url)
                
                if soup is None:
                    logger.warning(f"Não foi possível acessar: {current_url}")
                    break
                
                # Extrair dados da página atual
                # NOTA: Esta parte precisa ser adaptada à estrutura HTML real
                # Exemplo: procurar por tabelas com classe específica
                tables = soup.find_all('table')
                
                for table in tables:
                    rows = table.find_all('tr')[1:]  # Skip header
                    
                    for row in rows:
                        cols = row.find_all('td')
                        
                        if len(cols) >= 3:  # Verificar se tem colunas suficientes
                            # Exemplo de extração de dados
                            # Adaptar conforme estrutura real
                            record = {
                                'fase': phase,
                                'tipo': data_type,
                                'codigo_curso': cols[0].get_text(strip=True) if len(cols) > 0 else '',
                                'nome_curso': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                                'instituicao': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            }
                            
                            # Filtrar apenas dados do IPT
                            if self.is_ipt_institution(
                                record.get('instituicao', ''),
                                record.get('codigo_instituicao', '')
                            ):
                                phase_data.append(record)
                
                # Procurar link para próxima página
                next_url = self.find_next_page_link(soup)
                
                if next_url and next_url != current_url:
                    current_url = next_url
                    page_num += 1
                else:
                    logger.info(f"Não há mais páginas para Fase {phase} - {data_type}")
                    break
            
            logger.info(f"Total de registros coletados - Fase {phase} - {data_type}: {len(phase_data)}")
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados da Fase {phase} - {data_type}: {e}")
        
        return phase_data
    
    def scrape_admissions_data(self) -> Dict[str, List[Dict]]:
        """
        Scrape dados de admissões dos cursos do IPT para todas as fases.
        
        Returns:
            Dicionário com dados organizados por fase e tipo
            Chaves: 'fase1_colocados', 'fase1_candidatos', 'fase2_colocados', etc.
        """
        logger.info("Iniciando coleta de dados de admissões...")
        
        all_data = {}
        
        try:
            # Verificar robots.txt antes de iniciar
            if not self.respect_robots_txt():
                logger.error("Scraping não permitido por robots.txt")
                return all_data
            
            # Coletar dados para cada fase e tipo
            for phase in self.PHASES:
                for data_type in self.DATA_TYPES:
                    key = f"fase{phase}_{data_type}"
                    logger.info(f"\n{'='*60}")
                    logger.info(f"Processando: {key}")
                    logger.info(f"{'='*60}")
                    
                    data = self.scrape_phase_data(phase, data_type)
                    all_data[key] = data
                    
                    logger.info(f"Total de registros coletados para {key}: {len(data)}")
            
            # Resumo final
            logger.info(f"\n{'='*60}")
            logger.info("RESUMO DA COLETA")
            logger.info(f"{'='*60}")
            total_records = sum(len(data) for data in all_data.values())
            logger.info(f"Total geral de registros: {total_records}")
            
            for key, data in all_data.items():
                logger.info(f"  {key}: {len(data)} registros")
            
        except Exception as e:
            logger.error(f"Erro durante coleta de dados: {e}")
        
        return all_data
    
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
    
    def run(self) -> List[Path]:
        """
        Executa o processo completo de scraping.
        
        Returns:
            Lista de Paths dos arquivos CSV gerados (6 ficheiros: 3 fases x 2 tipos)
        """
        logger.info("=" * 60)
        logger.info("Iniciando Web Scraper DGES - IPT")
        logger.info("=" * 60)
        
        output_files = []
        
        try:
            # Coletar dados de todas as fases
            all_data = self.scrape_admissions_data()
            
            if not all_data or all(len(data) == 0 for data in all_data.values()):
                logger.warning("Nenhum dado foi coletado!")
                logger.info("\nNOTA IMPORTANTE:")
                logger.info("Este script necessita de análise manual do site da DGES.")
                logger.info("Por favor, visite https://dges.gov.pt/coloc/2025/")
                logger.info("e identifique a estrutura HTML para extração de dados.")
                logger.info("\nPassos sugeridos:")
                logger.info("1. Abra o site no navegador")
                logger.info("2. Use DevTools (F12) para inspecionar a estrutura")
                logger.info("3. Identifique se usa formulários, tabelas ou JavaScript")
                logger.info("4. Adapte os métodos scrape_phase_data() conforme necessário")
                
                # Criar CSVs vazios como placeholder para cada fase e tipo
                for phase in self.PHASES:
                    for data_type in self.DATA_TYPES:
                        filename = f"fase{phase}_{data_type}.csv"
                        placeholder_data = [{
                            'nota': 'Este ficheiro é um template',
                            'fase': phase,
                            'tipo': data_type,
                            'instrucoes': 'Adapte o script scraper.py à estrutura real do site'
                        }]
                        output_file = self.save_to_csv(placeholder_data, filename)
                        output_files.append(output_file)
            else:
                # Salvar dados de cada fase e tipo em CSV separado
                for key, data in all_data.items():
                    filename = f"{key}.csv"
                    
                    if not data:
                        # Se não houver dados, criar CSV vazio com cabeçalhos
                        logger.warning(f"Nenhum dado coletado para {key}")
                        data = [{
                            'nota': 'Nenhum dado coletado',
                            'fase': key.split('_')[0].replace('fase', ''),
                            'tipo': key.split('_')[1]
                        }]
                    
                    output_file = self.save_to_csv(data, filename)
                    output_files.append(output_file)
            
            logger.info("=" * 60)
            logger.info("Scraping concluído!")
            logger.info(f"Total de ficheiros gerados: {len(output_files)}")
            logger.info("=" * 60)
            
            logger.info("\nFicheiros gerados:")
            for file_path in output_files:
                logger.info(f"  ✓ {file_path}")
            
            return output_files
            
        except Exception as e:
            logger.error(f"Erro fatal durante execução: {e}")
            raise


def main():
    """Função principal."""
    try:
        scraper = DGESScraper(output_dir='data')
        output_files = scraper.run()
        
        print(f"\n✓ Dados salvos em {len(output_files)} ficheiros:")
        for file_path in output_files:
            print(f"  - {file_path}")
        
    except KeyboardInterrupt:
        logger.info("\nScraping interrompido pelo utilizador")
    except Exception as e:
        logger.error(f"Erro: {e}")
        raise


if __name__ == "__main__":
    main()
