#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificação de Configuração
Verifica se o ambiente está configurado corretamente para executar o projeto.
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Imprime cabeçalho formatado."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_check(passed, message):
    """Imprime resultado de uma verificação."""
    symbol = "✓" if passed else "✗"
    status = "OK" if passed else "FALHOU"
    print(f"{symbol} [{status}] {message}")
    return passed

def check_directory():
    """Verifica se está no diretório correto do projeto."""
    print_header("Verificação de Diretório")
    
    current_dir = Path.cwd()
    print(f"Diretório atual: {current_dir}")
    
    required_files = [
        'environment.yml',
        'requirements.txt',
        'README.md',
        'scripts/scraper.py'
    ]
    
    all_exist = True
    for file in required_files:
        file_path = current_dir / file
        exists = file_path.exists()
        all_exist = all_exist and exists
        print_check(exists, f"Ficheiro encontrado: {file}")
    
    if all_exist:
        print("\n✓ Está no diretório correto do projeto!")
    else:
        print("\n✗ ERRO: Não está no diretório do projeto!")
        print("\nSolução:")
        print("  Navegue para o diretório raiz do projeto:")
        print("  cd /caminho/para/PYTHON-IPT-Student-Enrollment-Web-Scraping")
        print("\nConsulte TROUBLESHOOTING.md para mais informações.")
    
    return all_exist

def check_python_version():
    """Verifica a versão do Python."""
    print_header("Verificação do Python")
    
    version = sys.version_info
    print(f"Versão do Python: {version.major}.{version.minor}.{version.micro}")
    
    required_major = 3
    required_minor = 8
    
    is_valid = version.major >= required_major and version.minor >= required_minor
    
    print_check(
        is_valid,
        f"Python {required_major}.{required_minor}+ requerido"
    )
    
    if not is_valid:
        print(f"\n✗ ERRO: Python {required_major}.{required_minor}+ necessário")
        print(f"  Versão atual: {version.major}.{version.minor}.{version.micro}")
        print("\nSolução:")
        print("  Instale Python 3.8 ou superior")
        print("  https://www.python.org/downloads/")
    
    return is_valid

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    print_header("Verificação de Dependências")
    
    required_modules = [
        ('requests', 'requests'),
        ('bs4', 'beautifulsoup4'),
        ('pandas', 'pandas'),
        ('lxml', 'lxml'),
        ('numpy', 'numpy'),
    ]
    
    all_installed = True
    missing_modules = []
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print_check(True, f"Módulo instalado: {package_name}")
        except ImportError:
            print_check(False, f"Módulo NÃO instalado: {package_name}")
            all_installed = False
            missing_modules.append(package_name)
    
    if not all_installed:
        print("\n✗ ERRO: Dependências em falta!")
        print("\nSolução:")
        print("  Opção 1 - Usar conda:")
        print("    conda env create -f environment.yml")
        print("    conda activate ipt-admissions-analysis")
        print("\n  Opção 2 - Usar pip:")
        print("    pip install -r requirements.txt")
        print("\n  Módulos em falta:")
        for module in missing_modules:
            print(f"    - {module}")
    
    return all_installed

def check_data_directory():
    """Verifica se o diretório de dados existe."""
    print_header("Verificação de Diretórios")
    
    data_dir = Path('data')
    exists = data_dir.exists()
    
    print_check(exists, "Diretório 'data/' existe")
    
    if exists:
        print(f"  Localização: {data_dir.absolute()}")
        csv_files = list(data_dir.glob('*.csv'))
        print(f"  Ficheiros CSV encontrados: {len(csv_files)}")
    else:
        print("\n⚠ Aviso: Diretório 'data/' não encontrado")
        print("  Será criado automaticamente ao executar o scraper")
    
    return exists

def check_internet_connection():
    """Verifica conexão à internet."""
    print_header("Verificação de Conectividade")
    
    try:
        import socket
        socket.create_connection(("www.google.com", 80), timeout=5)
        print_check(True, "Conexão à internet disponível")
        return True
    except OSError:
        print_check(False, "Sem conexão à internet")
        print("\n⚠ Aviso: Necessita de internet para fazer web scraping")
        return False

def check_dges_access():
    """Verifica se consegue aceder ao site da DGES."""
    print_header("Verificação de Acesso ao Site DGES")
    
    try:
        import requests
        url = "https://dges.gov.pt"
        response = requests.get(url, timeout=10)
        can_access = response.status_code == 200
        
        print_check(can_access, f"Acesso ao site DGES (status: {response.status_code})")
        
        if not can_access:
            print("\n⚠ Aviso: Problema ao aceder ao site da DGES")
            print("  Possíveis causas:")
            print("  - Site temporariamente indisponível")
            print("  - Firewall ou proxy bloqueando")
            print("  - Região geográfica restrita")
        
        return can_access
    except ImportError:
        print_check(False, "Módulo 'requests' não instalado")
        return False
    except Exception as e:
        print_check(False, f"Erro ao aceder DGES: {str(e)[:50]}")
        return False

def main():
    """Função principal."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "VERIFICAÇÃO DE CONFIGURAÇÃO DO PROJETO" + " " * 10 + "║")
    print("║" + " " * 12 + "IPT Admissions Analysis Web Scraper" + " " * 11 + "║")
    print("╚" + "═" * 58 + "╝")
    
    checks = []
    
    # Executar todas as verificações
    checks.append(("Diretório", check_directory()))
    checks.append(("Python", check_python_version()))
    checks.append(("Dependências", check_dependencies()))
    checks.append(("Diretório de Dados", check_data_directory()))
    checks.append(("Internet", check_internet_connection()))
    checks.append(("Acesso DGES", check_dges_access()))
    
    # Resumo
    print_header("Resumo")
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\nVerificações passadas: {passed}/{total}")
    
    for name, result in checks:
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {name}")
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print("\n🎉 SUCESSO! Tudo está configurado corretamente!")
        print("\nPróximos passos:")
        print("  1. Execute o scraper:")
        print("     python scripts/scraper.py")
        print("\n  2. Ou execute os testes:")
        print("     python scripts/test_scraper.py")
    else:
        print("\n⚠ ATENÇÃO! Alguns problemas encontrados.")
        print("\nConsulte TROUBLESHOOTING.md para soluções:")
        print("  cat TROUBLESHOOTING.md")
        print("\nOu veja a documentação:")
        print("  cat QUICK_START.md")
    
    print("=" * 60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nVerificação interrompida pelo utilizador.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Erro inesperado: {e}")
        sys.exit(1)
