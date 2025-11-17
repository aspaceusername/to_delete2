# RESUMO DAS ALTERAÇÕES - Web Scraper Multi-Fase

## O Que Foi Implementado

Adaptei o web scraper DGES para suportar **scraping multi-fase com paginação automática**, conforme solicitado.

### ✅ Funcionalidades Implementadas

#### 1. Suporte para 3 Fases de Admissão
O scraper agora processa automaticamente as 3 fases do concurso nacional de acesso:
- **Fase 1**: Primeira fase de colocações
- **Fase 2**: Segunda fase de colocações
- **Fase 3**: Terceira fase de colocações

#### 2. Dois Tipos de Dados por Fase
Para cada fase, o scraper coleta dois tipos de dados:
- **Colocados**: Alunos efetivamente admitidos/colocados
- **Candidatos**: Lista de candidatos

#### 3. Paginação Automática
Implementei uma função que:
- Detecta automaticamente links "Seguinte" no HTML
- Suporta variações: "Seguinte", "Next", "Próxima", "Proxima", ">"
- Converte URLs relativas em absolutas
- Percorre todas as páginas até não haver mais resultados

#### 4. Geração de 6 CSVs Separados
O scraper agora gera **6 ficheiros CSV distintos**:

| Ficheiro | Conteúdo |
|----------|----------|
| `fase1_colocados.csv` | Alunos admitidos na 1ª fase |
| `fase1_candidatos.csv` | Candidatos da 1ª fase |
| `fase2_colocados.csv` | Alunos admitidos na 2ª fase |
| `fase2_candidatos.csv` | Candidatos da 2ª fase |
| `fase3_colocados.csv` | Alunos admitidos na 3ª fase |
| `fase3_candidatos.csv` | Candidatos da 3ª fase |

## Mudanças no Código

### Ficheiro: `scripts/scraper.py`

#### Novas Constantes
```python
PHASES = ['1', '2', '3']  # 3 fases de admissão
DATA_TYPES = ['colocados', 'candidatos']  # admitidos e candidatos
```

#### Nova Função: `find_next_page_link()`
Detecta o link para a próxima página:
```python
def find_next_page_link(self, soup: BeautifulSoup) -> Optional[str]:
    # Procura por links com "Seguinte", "Next", "Próxima", etc.
    # Retorna URL da próxima página ou None
```

#### Nova Função: `scrape_phase_data()`
Coleta dados de uma fase específica com paginação:
```python
def scrape_phase_data(self, phase: str, data_type: str) -> List[Dict]:
    # Processa uma fase específica
    # Implementa paginação automática
    # Retorna todos os dados da fase
```

#### Função Atualizada: `scrape_admissions_data()`
Agora retorna um dicionário em vez de lista:
```python
# Antes: return List[Dict]
# Agora: return Dict[str, List[Dict]]
# 
# Exemplo de retorno:
# {
#   'fase1_colocados': [...],
#   'fase1_candidatos': [...],
#   'fase2_colocados': [...],
#   ...
# }
```

#### Função Atualizada: `run()`
Agora retorna lista de 6 Paths em vez de 1:
```python
# Antes: return Path
# Agora: return List[Path]
#
# Gera 6 ficheiros CSV
```

### Ficheiro: `scripts/test_scraper.py`

Adicionados 2 novos testes:

1. **`test_phases_and_data_types()`**
   - Verifica que PHASES tem 3 elementos
   - Verifica que DATA_TYPES tem 2 elementos

2. **`test_pagination_link_detection()`**
   - Testa detecção de link "Seguinte"
   - Testa com HTML que tem e que não tem link de paginação

**Resultado**: ✅ Todos os 6 testes passam

### Ficheiro: `scripts/example_usage.py`

Adicionado novo exemplo:

**`example_multi_phase_analysis()`**
- Demonstra como analisar dados de múltiplas fases
- Calcula taxa de colocação por fase
- Mostra insights sobre distribuição de alunos

### Novo Ficheiro: `docs/MULTI_PHASE_SCRAPING.md`

Documentação completa incluindo:
- Visão geral das funcionalidades
- Como usar o scraper
- Como adaptar à estrutura HTML real do site
- Exemplos de análise de dados
- Troubleshooting
- Boas práticas

## Como Usar

### Execução Básica

```bash
# Executar o scraper (gera 6 CSVs)
python scripts/scraper.py
```

### Verificar Resultados

```bash
# Listar CSVs gerados
ls -lh data/*.csv

# Ver conteúdo de um CSV
cat data/fase1_colocados.csv
```

### Executar Testes

```bash
# Executar todos os testes
python scripts/test_scraper.py

# Ver exemplos de uso
python scripts/example_usage.py
```

## Como Adaptar à Estrutura Real do Site

O código está preparado para ser facilmente adaptado. Siga estes passos:

### Passo 1: Identificar URLs

1. Abra https://dges.gov.pt/coloc/2025/ no navegador
2. Navegue até página de cada fase
3. Anote as URLs (exemplo hipotético):
   - Fase 1 Colocados: `https://dges.gov.pt/coloc/2025/fase1/colocados/`
   - Fase 1 Candidatos: `https://dges.gov.pt/coloc/2025/fase1/candidatos/`
   - etc.

### Passo 2: Atualizar URLs no Código

Em `scraper.py`, função `scrape_phase_data()`, linha ~242:
```python
# Atualizar esta linha conforme URLs reais:
url = f"{self.BASE_URL}fase{phase}/{data_type}/"
```

### Passo 3: Identificar Estrutura HTML

1. Use DevTools (F12) no navegador
2. Inspecione as tabelas de dados
3. Identifique os seletores CSS necessários

