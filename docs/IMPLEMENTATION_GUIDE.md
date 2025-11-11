# Guia de Implementação do Web Scraper DGES

## Visão Geral

Este documento fornece orientações detalhadas sobre como adaptar o script de web scraping (`scripts/scraper.py`) à estrutura real do site da DGES.

## Estrutura Atual do Script

O script `scraper.py` já implementa:

### ✅ Práticas Éticas de Web Scraping
- **Respeito ao robots.txt**: Verifica e respeita as regras do site
- **Rate Limiting**: Delay de 1.5 segundos entre requisições
- **User-Agent Identificável**: Identifica-se como bot educacional
- **Timeout configurável**: Evita requisições infinitas
- **Logging completo**: Rastreia todas as operações

### ✅ Proteção de Dados
- **Anonimização**: Função `anonymize_student_data()` remove informações pessoais
- **Dados agregados**: Foco em estatísticas, não em indivíduos

### ✅ Filtros IPT
- **Códigos de instituição**: Array com códigos do IPT
- **Padrões de nome**: Identifica variações do nome "Instituto Politécnico de Tomar"

## Como Adaptar o Script

### Passo 1: Análise Manual do Site

1. **Abra o site no navegador**:
   ```
   https://dges.gov.pt/coloc/2025/
   ```

2. **Use DevTools (F12)**:
   - Aba "Network": Veja quais requisições são feitas
   - Aba "Elements": Inspecione a estrutura HTML
   - Aba "Console": Teste seletores CSS/XPath

3. **Identifique a estrutura**:
   - O site usa formulários para pesquisa?
   - Os dados estão em tabelas HTML?
   - Usa JavaScript para carregar dados (AJAX)?
   - Existe paginação?

### Passo 2: Exemplos de Implementação

#### Se os dados estiverem em tabelas HTML:

```python
def scrape_courses(self) -> List[Dict]:
    soup = self.fetch_page(self.BASE_URL)
    courses_data = []
    
    # Encontrar todas as tabelas
    tables = soup.find_all('table', class_='nome-da-classe')
    
    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows:
            cols = row.find_all('td')
            
            course = {
                'codigo_curso': cols[0].text.strip(),
                'nome_curso': cols[1].text.strip(),
                'instituicao': cols[2].text.strip(),
                'vagas': int(cols[3].text.strip()),
                'colocados': int(cols[4].text.strip()),
                'nota_ultimo': float(cols[5].text.strip()),
            }
            
            # Filtrar apenas IPT
            if self.is_ipt_institution(course['instituicao']):
                courses_data.append(course)
    
    return courses_data
```

#### Se o site usar formulários:

```python
def scrape_courses(self) -> List[Dict]:
    courses_data = []
    
    # Parâmetros do formulário
    form_data = {
        'instituicao': '3100',  # Código do IPT
        'ano': '2025',
        # outros campos conforme necessário
    }
    
    # Submeter formulário
    response = self.session.post(
        f"{self.BASE_URL}/pesquisa",
        data=form_data,
        timeout=self.TIMEOUT
    )
    
    time.sleep(self.REQUEST_DELAY)
    
    soup = BeautifulSoup(response.content, 'lxml')
    # Processar resultados...
    
    return courses_data
```

#### Se usar JavaScript/AJAX:

**Opção 1 - Identificar API**:
```python
def scrape_courses(self) -> List[Dict]:
    # Verifique no DevTools > Network se há chamadas API
    api_url = "https://dges.gov.pt/api/coloc/2025/cursos"
    
    response = self.session.get(api_url, params={'instituicao': '3100'})
    data = response.json()
    
    # Processar JSON...
    return data
```

**Opção 2 - Usar Selenium**:
```python
# Adicionar ao requirements.txt: selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_courses_selenium(self) -> List[Dict]:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=options)
    driver.get(self.BASE_URL)
    
    # Esperar JavaScript carregar
    time.sleep(3)
    
    # Extrair dados
    elements = driver.find_elements(By.CLASS_NAME, 'curso-item')
    # Processar elementos...
    
    driver.quit()
    return courses_data
```

