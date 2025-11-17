# Resolução de Problemas (Troubleshooting)

## Problema: "file not found" ou "No such file or directory"

### Sintomas
```bash
EnvironmentFileNotFound: '/home/ruben/Documents/Mestrado/Software Engineering/store/environment.yml' file not found
```
ou
```bash
ERROR: Could not open requirements file: [Errno 2] Aucun fichier ou dossier de ce nom: 'requirements.txt'
```
ou
```bash
python: can't open file 'scripts/scraper.py': [Errno 2] No such file or directory
```

### ❌ Causa
Está a executar os comandos **no diretório errado**. Os comandos devem ser executados a partir do **diretório raiz do projeto**.

### ✅ Solução

1. **Primeiro, navegue para o diretório correto do projeto**:

   ```bash
   # Exemplo: se clonou o repositório na sua pasta de documentos
   cd ~/Documents/PYTHON-IPT-Student-Enrollment-Web-Scraping
   
   # OU se está noutro local, navegue para lá
   cd /caminho/para/PYTHON-IPT-Student-Enrollment-Web-Scraping
   ```

2. **Verifique que está no diretório correto**:

   ```bash
   # Liste os ficheiros - deve ver environment.yml, requirements.txt, etc.
   ls -la
   
   # Deve ver algo como:
   # .git
   # .github
   # README.md
   # environment.yml
   # requirements.txt
   # scripts/
   # data/
   # docs/
   ```

3. **Agora execute os comandos**:

   ```bash
   # Criar ambiente conda
   conda env create -f environment.yml
   
   # Ativar ambiente
   conda activate ipt-admissions-analysis
   
   # OU instalar com pip
   pip install -r requirements.txt
   
   # Executar o scraper
   python scripts/scraper.py
   ```

### Como Identificar o Diretório Correto

O diretório correto é aquele que contém os seguintes ficheiros:
- ✓ `environment.yml`
- ✓ `requirements.txt`
- ✓ `README.md`
- ✓ `scripts/` (pasta)
- ✓ `data/` (pasta)

**Comando rápido para verificar**:
```bash
# Se este comando mostrar todos os ficheiros, está no lugar certo
ls environment.yml requirements.txt scripts/scraper.py 2>/dev/null && echo "✓ Diretório correto!" || echo "✗ Diretório errado - navegue para o projeto"
```

---

## Outros Problemas Comuns

### Problema: "Module not found" ou "No module named..."

#### Causa
Dependências não instaladas ou ambiente virtual não ativado.

#### Solução
```bash
# Se usar conda
conda activate ipt-admissions-analysis
conda env create -f environment.yml  # se ainda não criou

# Se usar pip
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

### Problema: "Permission denied" ao executar scripts

#### Solução
```bash
# Linux/Mac - tornar o script executável
chmod +x scripts/scraper.py

# Ou executar com python explicitamente
python scripts/scraper.py
```

---

### Problema: Conda não reconhece environment.yml

#### Sintomas
```bash
conda env create -f environment.yml
# Erro: EnvironmentFileNotFound
```

#### Soluções

1. **Verifique que está no diretório correto** (veja acima)

2. **Verifique que o conda está instalado**:
   ```bash
   conda --version
   ```

3. **Use o caminho completo se necessário**:
   ```bash
   conda env create -f /caminho/completo/para/environment.yml
   ```

---

### Problema: "Connection error" ou timeout ao fazer scraping

#### Causas Possíveis
- Sem conexão à internet
- Site da DGES indisponível
- Firewall ou proxy bloqueando
- IP bloqueado pelo site

#### Soluções
```bash
# Verificar conexão
ping dges.gov.pt

# Verificar se o site está disponível
curl -I https://dges.gov.pt/coloc/2025/

# Ajustar timeout no código se necessário
# Edite scripts/scraper.py e aumente TIMEOUT = 30 para TIMEOUT = 60
```

---

### Problema: Python não encontrado

#### Solução
```bash
# Verificar versão do Python
python --version
python3 --version

# Se não instalado, instale:
# Ubuntu/Debian:
sudo apt-get install python3 python3-pip

# macOS (com Homebrew):
brew install python3

# Windows: baixe de python.org
```

---

### Problema: Git não reconhece o repositório

#### Sintomas
```bash
fatal: not a git repository (or any of the parent directories): .git
```

#### Solução
```bash
# Clone o repositório primeiro
git clone https://github.com/aspaceusername/PYTHON-IPT-Student-Enrollment-Web-Scraping.git

# Navegue para dentro
cd PYTHON-IPT-Student-Enrollment-Web-Scraping

# Agora execute os comandos
```

---

## Checklist de Verificação Rápida

Antes de pedir ajuda, verifique:

- [ ] Estou no diretório raiz do projeto?
  ```bash
  pwd
  ls environment.yml requirements.txt
  ```

- [ ] Instalei as dependências?
  ```bash
  pip list | grep requests
  pip list | grep beautifulsoup4
  ```

- [ ] Tenho Python 3.13+ instalado?
  ```bash
  python --version
  ```

- [ ] O ambiente virtual/conda está ativado?
  ```bash
  which python
  echo $CONDA_DEFAULT_ENV
  ```

- [ ] Tenho conexão à internet?
  ```bash
  ping -c 3 google.com
  ```

---

## Ainda com Problemas?

### Passo 1: Recomeçar do Zero
```bash
# 1. Navegue para um diretório limpo
cd ~/Documents/

# 2. Clone o repositório novamente
git clone https://github.com/aspaceusername/PYTHON-IPT-Student-Enrollment-Web-Scraping.git

# 3. Entre no diretório
cd PYTHON-IPT-Student-Enrollment-Web-Scraping

# 4. Verifique que está no lugar certo
ls -la

# 5. Crie o ambiente
conda env create -f environment.yml
conda activate ipt-admissions-analysis

# 6. Execute o scraper
python scripts/scraper.py
```

### Passo 2: Verificação de Diagnóstico
Execute o script de diagnóstico:
```bash
python scripts/check_setup.py
```

### Passo 3: Contactar Suporte
Se ainda tiver problemas, forneça estas informações:
```bash
# Recolha informações do sistema
python --version
conda --version
pwd
ls -la
pip list
```

---

**Última Atualização**: 2025-11-17  
**Projeto**: IPT Admissions Analysis  
**Propósito**: Educacional
