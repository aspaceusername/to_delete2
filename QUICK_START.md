# Como Usar o Web Scraper DGES - Guia Rápido

## Pré-requisitos

Certifique-se de ter Python 3.13+ instalado.

## Instalação

### Opção 1: Usando Conda (Recomendado)

```bash
# Criar ambiente
conda env create -f environment.yml

# Ativar ambiente
conda activate ipt-admissions-analysis
```

### Opção 2: Usando pip

```bash
# Criar ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

## Uso Básico

### 1. Executar o Scraper

```bash
python scripts/scraper.py
```

**Nota**: Como o site da DGES requer análise manual da estrutura HTML, o script atual:
- Verifica o robots.txt
- Tenta aceder à página principal
- Cria um ficheiro CSV template
- Fornece instruções sobre próximos passos

### 2. Executar Testes

```bash
python scripts/test_scraper.py
```

Testa:
- ✓ Inicialização do scraper
- ✓ Detecção de instituições IPT
- ✓ Anonimização de dados
- ✓ Estrutura de dados

## Próximos Passos

### Para começar a coletar dados reais:

1. **Analise o site manualmente**:
   - Visite https://dges.gov.pt/coloc/2025/
   - Abra DevTools (F12)
   - Identifique a estrutura HTML dos dados

2. **Adapte o scraper**:
   - Edite `scripts/scraper.py`
   - Modifique o método `scrape_courses()`
   - Consulte `docs/IMPLEMENTATION_GUIDE.md` para exemplos

3. **Execute e valide**:
   ```bash
   python scripts/scraper.py
   ```

4. **Verifique os dados**:
   ```bash
   cat data/ipt_admissions_*.csv
   ```

## Estrutura de Ficheiros

```
.
├── scripts/
│   ├── scraper.py          # Script principal
│   └── test_scraper.py     # Testes unitários
├── data/                   # Dados coletados (não versionados)
├── docs/
│   ├── IMPLEMENTATION_GUIDE.md  # Guia de implementação
│   └── DATA_DICTIONARY.md       # Dicionário de dados
├── README.md               # Visão geral do projeto
├── environment.yml         # Dependências conda
└── requirements.txt        # Dependências pip
```

## Práticas Éticas Implementadas

✓ **Respeito ao robots.txt**
✓ **Rate limiting** (1.5s entre requisições)
✓ **User-Agent identificável**
✓ **Timeouts configuráveis**
✓ **Anonimização de dados pessoais**
✓ **Logging completo**

## Documentação Adicional

- `README.md` - Visão geral do projeto
- `docs/IMPLEMENTATION_GUIDE.md` - Como adaptar à estrutura real do site
- `docs/DATA_DICTIONARY.md` - Estrutura de dados esperada

## Resolução de Problemas

### "Module not found"
```bash
# Certifique-se de que instalou as dependências
pip install -r requirements.txt
```

### "Permission denied"
```bash
# Torne o script executável
chmod +x scripts/scraper.py
```

### "Connection error"
- Verifique conexão com internet
- Verifique se o site está disponível
- O site pode bloquear certos IPs/regiões

## Questões?

Consulte a documentação completa em `docs/` ou contacte o professor orientador.

---

**Projeto**: Big Data Processing - Análise de Admissões IPT  
**Propósito**: Apenas educacional  
**Autor**: Mestrado em CS
