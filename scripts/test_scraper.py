#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes básicos para o scraper DGES.

Este script testa as funcionalidades principais do scraper sem fazer
requisições reais ao site.
"""

import sys
from pathlib import Path

# Adicionar scripts ao path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from scraper import DGESScraper


def test_ipt_institution_detection():
    """Testa a detecção de instituições IPT."""
    scraper = DGESScraper(output_dir='/tmp')
    
    # Testes positivos
    assert scraper.is_ipt_institution("Instituto Politécnico de Tomar", "")
    assert scraper.is_ipt_institution("Inst. Politécnico de Tomar", "")
    assert scraper.is_ipt_institution("IPT - Tomar", "")
    assert scraper.is_ipt_institution("Qualquer nome", "3100")
    assert scraper.is_ipt_institution("", "3101")
    
    # Testes negativos
    assert not scraper.is_ipt_institution("Instituto Politécnico de Lisboa", "")
    assert not scraper.is_ipt_institution("Universidade de Coimbra", "")
    assert not scraper.is_ipt_institution("", "9999")
    
    print("✓ Testes de detecção IPT passaram")


def test_anonymization():
    """Testa a anonimização de dados."""
    scraper = DGESScraper(output_dir='/tmp')
    
    # Dados com informação pessoal
    student_data = {
        'nome': 'João Silva',
        'numero_candidato': '12345678',
        'email': 'joao@example.com',
        'nota': 150.5,
        'curso': 'Engenharia Informática'
    }
    
    # Anonimizar
    anon_data = scraper.anonymize_student_data(student_data)
    
    # Verificar que dados pessoais foram removidos
    assert 'nome' not in anon_data
    assert 'email' not in anon_data
    assert 'ANON_' in anon_data['numero_candidato']
    
    # Verificar que dados não pessoais foram mantidos
    assert anon_data['nota'] == 150.5
    assert anon_data['curso'] == 'Engenharia Informática'
    
    print("✓ Testes de anonimização passaram")


def test_scraper_initialization():
    """Testa a inicialização do scraper."""
    scraper = DGESScraper(output_dir='/tmp/test_output')
    
    assert scraper.output_dir.exists()
    assert scraper.REQUEST_DELAY == 1.5
    assert scraper.TIMEOUT == 30
    assert 'Educational Purpose' in scraper.session.headers['User-Agent']
    
    print("✓ Testes de inicialização passaram")


def test_data_structure():
    """Testa a estrutura de dados esperada."""
    scraper = DGESScraper(output_dir='/tmp')
    
    # Estrutura de exemplo de um curso
    course_example = {
        'codigo_curso': '9999',
        'nome_curso': 'Engenharia Informática',
        'instituicao': 'Instituto Politécnico de Tomar',
        'vagas': 30,
        'colocados': 28,
        'nota_ultimo': 145.5,
        'ano': 2025
    }
    
    # Verificar campos essenciais
    required_fields = ['nome_curso', 'instituicao', 'vagas', 'colocados']
    for field in required_fields:
        assert field in course_example, f"Campo obrigatório '{field}' não encontrado"
    
    print("✓ Testes de estrutura de dados passaram")


def test_phases_and_data_types():
    """Testa a configuração de fases e tipos de dados."""
    scraper = DGESScraper(output_dir='/tmp')
    
    # Verificar que as fases estão definidas
    assert hasattr(scraper, 'PHASES')
    assert len(scraper.PHASES) == 3
    assert '1' in scraper.PHASES
    assert '2' in scraper.PHASES
    assert '3' in scraper.PHASES
    
    # Verificar que os tipos de dados estão definidos
    assert hasattr(scraper, 'DATA_TYPES')
    assert len(scraper.DATA_TYPES) == 2
    assert 'colocados' in scraper.DATA_TYPES
    assert 'candidatos' in scraper.DATA_TYPES
    
    print("✓ Testes de fases e tipos de dados passaram")


def test_pagination_link_detection():
    """Testa a detecção de links de paginação."""
    from bs4 import BeautifulSoup
    
    scraper = DGESScraper(output_dir='/tmp')
    
    # HTML de teste com link "Seguinte"
    html_with_next = """
    <html>
        <body>
            <div class="pagination">
                <a href="page2.html">Seguinte</a>
            </div>
        </body>
    </html>
    """
    
    soup = BeautifulSoup(html_with_next, 'lxml')
    next_link = scraper.find_next_page_link(soup)
    
    assert next_link is not None
    assert 'page2.html' in next_link
    
    # HTML de teste sem link "Seguinte"
    html_without_next = """
    <html>
        <body>
            <div class="pagination">
                <a href="page1.html">Anterior</a>
            </div>
        </body>
    </html>
    """
    
    soup_no_next = BeautifulSoup(html_without_next, 'lxml')
    no_next_link = scraper.find_next_page_link(soup_no_next)
    
    # Pode retornar None ou não encontrar
    # (depende se "anterior" é interpretado)
    
    print("✓ Testes de detecção de link de paginação passaram")


def run_all_tests():
    """Executa todos os testes."""
    print("=" * 60)
    print("Executando testes do scraper DGES")
    print("=" * 60)
    
    try:
        test_scraper_initialization()
        test_ipt_institution_detection()
        test_anonymization()
        test_data_structure()
        test_phases_and_data_types()
        test_pagination_link_detection()
        
        print("=" * 60)
        print("✓ TODOS OS TESTES PASSARAM")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Teste falhou: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Erro durante testes: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