### Passo 3: Testar Incrementalmente

1. **Teste com uma página**:
   ```bash
   python scripts/scraper.py
   ```

2. **Verifique os logs**:
   ```bash
   cat scraper.log
   ```

3. **Inspecione o CSV gerado**:
   ```bash
   cat data/ipt_admissions_*.csv
   ```

## Campos de Dados Sugeridos

Com base nos objetivos do projeto, tente coletar:

### Dados dos Cursos
- `codigo_curso`: Código único do curso
- `nome_curso`: Nome completo do curso
- `codigo_instituicao`: Código do IPT
- `instituicao`: Nome da instituição
- `escola`: Escola/Departamento (se disponível)
- `vagas_totais`: Total de vagas abertas
- `vagas_colocados`: Número de colocados
- `vagas_nao_preenchidas`: Vagas que sobraram
- `ano_letivo`: 2025

### Dados de Notas
- `nota_ultimo_colocado`: Nota do último aluno colocado
- `nota_primeiro_colocado`: Nota do primeiro colocado (opcional)
- `nota_media`: Nota média dos colocados (se disponível)

### Dados de Candidaturas (Anonimizados)
- `total_candidatos`: Número total de candidatos ao curso
- `posicao_media_ipt`: Posição média em que IPT aparece nas preferências
- `primeiras_escolhas`: Quantos puseram IPT como 1ª opção

### Dados Estatísticos
- `percentil_25`: 25º percentil das notas
- `percentil_50`: Mediana
- `percentil_75`: 75º percentil

## Boas Práticas

### ✅ FAZER:
- Testar com poucos cursos primeiro
- Salvar versões incrementais dos dados
- Usar try-except para robustez
- Documentar estruturas HTML encontradas
- Respeitar delays entre requisições
- Verificar se há mudanças na estrutura do site

### ❌ NÃO FAZER:
- Fazer múltiplas requisições simultâneas
- Ignorar erros HTTP
- Coletar dados pessoais identificáveis
- Fazer scraping 24/7
- Ignorar mensagens de erro do site

## Troubleshooting

### Problema: "Não foi possível acessar a página"
**Solução**: Verifique:
- Conexão com internet
- URL está correta
- Site não está em manutenção
- Firewall não bloqueia requisições

### Problema: "Estrutura HTML mudou"
**Solução**: 
- Re-inspecionar o site
- Atualizar seletores CSS/XPath
- Verificar se há nova versão da API

### Problema: "Dados incompletos"
**Solução**:
- Verificar se há paginação
- Verificar se precisa de autenticação
- Confirmar que filtros estão corretos

### Problema: "Bloqueado pelo site"
**Solução**:
- Aumentar delay entre requisições
- Verificar se User-Agent é aceito
- Respeitar horários de menor tráfego
- Contactar administradores do site se necessário

## Exemplo Completo de Fluxo

```python
# 1. Iniciar scraper
scraper = DGESScraper(output_dir='data')

# 2. Verificar robots.txt
if not scraper.respect_robots_txt():
    print("Scraping não permitido")
    exit(1)

# 3. Buscar página principal
soup = scraper.fetch_page(scraper.BASE_URL)

# 4. Identificar link/formulário para dados do IPT
# (Adaptar conforme estrutura real)

# 5. Extrair dados
courses = scraper.scrape_courses()

# 6. Filtrar apenas IPT
ipt_courses = [c for c in courses if scraper.is_ipt_institution(c['instituicao'])]

# 7. Salvar
scraper.save_to_csv(ipt_courses)
```

## Próximos Passos

Após coletar os dados:

1. **Validação**: Verificar consistência dos dados
2. **Limpeza**: Remover duplicados, normalizar formatos
3. **Análise**: Executar EDA (Exploratory Data Analysis)
4. **Visualização**: Criar gráficos e insights
5. **Relatório**: Documentar descobertas

## Recursos Adicionais

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)

## Contacto para Dúvidas

Este é um projeto educacional. Se tiver dúvidas sobre o scraping ético ou a estrutura do site, consulte o professor orientador.
