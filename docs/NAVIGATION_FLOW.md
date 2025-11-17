# DGES Navigation Flow

## Overview

Este documento descreve o fluxo de navegação implementado no scraper DGES baseado nos ficheiros HTML reais fornecidos na pasta `pages/`.

## Fluxo Completo de Navegação

### Passo 1: Página Inicial
**Ficheiro**: `pages/first_page.html`  
**URL**: `https://dges.gov.pt/coloc/2025/`

**Ação**: Clicar em "Listas de candidatos da 1ª fase" (ou 2ª, 3ª fase)

### Passo 2: Seleção de Tipo de Ensino
**Ficheiro**: `pages/second_page.html`

**Ação**: Clicar em "Ensino Superior Público Politécnico"

### Passo 3: Seleção de Instituição
**Ficheiro**: `pages/third_page.html`  
**Form**: `<form action="col1listaredir.asp" method="post">`

**Campos do Formulário**:
- `CodEstab`: Código da instituição (3242 para IPT)
- `CodR`: Código da região (12)
- `listagem`: Tipo de lista

**Ação**: Selecionar "3242 - Instituto Politécnico de Tomar - Escola Superior de Tecnologia de Tomar" no dropdown

### Passo 4: Seleção de Tipo de Lista
**Ficheiro**: `pages/fourth_page.html`

**Opções**:
- "Lista de Colocados" → colocados
- "Lista Ordenada de Candidatos" → candidatos

**Ação**: Selecionar tipo de lista e clicar em botão específico

### Passo 5: Seleção de Curso
**Ação**: Selecionar "Engenharia Informática" (código 9119) e clicar "Continuar"

### Passo 6: Página de Dados
**Ficheiros**: 
- `pages/lista_colocados_1_fase.html` (para colocados)
- `pages/lista_cadidatos_1_fase.html` (para candidatos)

**Estrutura HTML**:
```html
<!-- Informação de instituição e curso -->
<table class="caixa">
  <tr><td>3242 - Instituto Politécnico de Tomar - Escola Superior...</td></tr>
  <tr><td>9119 - Engenharia Informática</td></tr>
</table>

<!-- Dados dos estudantes -->
<table width="700" border="0">
  <tr>
    <td width="150">303(...)97</td>  <!-- Nº Identificação (parcial) -->
    <td width="550">DIOGO SANTOS GOMES</td>  <!-- Nome -->
  </tr>
</table>
```

**Paginação**: Link "Seguinte" para próxima página

## Implementação no Scraper

### Método Principal: `navigate_to_course_data(phase, data_type)`

Este método implementa toda a navegação:

1. **Acessa página inicial**: `col{phase}listas.asp?CodR=12&action=2`
2. **Procura formulário**: Detecta formulário com select de instituição
3. **Seleciona IPT**: Procura option com value="3242"
4. **Prepara dados**: Adiciona campos hidden e tipo de lista
5. **Submete formulário**: POST para `col{phase}listaredir.asp`
6. **Retorna URL final**: Página com dados para scraping

### Método de Extração: `scrape_phase_data(phase, data_type)`

1. **Navega até dados**: Usa `navigate_to_course_data()`
2. **Loop de paginação**: Processa cada página
3. **Extrai informações**:
   - Instituição: `3242 - Instituto Politécnico de Tomar...`
   - Curso: `9119 - Engenharia Informática`
   - Estudantes: ID parcial e Nome
4. **Anonimiza dados**: Nome completo → Iniciais
5. **Procura próxima página**: Link "Seguinte"

### Detecção de Paginação: `find_next_page_link(soup)`

Procura links com texto:
- "Seguinte"
- "Next"
- "Próxima"
- ">"

Retorna URL absoluta ou `None` se não houver mais páginas.

## Dados Extraídos

### Estrutura do Registro

```python
{
    'fase': '1',  # Fase de admissão (1, 2 ou 3)
    'tipo': 'colocados',  # Tipo de dados (colocados ou candidatos)
    'codigo_instituicao': '3242',
    'nome_instituicao': 'Instituto Politécnico de Tomar - Escola Superior...',
    'codigo_curso': '9119',
    'nome_curso': 'Engenharia Informática',
    'id_estudante_parcial': '303(...)97',  # Já anonimizado pelo DGES
    'nome_estudante': 'D. G.',  # Anonimizado para iniciais
    'ano': 2025
}
```

### CSVs Gerados

**6 ficheiros CSV** (um para cada combinação de fase e tipo):

1. `data/fase1_colocados.csv`
2. `data/fase1_candidatos.csv`
3. `data/fase2_colocados.csv`
4. `data/fase2_candidatos.csv`
5. `data/fase3_colocados.csv`
6. `data/fase3_candidatos.csv`

## Adaptações Implementadas

### Detecção Flexível de Campos

O scraper tenta múltiplas estratégias para encontrar campos:

**Seleção de Instituição**:
- Por nome: `CodEstab`, `CodEst`, `escola`, `instituicao`
- Por valor: Procura select que contenha option="3242"

**Tipo de Lista**:
- Radio buttons com labels contendo keywords
- Campos hidden já preenchidos

**Campos Hidden**:
- Inclui automaticamente todos os inputs type="hidden"
- Preserva valores existentes (como `CodR`)

### Robustez

✅ Não depende de nomes específicos de campos  
✅ Funciona com URLs relativas e absolutas  
✅ Trata ausência de form action (usa URL atual)  
✅ Fallback para URLs diretas se navegação falhar  
✅ Logging detalhado para debugging  
✅ Session management para manter estado

## Execução

```bash
python scripts/scraper.py
```

### Logs Esperados

```
INFO - Navegando para dados - Fase 1 - colocados
INFO - Passo 1: Acessando https://dges.gov.pt/coloc/2025/col1listas.asp?CodR=12&action=2
INFO - Encontrados 1 formulários na página
INFO - Select de escola encontrado por valor 3242
INFO - Selecionando IPT: CodEstab=3242
INFO - Submetendo formulário para: https://dges.gov.pt/coloc/2025/col1listaredir.asp
INFO - Dados do formulário: {'CodEstab': '3242', 'CodR': '12', 'listagem': 'Últimos Colocados'}
INFO - Navegação concluída. URL final: https://dges.gov.pt/coloc/2025/col1listaredir.asp
INFO - Processando página 1 - Fase 1 - colocados
INFO - Instituição: 3242 - Instituto Politécnico de Tomar...
INFO - Curso: 9119 - Engenharia Informática
INFO - Extraídos 8 estudantes nesta página
INFO - Total de registros coletados - Fase 1 - colocados: 8
```

## Referências

- Ficheiros HTML de exemplo: `pages/`
- Implementação: `scripts/scraper.py`
- Testes: `scripts/test_scraper.py`
- Documentação: `docs/MULTI_PHASE_SCRAPING.md`
