# Guia de Web Scraping Multi-Fase

## Visão Geral

O scraper DGES foi atualizado para suportar a coleta de dados de **3 fases** de admissão, gerando **6 ficheiros CSV** distintos:

1. `fase1_colocados.csv` - Alunos admitidos na 1ª fase
2. `fase1_candidatos.csv` - Candidatos da 1ª fase
3. `fase2_colocados.csv` - Alunos admitidos na 2ª fase
4. `fase2_candidatos.csv` - Candidatos da 2ª fase
5. `fase3_colocados.csv` - Alunos admitidos na 3ª fase
6. `fase3_candidatos.csv` - Candidatos da 3ª fase

## Funcionalidades Principais

### 1. Suporte Multi-Fase

O scraper processa automaticamente as 3 fases de colocação do concurso nacional de acesso:

```python
# Configuração no DGESScraper
PHASES = ['1', '2', '3']  # 3 fases de admissão
DATA_TYPES = ['colocados', 'candidatos']  # admitidos e candidatos
```

### 2. Paginação Automática

A função `find_next_page_link()` detecta automaticamente links de paginação:

```python
def find_next_page_link(self, soup: BeautifulSoup) -> Optional[str]:
    """
    Procura por links com texto "Seguinte", "Next", "Próxima", etc.
    Retorna a URL da próxima página ou None se não houver.
    """
```

Palavras-chave suportadas:
- "Seguinte"
- "Next"
- "Próxima"
- "Proxima"
- ">"

### 3. Scraping por Fase

A função `scrape_phase_data()` processa uma fase específica com paginação automática:

```python
def scrape_phase_data(self, phase: str, data_type: str) -> List[Dict]:
    """
    Args:
        phase: Número da fase ('1', '2', ou '3')
        data_type: Tipo de dados ('colocados' ou 'candidatos')
    
    Returns:
        Lista de dicionários com dados da fase
    """
```

**Processo:**
1. Acede à URL da fase específica
2. Extrai dados da página atual
3. Procura link "Seguinte"
4. Se existir, vai para próxima página
5. Repete até não haver mais páginas
6. Retorna todos os dados coletados

## Como Usar

### Execução Básica

```bash
python scripts/scraper.py
```

Isto irá:
- Processar todas as 3 fases
- Para cada fase, coletar dados de colocados e candidatos
- Gerar 6 ficheiros CSV na pasta `data/`

### Uso Programático

```python
from scraper import DGESScraper

# Criar scraper
scraper = DGESScraper(output_dir='data')

# Executar (gera 6 CSVs)
output_files = scraper.run()

print(f"Gerados {len(output_files)} ficheiros:")
for file in output_files:
    print(f"  - {file}")
```

### Processar Apenas uma Fase

```python
# Coletar apenas dados da Fase 1 - Colocados
data = scraper.scrape_phase_data(phase='1', data_type='colocados')

# Salvar em CSV
scraper.save_to_csv(data, 'fase1_colocados_custom.csv')
```

## Estrutura de Dados

Cada ficheiro CSV contém:

### Campos Comuns
- `fase`: Número da fase (1, 2, ou 3)
- `tipo`: Tipo de dados ('colocados' ou 'candidatos')
- `codigo_curso`: Código único do curso
- `nome_curso`: Nome do curso
- `instituicao`: Nome da instituição (filtrado para IPT)

### Campos Específicos (dependem da estrutura HTML real)
- `codigo_instituicao`: Código da instituição
- `vagas`: Número de vagas
- `colocados`: Número de alunos colocados
- `nota_ultimo`: Nota do último colocado
- etc.

## Adaptação à Estrutura Real do Site

Para adaptar o scraper à estrutura HTML real do site DGES:

### 1. Identificar URLs

```python
# Exemplo de URLs a identificar:
# Fase 1 - Colocados: https://dges.gov.pt/coloc/2025/fase1/colocados/
# Fase 1 - Candidatos: https://dges.gov.pt/coloc/2025/fase1/candidatos/
# etc.
```

Atualize em `scrape_phase_data()`:
```python
url = f"{self.BASE_URL}fase{phase}/{data_type}/"
```

### 2. Identificar Estrutura das Tabelas

Use DevTools (F12) para inspecionar:
```python
# Exemplo: se os dados estiverem numa tabela com class="resultado"
tables = soup.find_all('table', class_='resultado')
```

### 3. Adaptar Extração de Dados

