# Dicionário de Dados - IPT Admissions Analysis

## Visão Geral

Este documento descreve a estrutura de dados esperada para o projeto de análise de admissões do IPT.

## Estrutura de Dados Principal

### Tabela: Cursos e Admissões

| Campo | Tipo | Descrição | Exemplo | Obrigatório |
|-------|------|-----------|---------|-------------|
| `codigo_curso` | String | Código único do curso no sistema DGES | "9853" | ✓ |
| `nome_curso` | String | Nome completo do curso | "Engenharia Informática" | ✓ |
| `codigo_instituicao` | String | Código da instituição (IPT) | "3100" | ✓ |
| `instituicao` | String | Nome da instituição | "Instituto Politécnico de Tomar" | ✓ |
| `escola` | String | Escola/Departamento dentro do IPT | "Escola Superior de Tecnologia" | - |
| `regime` | String | Regime de frequência | "Diurno", "Pós-Laboral" | - |
| `grau` | String | Grau académico | "Licenciatura", "Mestrado" | - |
| `ano_letivo` | Integer | Ano letivo das admissões | 2025 | ✓ |

### Tabela: Vagas e Colocações

| Campo | Tipo | Descrição | Exemplo | Obrigatório |
|-------|------|-----------|---------|-------------|
| `vagas_totais` | Integer | Total de vagas abertas | 30 | ✓ |
| `vagas_colocadas` | Integer | Número de alunos colocados | 28 | ✓ |
| `vagas_nao_preenchidas` | Integer | Vagas que ficaram vazias | 2 | - |
| `taxa_ocupacao` | Float | Percentagem de vagas preenchidas | 93.33 | - |

### Tabela: Notas de Admissão

| Campo | Tipo | Descrição | Exemplo | Obrigatório |
|-------|------|-----------|---------|-------------|
| `nota_ultimo_colocado` | Float | Nota do último aluno colocado | 145.5 | ✓ |
| `nota_primeiro_colocado` | Float | Nota do primeiro colocado (maior nota) | 185.0 | - |
| `nota_media` | Float | Nota média dos colocados | 160.3 | - |
| `nota_minima` | Float | Nota mínima de candidatura | 95.0 | - |
| `percentil_25` | Float | 25º percentil das notas | 150.0 | - |
| `percentil_50` | Float | Mediana das notas | 158.5 | - |
| `percentil_75` | Float | 75º percentil das notas | 170.0 | - |

### Tabela: Candidaturas (Dados Agregados)

| Campo | Tipo | Descrição | Exemplo | Obrigatório |
|-------|------|-----------|---------|-------------|
| `total_candidatos` | Integer | Número total de candidatos | 45 | - |
| `candidatos_primeira_opcao` | Integer | Candidatos com IPT como 1ª escolha | 20 | - |
| `percentagem_primeira_opcao` | Float | % de 1ª opções | 44.4 | - |
| `posicao_media_preferencia` | Float | Posição média do curso nas preferências | 2.5 | - |
| `ratio_candidatos_vagas` | Float | Rácio candidatos/vagas | 1.5 | - |

## Dados Anonimizados

### Princípios de Anonimização

1. **Não coletar**:
   - Nomes completos de estudantes
   - Números de identificação pessoal
   - Emails ou contactos
   - Moradas

2. **Agregar sempre que possível**:
   - Usar estatísticas agregadas
   - Agrupar por faixas (e.g., notas 140-150)
   - Reportar médias, medianas, percentis

3. **Hash quando necessário**:
   - Se precisar de identificador único: usar hash
   - Formato: `ANON_` + primeiros 8 caracteres do hash

## Campos Calculados

### Derivados dos dados brutos

```python
# Taxa de ocupação
taxa_ocupacao = (vagas_colocadas / vagas_totais) * 100

# Vagas não preenchidas
vagas_nao_preenchidas = vagas_totais - vagas_colocadas

# Percentagem primeira opção
percentagem_primeira_opcao = (candidatos_primeira_opcao / total_candidatos) * 100

# Rácio candidatos/vagas
ratio_candidatos_vagas = total_candidatos / vagas_totais
```

## Formato de Saída

### CSV Principal: `ipt_admissions_YYYYMMDD.csv`

```csv
codigo_curso,nome_curso,instituicao,ano_letivo,vagas_totais,vagas_colocadas,nota_ultimo_colocado
9853,Engenharia Informática,Instituto Politécnico de Tomar,2025,30,28,145.5
9854,Gestão de Empresas,Instituto Politécnico de Tomar,2025,25,22,138.0
```

### CSV Estatísticas: `ipt_statistics_YYYYMMDD.csv`

```csv
codigo_curso,nota_media,nota_minima,nota_maxima,percentil_25,percentil_50,percentil_75
9853,160.3,145.5,185.0,150.0,158.5,170.0
9854,152.1,138.0,178.5,142.0,150.0,162.0
```

## Validações de Dados

### Regras de validação

1. **Integridade**:
   - `vagas_colocadas <= vagas_totais`
   - `nota_ultimo_colocado <= nota_primeiro_colocado`
   - `nota_minima <= nota_ultimo_colocado`

2. **Ranges**:
   - Notas: 0 - 200
   - Vagas: > 0
   - Ano letivo: ano atual ou futuro

3. **Obrigatoriedade**:
   - Campos marcados como obrigatórios não podem estar vazios

### Exemplo de validação em Python

```python
import pandas as pd

def validate_admissions_data(df: pd.DataFrame) -> bool:
    """Valida dados de admissões."""
    
    # Verificar campos obrigatórios
    required = ['codigo_curso', 'nome_curso', 'instituicao', 
                'vagas_totais', 'vagas_colocadas', 'nota_ultimo_colocado']
    
    if not all(col in df.columns for col in required):
        print("Campos obrigatórios em falta")
        return False
    
    # Validar integridade
    if (df['vagas_colocadas'] > df['vagas_totais']).any():
        print("Erro: vagas_colocadas > vagas_totais")
        return False
    
    # Validar ranges
    if (df['nota_ultimo_colocado'] < 0).any() or (df['nota_ultimo_colocado'] > 200).any():
        print("Erro: notas fora do range válido (0-200)")
        return False
    
    return True
```

## Campos para Análise de Questões-Chave

### Popularidade dos Cursos
- `vagas_colocadas`
- `vagas_nao_preenchidas`
- `ratio_candidatos_vagas`
- `candidatos_primeira_opcao`

### Notas de Entrada
- `nota_ultimo_colocado`
- `nota_media`
- Comparação com percentis nacionais (dados externos)

### Perfil do Estudante
- `posicao_media_preferencia`
- `percentagem_primeira_opcao`
- Distribuição de notas (percentis)

### Indicadores de Abandono
- Correlação entre `posicao_media_preferencia` e taxa de abandono
- Análise de notas baixas (`nota_ultimo_colocado` vs `nota_minima`)

## Próximos Passos

1. **Coletar dados** usando o scraper
2. **Validar** usando as regras acima
3. **Limpar** dados inconsistentes
4. **Enriquecer** com dados calculados
5. **Exportar** em formatos adequados para análise

## Notas

- Todos os dados devem ser anonimizados
- Focar em estatísticas agregadas
- Manter dados brutos separados dos processados
- Documentar todas as transformações aplicadas
