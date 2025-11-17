# Como Usar o Web Scraper DGES - Guia Rápido

## ⚠️ IMPORTANTE: Navegue para o Diretório Correto!

**ANTES** de executar qualquer comando, certifique-se de que está no diretório raiz do projeto:

```bash
# Navegue para o diretório do projeto
cd /caminho/para/PYTHON-IPT-Student-Enrollment-Web-Scraping

# Verifique que está no lugar certo - este comando deve funcionar:
ls environment.yml requirements.txt scripts/scraper.py

# Se obtiver "No such file or directory", está no lugar errado!
# Use 'pwd' para ver onde está e navegue para o diretório correto
```

### Como Encontrar o Diretório Correto?

```bash
# Se clonou o repositório mas não sabe onde:
find ~ -name "environment.yml" -path "*/PYTHON-IPT-Student-Enrollment-Web-Scraping/*" 2>/dev/null

# O comando acima mostrará o caminho completo. Depois:
cd /caminho/mostrado/pelo/comando/acima
```

## Pré-requisitos

Certifique-se de ter Python 3.13+ instalado.

## Instalação

### Verificação Rápida

Primeiro, execute o script de verificação para garantir que tudo está configurado:

```bash
python scripts/check_setup.py
```

Se encontrar problemas, consulte TROUBLESHOOTING.md.

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

### ❌ "file not found" ou "No such file or directory"

**Este é o erro mais comum!**

**Causa**: Está a executar os comandos no diretório errado.

**Solução**:
```bash
# 1. Verifique onde está
pwd

# 2. Liste os ficheiros - deve ver environment.yml, requirements.txt, etc.
ls -la

# 3. Se NÃO vir esses ficheiros, navegue para o diretório correto:
cd /caminho/para/PYTHON-IPT-Student-Enrollment-Web-Scraping

# 4. Confirme que está no lugar certo:
ls environment.yml && echo "✓ Diretório correto!" || echo "✗ Ainda errado!"
```

📖 **Para mais soluções detalhadas, consulte**: `TROUBLESHOOTING.md`

## Questões?

Consulte a documentação completa em `docs/` ou contacte o professor orientador.

---

**Projeto**: Big Data Processing - Análise de Admissões IPT  
**Propósito**: Apenas educacional  
**Autor**: Mestrado em CS