Modifique em `scrape_phase_data()`:
```python
for table in tables:
    rows = table.find_all('tr')[1:]  # Skip header
    
    for row in rows:
        cols = row.find_all('td')
        
        record = {
            'fase': phase,
            'tipo': data_type,
            'codigo_curso': cols[0].get_text(strip=True),
            'nome_curso': cols[1].get_text(strip=True),
            'instituicao': cols[2].get_text(strip=True),
            # Adicione mais campos conforme necessário
        }
        
        # Filtrar apenas IPT
        if self.is_ipt_institution(record.get('instituicao', '')):
            phase_data.append(record)
```

### 4. Testar Paginação

Verifique se o link "Seguinte" é detectado corretamente:
```python
# O link pode ter diferentes formatos:
# <a href="page2.html">Seguinte</a>
# <a href="?page=2">Próxima ></a>
# <a href="/coloc/2025/fase1/colocados/?p=2">Next</a>
```

A função `find_next_page_link()` deve funcionar para todos estes casos.

## Análise de Dados Multi-Fase

### Exemplo: Comparação entre Fases

```python
import pandas as pd

# Carregar dados de todas as fases
df1 = pd.read_csv('data/fase1_colocados.csv')
df2 = pd.read_csv('data/fase2_colocados.csv')
df3 = pd.read_csv('data/fase3_colocados.csv')

# Análise
print(f"Fase 1: {len(df1)} colocados")
print(f"Fase 2: {len(df2)} colocados")
print(f"Fase 3: {len(df3)} colocados")

# Combinar para análise global
all_phases = pd.concat([df1, df2, df3])
```

### Exemplo: Taxa de Preenchimento por Fase

```python
# Carregar colocados e candidatos
colocados = pd.read_csv('data/fase1_colocados.csv')
candidatos = pd.read_csv('data/fase1_candidatos.csv')

# Calcular taxa
if len(candidatos) > 0:
    taxa = (len(colocados) / len(candidatos)) * 100
    print(f"Taxa de colocação Fase 1: {taxa:.1f}%")
```

## Boas Práticas

### ✅ FAZER
- Testar com uma fase primeiro antes de processar todas
- Verificar a estrutura HTML do site antes de executar
- Respeitar delays entre requisições (já configurado: 1.5s)
- Validar dados coletados antes de análise
- Criar backup dos CSVs gerados

### ❌ NÃO FAZER
- Executar o scraper repetidamente sem necessidade
- Modificar REQUEST_DELAY para valores muito baixos
- Processar dados sem filtrar pelo IPT
- Ignorar erros de paginação

## Resolução de Problemas

### Nenhum dado coletado

**Causa**: URLs ou estrutura HTML incorretos

**Solução**:
1. Verifique os logs em `scraper.log`
2. Confirme as URLs no navegador
3. Inspecione a estrutura HTML com DevTools
4. Adapte `scrape_phase_data()` conforme necessário

### Paginação não funciona

**Causa**: Link "Seguinte" não detectado

**Solução**:
1. Inspecione o HTML do link de paginação
2. Verifique se usa palavras diferentes ("Next", "Mais", etc.)
3. Adicione à lista de keywords em `find_next_page_link()`

### Dados duplicados

**Causa**: Paginação pode estar visitando mesma página

**Solução**:
1. Verifique se `next_url != current_url` no código
2. Adicione verificação de URLs já visitadas
3. Implemente set de URLs processadas

## Logs e Debugging

O scraper gera logs detalhados em `scraper.log`:

```
INFO - Processando: fase1_colocados
INFO - Processando página 1 - Fase 1 - colocados
INFO - Buscando: https://dges.gov.pt/coloc/2025/fase1/colocados/
INFO - Link 'Seguinte' encontrado: https://dges.gov.pt/coloc/2025/fase1/colocados/?page=2
INFO - Processando página 2 - Fase 1 - colocados
INFO - Não há mais páginas para Fase 1 - colocados
INFO - Total de registros coletados - Fase 1 - colocados: 42
```

## Próximos Passos

1. **Analisar o site**: Use DevTools para identificar estrutura HTML
2. **Adaptar código**: Modifique `scrape_phase_data()` conforme necessário
3. **Testar**: Execute com uma fase primeiro
4. **Validar**: Verifique dados nos CSVs gerados
5. **Escalar**: Processar todas as fases
6. **Analisar**: Use os dados para responder questões de investigação

## Referências

- `scripts/scraper.py` - Código principal
- `scripts/example_usage.py` - Exemplos de uso
- `docs/IMPLEMENTATION_GUIDE.md` - Guia de implementação
- `docs/DATA_DICTIONARY.md` - Estrutura de dados

---

**Última atualização**: 2025-11-17  
**Versão**: 2.0 (Multi-Fase com Paginação)
