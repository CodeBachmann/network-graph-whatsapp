


# network-graph-whatsapp
Um notebook python para processar conversas de whatsapp crir um dicionário normalizador de palavras e plotar um gráfico de conexão entre as palavras

https://github.com/user-attachments/assets/b4f9e4c9-3e21-4597-9d67-13b66952b733


# Análise de Rede do WhatsApp

Este notebook realiza uma análise de rede de mensagens do WhatsApp, utilizando bibliotecas como `pandas`, `networkx`, `pyvis`, e `spacy`. O objetivo é explorar e visualizar as interações entre os usuários.

## Dependências

Certifique-se de ter as seguintes bibliotecas instaladas:

- `pandas`
- `nltk`
- `seaborn`
- `matplotlib`
- `spacy`
- `networkx`
- `pyvis`
- `numpy`

Você pode instalar as dependências usando o seguinte comando:

```bash
pip install pandas nltk seaborn matplotlib spacy networkx pyvis numpy
```

## Carregamento de Dados

O notebook começa importando as bibliotecas necessárias e configurando o ambiente para visualização de gráficos:

```python
import sys
import os
import pandas as pd
import nltk
import seaborn as sns
import matplotlib
from pathlib import Path
```

## Importação de Módulos Personalizados

O caminho do diretório atual é adicionado ao `sys.path` para permitir a importação de módulos personalizados:

```python
print(os.getcwd())
sys.path.append(os.getcwd())  # Usando o diretório de trabalho atual
import Funcao
```

## Configuração do Ambiente

A configuração do ambiente é feita para utilizar o plotter do Tkinter que permite a interação com o gráfico:

```python
matplotlib.use('TkAgg')
```

## Processamento de Texto

O modelo de linguagem em português do `spacy` é carregado, e um stemmer é inicializado para processamento de texto:

```python
nlp = spacy.load("pt_core_news_sm")
stemmer = RSLPStemmer()
```

### Formatando os textos
def remove_stopwords
  retira palavras que não agregam para a analise baseado em uma lista de palavras definidas dentro da propria função
  
def preprocess_text 
  aplica uma serie de processamentos para facilitar a manipulação dos textos

```python
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', 'link', text, flags=re.MULTILINE)
    
    # Remove emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'mail', text)
    
    # Remove usernames (e.g., @username)
    text = re.sub(r'@\w+', 'user', text)
    
    # Remove special characters except for punctuation
    text = remover_acentos(text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    text = corrigir_abreviacoes(texto=text)
    
    return text
```   

### Dicionário

Utilizando Spacy e Stemmer é criado um dicionário de normalização de palavras, o resultado não é perfeito, por isso algum trabalho manual pode ser necessário:

![image](https://github.com/user-attachments/assets/6b5196bc-be8b-4942-a5e7-3af9ccf1cde4)

## Preparo dos Dados para plotagem

Utilizando a biblioteca Networkx em um laço for é criada a relação entre as palavras:

```python
def build_cooccurrence_graph(texts):
    G = nx.Graph()  # Criar um grafo vazio
    for text in texts:
        words = text.split()  # Tokenizar o texto
        for i in range(len(words) - 1):
            word_pair = (words[i], words[i + 1])  # Par de palavras consecutivas
            if G.has_edge(*word_pair):
                G[word_pair[0]][word_pair[1]]['weight'] += 1  # Fortalecer a conexão existente
            else:
                G.add_edge(*word_pair, weight=1)  # Adicionar nova conexão
    return G

G = build_cooccurrence_graph(df['text'])
```
## Ajuste na Visualização

Ajuste os parâmetros conforme for necessário e interessante para a sua analise.

```python


https://github.com/user-attachments/assets/a978a974-ffb8-4fe7-8936-6d174edf0926


# Obter todas as arestas e seus pesos
edges = G.edges(data=True)

# Filtrar para remover arestas entre palavras iguais
filtered_edges = [(u, v, data) for u, v, data in edges if u != v]

# Ordenar as arestas por peso em ordem decrescente
sorted_edges = sorted(filtered_edges, key=lambda x: x[2]['weight'], reverse=True)

# Manter apenas as 100 conexões mais fortes (ou menos se houver menos de 100)
top_edges = sorted_edges[:100]

# Criar um novo grafo com apenas as arestas mais fortes
G_filtered = nx.Graph()
G_filtered.add_edges_from((u, v, data) for u, v, data in top_edges)

# Aplicar normalização e escalonamento logarítmico aos pesos das arestas
edge_weights = np.array([data['weight'] for u, v, data in G_filtered.edges(data=True)])
scaled_edge_weights = np.log1p(edge_weights)

# Definir uma largura máxima para as arestas e limitar as larguras escaladas das arestas
max_edge_width = 3
scaled_edge_weights = np.clip(scaled_edge_weights, 0, max_edge_width)

# Criar um mapeamento das arestas para suas larguras limitadas
edge_widths = { (u, v): w for (u, v), w in zip(G_filtered.edges(), scaled_edge_weights) }

# Layout para visualização
pos = nx.spring_layout(G_filtered, k=1.0)  # Ajuste o valor de k conforme necessário

# Aumentar o tamanho dos nós
node_size = 700  # Ajuste conforme necessário
```

## Visualização de Dados

O notebook utiliza `pyvis` para criar visualizações interativas da rede de mensagens, permitindo uma análise mais profunda das interações entre os usuários.

https://github.com/user-attachments/assets/b4f9e4c9-3e21-4597-9d67-13b66952b733


## Conclusão

Este notebook fornece uma base para a análise de redes de mensagens do WhatsApp. Você pode expandir a análise adicionando mais funcionalidades e visualizações conforme necessário. Além disso permite a criação de um Dicionário para normalizar palavras.


