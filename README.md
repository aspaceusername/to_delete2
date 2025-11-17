# IPT Admissions Analysis - Web Scraping Project

## Visão Geral do Projeto

Este projeto faz parte do mestrado em Engenharia Informática: IOT - Internet das Coisas e tem como objetivo coletar e analisar dados de admissões do Instituto Politécnico de Tomar (IPT) a partir do site oficial da DGES (Direção-Geral do Ensino Superior).

## Objetivos

1. **Coleta de Dados**: Obter dados necessários do site oficial da DGES para as admissões de 2025
2. **Preparação de Dados**: Limpar, anonimizar, transformar e organizar os dados brutos
3. **Análise Exploratória de Dados (EDA)**: Identificar tendências e padrões
4. **Geração de Insights**: Formular recomendações sobre admissões e retenção de estudantes
5. **Comunicação**: Apresentar descobertas num relatório ou dashboard interativo

## Estrutura do Projeto

```
.
├── scripts/          # Scripts de scraping e análise
│   └── scraper.py   # Script principal de web scraping
├── data/            # Dados coletados (excluídos do git)
├── docs/            # Documentação adicional
├── environment.yml  # Dependências do conda
└── requirements.txt # Dependências do pip
```

## Instalação

⚠️ **IMPORTANTE**: Certifique-se de que está no **diretório raiz do projeto** antes de executar estes comandos!

```bash
# PRIMEIRO: Navegue para o diretório do projeto
cd /caminho/para/PYTHON-IPT-Student-Enrollment-Web-Scraping

# Verifique que está no lugar certo
ls environment.yml requirements.txt  # Deve mostrar os ficheiros
```

### Usando Conda (Recomendado)

```bash
conda env create -f environment.yml
conda activate ipt-admissions-analysis
```

### Usando pip

```bash
pip install -r requirements.txt
```

### Verificar Configuração

Execute o script de verificação para confirmar que tudo está configurado:

```bash
python scripts/check_setup.py
```

## Uso

### Web Scraping

Para coletar dados do site da DGES:

```bash
python scripts/scraper.py
```

O script irá:
- Respeitar o robots.txt e práticas éticas de scraping
- Implementar delays entre requisições para não sobrecarregar o servidor
- Filtrar dados específicos do IPT
- Anonimizar dados pessoais quando necessário
- Salvar os dados em formato CSV na pasta `data/`

### Configurações

O script usa as seguintes práticas éticas:
- Delay mínimo de 1 segundo entre requisições
- User-Agent identificável
- Respeito às regras de robots.txt
- Anonimização de dados pessoais

## Fonte de Dados

- **Fonte Primária**: DGES - Concurso Nacional de Acesso e Ingresso no Ensino Superior
- **URL**: https://dges.gov.pt/coloc/2025/
- **Técnica**: Web scraping usando Python (requests + BeautifulSoup)

## Notas Importantes

- Este projeto é **apenas para fins educacionais**
- A coleta de dados respeita práticas éticas de web scraping
- Dados pessoais são anonimizados para proteger a privacidade individual
- O foco está nos dados do Instituto Politécnico de Tomar (IPT)

## Questões de Investigação

O projeto procura responder a questões como:
- Quais cursos do IPT atraem mais estudantes?
- Como estão as notas de entrada em relação aos percentis nacionais?
- Por que alguns cursos têm vagas não preenchidas?
- Qual é o perfil típico do estudante que vem para o IPT?
- O IPT foi a primeira escolha dos alunos?
- Existem indicadores de possível abandono escolar?

## Resolução de Problemas

Se encontrar erros como:
- ❌ `EnvironmentFileNotFound: 'environment.yml' file not found`
- ❌ `Could not open requirements file: 'requirements.txt'`
- ❌ `can't open file 'scripts/scraper.py'`

**Causa**: Está a executar os comandos no diretório errado!

**Solução**: Navegue para o diretório raiz do projeto primeiro:
```bash
cd /caminho/para/PYTHON-IPT-Student-Enrollment-Web-Scraping
ls environment.yml  # Deve mostrar o ficheiro
```

📖 **Consulte TROUBLESHOOTING.md para mais soluções**: `cat TROUBLESHOOTING.md`

## Autor

Projeto desenvolvido como parte do mestrado em CS - Big Data Processing

## Licença

Este projeto é apenas para fins educacionais.
