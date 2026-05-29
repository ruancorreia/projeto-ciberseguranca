# Análise de Segurança Cibernética e Ataques Digitais

Projeto final da disciplina **Linguagens de Programação**, desenvolvido para o
curso de **Sistemas de Informação - Unilasalle**.

- Professor orientador: [Alexandre Neves Louzada](https://github.com/AlexandreLouzada)
- Aluno: [Ruan da Silva Correia](https://github.com/ruancorreia)

## Sobre o projeto

Este projeto usa a base `simulacao_ciberseguranca_brasil.csv` para analisar
incidentes de segurança cibernética no Brasil entre 2015 e 2024. O dashboard foi
criado com **Python**, **Pandas**, **Plotly** e **Streamlit**, trazendo KPIs,
filtros interativos, gráficos e interpretação executiva dos resultados.

Base utilizada:
[simulacao_ciberseguranca_brasil.csv](https://github.com/AlexandreLouzada/Dados-Simulados-G2/blob/main/datasets_g2_30_temas/simulacao_ciberseguranca_brasil.csv)

## Funcionalidades

- Página inicial em dark mode.
- Dashboard com modo claro/escuro.
- Filtros por ano, mês, região, UF, setor, tipo de ataque e criticidade.
- KPIs animados com visão geral do recorte filtrado.
- Linha temporal de incidentes.
- Barras por tipo de ataque, setor e UF.
- Heatmap mensal.
- Mapa de ataques por setor.
- Análise de criticidade e status de resposta.
- Dispersão entre impacto financeiro e incidentes.
- Tabela dinâmica para exploração dos dados.
- Interpretação textual e conclusão executiva dinâmicas.

## KPIs apresentados

- Total de incidentes.
- Tipo de ataque predominante.
- Setor mais afetado.
- Impacto financeiro total.
- Tempo médio de recuperação.
- Região mais crítica.

## Estrutura

```text
projeto-ciberseguranca/
|-- app.py
|-- requirements.txt
|-- README.md
|-- index.html
|-- dados/
|   |-- simulacao_ciberseguranca_brasil.csv
|-- notebooks/
|   |-- analise_ciberseguranca.ipynb
|-- database/
|-- imagens/
```

## Como rodar na sua máquina

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd projeto-ciberseguranca
```

### 2. Criar um ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o dashboard

```bash
streamlit run app.py
```

Depois, abra o endereço exibido no terminal. Normalmente:

```text
http://localhost:8501
```

## Notebook

O notebook de análise está em:

```text
notebooks/analise_ciberseguranca.ipynb
```

Ele contém introdução, contextualização, explicação da base, leitura dos dados,
limpeza, engenharia de atributos, KPIs, visualizações, interpretação e conclusão.

## Publicação

Após publicar o projeto, atualize os links abaixo:

- GitHub: [https://github.com/ruancorreia/projeto-ciberseguranca](https://github.com/ruancorreia/projeto-ciberseguranca)
- GitHub Pages: [https://ruancorreia.github.io/projeto-ciberseguranca/](https://ruancorreia.github.io/projeto-ciberseguranca/)
- Streamlit Cloud: `<link do dashboard>`

## Tecnologias

- Python
- Pandas
- Plotly
- Streamlit
- GitHub Pages

## Licença

Projeto acadêmico desenvolvido para fins educacionais.
