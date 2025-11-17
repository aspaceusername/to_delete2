#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do scraper DGES.

Este script demonstra como usar o DGESScraper de forma programática
e como processar os dados coletados.
"""

import sys
from pathlib import Path

# Adicionar scripts ao path
sys.path.insert(0, str(Path(__file__).parent))

from scraper import DGESScraper
import pandas as pd


def example_basic_usage():
    """Exemplo básico de uso do scraper."""
    print("=" * 60)
    print("Exemplo 1: Uso Básico - Multi-Fase")
    print("=" * 60)
    
    # Criar scraper
    scraper = DGESScraper(output_dir='../data')
    
    # Executar (gera 6 CSVs)
    output_files = scraper.run()
    
    print(f"\nDados salvos em {len(output_files)} ficheiros:")
    for file_path in output_files:
        print(f"  - {file_path}")


def example_custom_usage():
    """Exemplo de uso customizado do scraper."""
    print("\n" + "=" * 60)
    print("Exemplo 2: Uso Customizado")
    print("=" * 60)
    
    # Criar scraper
    scraper = DGESScraper(output_dir='../data')
    
    # Dados de exemplo (em produção, viria de scrape_courses)
    example_data = [
        {
            'codigo_curso': '9853',
            'nome_curso': 'Engenharia Informática',
            'instituicao': 'Instituto Politécnico de Tomar',
            'codigo_instituicao': '3100',
            'vagas_totais': 30,
            'vagas_colocadas': 28,
            'nota_ultimo': 145.5,
            'nota_primeiro': 185.0,
            'ano': 2025
        },
        {
            'codigo_curso': '9854',
            'nome_curso': 'Gestão de Empresas',
            'instituicao': 'Instituto Politécnico de Tomar',
            'codigo_instituicao': '3100',
            'vagas_totais': 25,
            'vagas_colocadas': 22,
            'nota_ultimo': 138.0,
            'nota_primeiro': 178.5,
            'ano': 2025
        },
        {
            'codigo_curso': '9855',
            'nome_curso': 'Design de Comunicação',
            'instituicao': 'Instituto Politécnico de Tomar',
            'codigo_instituicao': '3100',
            'vagas_totais': 20,
            'vagas_colocadas': 15,
            'nota_ultimo': 125.0,
            'nota_primeiro': 165.0,
            'ano': 2025
        }
    ]
    
    # Filtrar apenas IPT
    ipt_data = [
        course for course in example_data 
        if scraper.is_ipt_institution(
            course['instituicao'], 
            course.get('codigo_instituicao', '')
        )
    ]
    
    print(f"\nTotal de cursos IPT: {len(ipt_data)}")
    
    # Salvar
    output_file = scraper.save_to_csv(ipt_data, 'exemplo_ipt_dados.csv')
    print(f"Dados salvos em: {output_file}")
    
    return ipt_data


def example_data_analysis(data):
    """Exemplo de análise básica dos dados."""
    print("\n" + "=" * 60)
    print("Exemplo 3: Análise Básica de Dados")
    print("=" * 60)
    
    # Converter para DataFrame
    df = pd.DataFrame(data)
    
    # Calcular estatísticas
    df['vagas_nao_preenchidas'] = df['vagas_totais'] - df['vagas_colocadas']
    df['taxa_ocupacao'] = (df['vagas_colocadas'] / df['vagas_totais'] * 100).round(2)
    df['amplitude_notas'] = df['nota_primeiro'] - df['nota_ultimo']
    
    print("\n📊 Estatísticas Gerais:")
    print(f"Total de cursos: {len(df)}")
    print(f"Total de vagas: {df['vagas_totais'].sum()}")
    print(f"Total de colocados: {df['vagas_colocadas'].sum()}")
    print(f"Vagas não preenchidas: {df['vagas_nao_preenchidas'].sum()}")
    print(f"Taxa média de ocupação: {df['taxa_ocupacao'].mean():.2f}%")
    
    print("\n📈 Top 3 Cursos com Mais Colocados:")
    top_courses = df.nlargest(3, 'vagas_colocadas')[['nome_curso', 'vagas_colocadas']]
    for idx, row in top_courses.iterrows():
        print(f"  - {row['nome_curso']}: {row['vagas_colocadas']} alunos")
    
    print("\n📉 Cursos com Mais Vagas Não Preenchidas:")
    unfilled = df.nlargest(3, 'vagas_nao_preenchidas')[['nome_curso', 'vagas_nao_preenchidas']]
    for idx, row in unfilled.iterrows():
        print(f"  - {row['nome_curso']}: {row['vagas_nao_preenchidas']} vagas")
    
    print("\n🎓 Notas de Entrada:")
    print(f"Nota média (último colocado): {df['nota_ultimo'].mean():.2f}")
    print(f"Nota mínima (último colocado): {df['nota_ultimo'].min():.2f}")
    print(f"Nota máxima (último colocado): {df['nota_ultimo'].max():.2f}")
    
    return df


def example_anonymization():
    """Exemplo de anonimização de dados."""
    print("\n" + "=" * 60)
    print("Exemplo 4: Anonimização de Dados")
    print("=" * 60)
    
    scraper = DGESScraper(output_dir='../data')
    
    # Dados com informação pessoal (EXEMPLO - não coletar na realidade)
    student_data = {
        'nome': 'João Silva',
        'numero_candidato': '12345678',
        'email': 'joao@example.com',
        'nota': 150.5,
        'curso': 'Engenharia Informática',
        'colocacao': 15
    }
    
    print("\n🔒 Dados Originais:")
    for key, value in student_data.items():
        print(f"  {key}: {value}")
    
    # Anonimizar
    anon_data = scraper.anonymize_student_data(student_data)
    
    print("\n✓ Dados Anonimizados:")
    for key, value in anon_data.items():
        print(f"  {key}: {value}")
    
    print("\n📝 Nota: Dados pessoais (nome, email) foram removidos.")
    print("Número de candidato foi convertido em hash anónimo.")


def example_multi_phase_analysis():
    """Exemplo de análise de dados multi-fase."""
    print("\n" + "=" * 60)
    print("Exemplo 5: Análise de Dados Multi-Fase")
    print("=" * 60)
    
    scraper = DGESScraper(output_dir='../data')
    
    # Dados de exemplo para demonstração
    # Em produção, estes viriam do scraping real
    example_data = {
        'fase1_colocados': [
            {'curso': 'Engenharia Informática', 'colocados': 28, 'fase': '1'},
            {'curso': 'Gestão de Empresas', 'colocados': 22, 'fase': '1'}
        ],
        'fase1_candidatos': [
            {'curso': 'Engenharia Informática', 'candidatos': 45, 'fase': '1'},
            {'curso': 'Gestão de Empresas', 'candidatos': 35, 'fase': '1'}
        ],
        'fase2_colocados': [
            {'curso': 'Engenharia Informática', 'colocados': 2, 'fase': '2'},
            {'curso': 'Gestão de Empresas', 'colocados': 3, 'fase': '2'}
        ],
        'fase2_candidatos': [
            {'curso': 'Engenharia Informática', 'candidatos': 15, 'fase': '2'},
            {'curso': 'Gestão de Empresas', 'candidatos': 12, 'fase': '2'}
        ],
        'fase3_colocados': [],
        'fase3_candidatos': []
    }
    
    print("\n📊 Resumo por Fase:")
    for phase in ['1', '2', '3']:
        colocados_key = f'fase{phase}_colocados'
        candidatos_key = f'fase{phase}_candidatos'
        
        total_colocados = sum(item.get('colocados', 0) for item in example_data.get(colocados_key, []))
        total_candidatos = sum(item.get('candidatos', 0) for item in example_data.get(candidatos_key, []))
        
        print(f"\nFase {phase}:")
        print(f"  Total de colocados: {total_colocados}")
        print(f"  Total de candidatos: {total_candidatos}")
        if total_candidatos > 0:
            taxa = (total_colocados / total_candidatos * 100)
            print(f"  Taxa de colocação: {taxa:.1f}%")
    
    print("\n💡 Insight: A maioria dos alunos é colocada na Fase 1.")
    print("   As vagas restantes são preenchidas nas fases 2 e 3.")


def main():
    """Função principal - executa todos os exemplos."""
    print("\n" + "=" * 60)
    print("EXEMPLOS DE USO DO SCRAPER DGES - MULTI-FASE")
    print("=" * 60)
    
    try:
        # Exemplo 1: Uso básico
        # Descomente a linha abaixo para testar (requer conexão ao site)
        # example_basic_usage()
        
        # Exemplo 2: Uso customizado
        data = example_custom_usage()
        
        # Exemplo 3: Análise de dados
        df = example_data_analysis(data)
        
        # Exemplo 4: Anonimização
        example_anonymization()
        
        # Exemplo 5: Análise multi-fase
        example_multi_phase_analysis()
        
        print("\n" + "=" * 60)
        print("✓ Todos os exemplos executados com sucesso!")
        print("=" * 60)
        print("\nPróximos passos:")
        print("1. Analise o site da DGES para identificar a estrutura HTML")
        print("2. Adapte o método scrape_phase_data() em scraper.py")
        print("3. Execute o scraper: python scripts/scraper.py")
        print("4. Analise os 6 CSVs gerados (3 fases x 2 tipos)")
        print("\nConsulte docs/IMPLEMENTATION_GUIDE.md para mais detalhes.")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