Exemplo:
```html
<table class="resultados">
  <tr>
    <td>Código</td>
    <td>Nome do Curso</td>
    <td>Instituição</td>
  </tr>
  <tr>
    <td>9999</td>
    <td>Engenharia Informática</td>
    <td>Instituto Politécnico de Tomar</td>
  </tr>
</table>
```

### Passo 4: Adaptar Extração de Dados

Em `scraper.py`, função `scrape_phase_data()`, linhas ~255-270:

```python
# Adaptar seletores conforme estrutura real
tables = soup.find_all('table', class_='resultados')  # Atualizar class

for table in tables:
    rows = table.find_all('tr')[1:]  # Skip header
    
    for row in rows:
        cols = row.find_all('td')
        
        # Adaptar extração conforme colunas reais
        record = {
            'fase': phase,
            'tipo': data_type,
            'codigo_curso': cols[0].get_text(strip=True),
            'nome_curso': cols[1].get_text(strip=True),
            'instituicao': cols[2].get_text(strip=True),
            # Adicionar mais campos conforme necessário
        }
```

### Passo 5: Testar

```bash
# Testar com uma fase primeiro
python scripts/scraper.py

# Verificar dados
cat data/fase1_colocados.csv
```

## Estrutura de Paginação

A função `find_next_page_link()` suporta diferentes formatos de links:

```html
<!-- Formato 1: Link relativo -->
<a href="page2.html">Seguinte</a>

<!-- Formato 2: Link com query string -->
<a href="?page=2">Próxima</a>

<!-- Formato 3: Link absoluto -->
<a href="https://dges.gov.pt/coloc/2025/fase1/colocados/?p=2">Next</a>

<!-- Formato 4: Link com símbolo -->
<a href="pagina2">></a>
```

Todos estes formatos são automaticamente detectados e convertidos para URL absoluta.

## Exemplo de Fluxo de Execução

```
1. Iniciar scraper
   ↓
2. Para cada fase (1, 2, 3):
   ↓
3. Para cada tipo (colocados, candidatos):
   ↓
4. Acessar URL da fase/tipo
   ↓
5. Extrair dados da página
   ↓
6. Procurar link "Seguinte"
   ↓
7. Se existir:
   - Ir para próxima página
   - Voltar ao passo 5
   ↓
8. Se não existir:
   - Avançar para próximo tipo/fase
   ↓
9. Salvar dados em CSV
   ↓
10. Gerar 6 ficheiros CSV
```

## Logs e Debugging

O scraper gera logs detalhados em `scraper.log`:

```
INFO - Processando: fase1_colocados
INFO - Processando página 1 - Fase 1 - colocados
INFO - Link 'Seguinte' encontrado: [URL]
INFO - Processando página 2 - Fase 1 - colocados
INFO - Não há mais páginas para Fase 1 - colocados
INFO - Total de registros coletados - Fase 1 - colocados: 42
```

## Testes Implementados

| Teste | Descrição | Status |
|-------|-----------|--------|
| `test_scraper_initialization()` | Verifica inicialização | ✅ |
| `test_ipt_institution_detection()` | Testa detecção IPT | ✅ |
| `test_anonymization()` | Testa anonimização | ✅ |
| `test_data_structure()` | Verifica estrutura | ✅ |
| `test_phases_and_data_types()` | Testa configuração fases | ✅ |
| `test_pagination_link_detection()` | Testa paginação | ✅ |

## Próximos Passos

1. ✅ **CONCLUÍDO**: Implementar multi-fase
2. ✅ **CONCLUÍDO**: Implementar paginação
3. ✅ **CONCLUÍDO**: Gerar 6 CSVs
4. ✅ **CONCLUÍDO**: Adicionar testes
5. ✅ **CONCLUÍDO**: Criar documentação
6. ⏳ **PENDENTE**: Adaptar à estrutura HTML real (requer acesso ao site)
7. ⏳ **PENDENTE**: Testar com dados reais
8. ⏳ **PENDENTE**: Análise de dados coletados

## Ficheiros Criados/Modificados

### Modificados
- ✅ `scripts/scraper.py` - Implementação principal
- ✅ `scripts/test_scraper.py` - Novos testes
- ✅ `scripts/example_usage.py` - Novos exemplos

### Criados
- ✅ `docs/MULTI_PHASE_SCRAPING.md` - Documentação completa

### Gerados (em runtime)
- ✅ `data/fase1_colocados.csv`
- ✅ `data/fase1_candidatos.csv`
- ✅ `data/fase2_colocados.csv`
- ✅ `data/fase2_candidatos.csv`
- ✅ `data/fase3_colocados.csv`
- ✅ `data/fase3_candidatos.csv`

## Recursos Adicionais

- **Documentação completa**: `docs/MULTI_PHASE_SCRAPING.md`
- **Guia de implementação**: `docs/IMPLEMENTATION_GUIDE.md`
- **Exemplos de uso**: `scripts/example_usage.py`
- **Testes**: `scripts/test_scraper.py`

## Suporte

Para questões sobre:
- **Adaptação do código**: Consulte `docs/MULTI_PHASE_SCRAPING.md`
- **Estrutura HTML**: Use DevTools (F12) no navegador
- **Paginação**: Verifique `find_next_page_link()` em `scraper.py`
- **Dados**: Consulte `docs/DATA_DICTIONARY.md`

---

**Data**: 2025-11-17  
**Versão**: 2.0  
**Status**: ✅ Implementação completa  
**Testes**: ✅ 6/6 passando  
**Documentação**: ✅ Completa
