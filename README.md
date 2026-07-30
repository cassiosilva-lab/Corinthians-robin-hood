# 🏹 Corinthians: O Robin Hood do Brasileirão?
### Análise do desempenho do Corinthians no Brasileirão Série A (2015-2024)

**Autor:** Cassio Bonfim
**Dataset:** Campeonato Brasileiro de Futebol - Série A (Kaggle - adaoduque)

> Analisei 10 temporadas do Brasileirão para testar uma hipótese: será que o Corinthians joga melhor contra os grandes rivais ou contra os times menores da tabela?

---

## 🧩 Contexto

O termo "Robin Hood" no futebol descreve um time que rende mais contra os grandes clubes (os "ricos") do que contra os times menores (os "pobres") — como se "roubasse pontos dos ricos para doar aos pobres" seria o oposto, mas o apelido descreve o time que bate de frente com os grandes e tropeça com os pequenos.

Como torcedor do Corinthians, sempre tive a impressão de que o time vivia esse padrão: "rouba pontos dos ricos" (rende bem contra os grandes) e "doa pontos pros pobres" (tropeça contra os times menores).

Em vez de ficar na opinião, decidi testar essa hipótese com dados reais de 10 temporadas do Brasileirão (2015–2024). O resultado surpreendeu: a crença de torcedor estava errada na maior parte do tempo.

---

## 🎯 Objetivo da Análise

- Comparar o aproveitamento do Corinthians contra clubes tradicionais ("Grandes") versus clubes menores ("Pequenos")
- Verificar se o padrão se repete ano a ano, ou se é só uma média que engana
- Analisar o desempenho por faixa de classificação do adversário (G6, Meio de tabela, Z4)
- Investigar se o Corinthians tira proveito de adversários "em jejum" de vitórias

---

## 📁 Estrutura do Repositório

```
📂 efeito-anti-robin-hood/
├── 📄 README.md
├── 🐍 analise.py                         # Script de análise em Python
├── 📊 campeonato-brasileiro-full.csv     # Base de dados (Kaggle)
├── 📑 dashboard_ano_a_ano.csv            # Dados pré-calculados: por temporada  
├── 📑 dashboard_desempenho_geral.csv     # Dados pré-calculados: por faixa de tabela
└── 📑 dashboard_geral.csv                # Dados pré-calculados: visão geral
```

---

## 🗃️ Sobre os Dados

Base pública do Campeonato Brasileiro Série A, disponível no Kaggle (autor: adaoduque), contendo todos os jogos do Brasileirão de anos anteriores. O escopo desta análise foi recortado para as temporadas de **2015 a 2024**.

> **Nota sobre o Brasileirão 2020:** por causa da pandemia, a temporada de 2020 só terminou em fevereiro de 2021. Sem tratamento, os jogos de jan-mar/2021 seriam contados como parte do campeonato de 2021 (o que daria um campeão errado). O script corrige isso reatribuindo esses jogos à temporada de 2020.

---

## 🔧 Ferramentas e Abordagem

- **Python (pandas)** — tratamento, cálculo e cruzamento dos dados
- **Looker Studio** — dashboard interativo (em desenvolvimento)

Este projeto foi desenvolvido com apoio de IA (Claude, Anthropic) como ferramenta de aprendizado — usada para estruturar a lógica de código e explicar conceitos de Python/pandas durante o processo. A escolha de metodologia, hipóteses e interpretação dos resultados é minha. Acredito que ser transparente sobre isso é mais honesto do que aparentar um domínio técnico que ainda estou construindo — e hoje, saber usar IA como ferramenta de trabalho é parte do que se espera de quem atua com dados.

---

## 🧭 Como o Script Funciona (passo a passo)

1. **Carregamento e tratamento** — lê o CSV, converte datas e corrige a temporada de 2020 (jogos de 2021 que pertencem ao campeonato anterior).
2. **Tabela de classificação por ano** — reconstrói a tabela final de cada temporada (pontos e posição de cada clube), a partir do resultado jogo a jogo.
3. **Filtro dos jogos do Corinthians** — isola todas as partidas do clube no período e classifica cada resultado como Vitória, Empate ou Derrota.
4. **Definição dos "12 Grandes"** — lista fixa de clubes tradicionais do futebol brasileiro (Palmeiras, São Paulo, Santos, Flamengo, Fluminense, Vasco, Botafogo, Grêmio, Internacional, Cruzeiro, Atlético-MG), independente da posição na tabela naquele ano específico — o critério é tradição histórica, não desempenho pontual.
5. **Cálculo de aproveitamento** — função que transforma vitórias/empates/derrotas em % de aproveitamento (fórmula padrão: pontos conquistados ÷ pontos possíveis).
6. **Quatro análises comparativas:**
   - Geral: Grandes vs. Pequenos (2015–2024)
   - Ano a ano: Grandes vs. Pequenos
   - Ano a ano: G6 (topo da tabela) vs. Meio vs. Z4 (rebaixamento)
   - Adversários "em jejum" (sem vencer há 5+, 7+ ou 10+ jogos)

---

## 📈 Principais Resultados

### Análise 1 — Aproveitamento geral (2015–2024)

Total de jogos no período: 3.799 | Total de jogos do Corinthians: 380

| Tipo de Adversário | Jogos | V | E | D | Aproveitamento |
|---|---|---|---|---|---|
| Clubes Grandes (12 fixos) | 198 | 67 | 61 | 70 | 44,1% |
| Clubes Pequenos (resto) | 182 | 91 | 52 | 39 | 59,5% |

### Análise 2 — Ano a ano (Grandes vs Pequenos)

| Ano | Grandes | Pequenos | Padrão |
|---|---|---|---|
| 2015 | 63,3% | 79,6% | ❌ Anti-Robin |
| 2016 | 33,3% | 64,8% | ❌ Anti-Robin |
| 2017 | 68,3% | 57,4% | 🏹 Robin Hood |
| 2018 | 33,3% | 45,8% | ❌ Anti-Robin |
| 2019 | 33,3% | 70,8% | ❌ Anti-Robin |
| 2020 | 35,0% | 55,6% | ❌ Anti-Robin |
| 2021 | 39,6% | 57,6% | ❌ Anti-Robin |
| 2022 | 47,9% | 63,6% | ❌ Anti-Robin |
| 2023 | 50,0% | 35,4% | 🏹 Robin Hood |
| 2024 | 38,3% | 61,1% | ❌ Anti-Robin |

O padrão "Anti-Robin Hood" (melhor rendimento contra pequenos do que contra grandes) se confirmou em **8 das 10 temporadas analisadas** — não é um efeito de média, é recorrente ano após ano.

Nas únicas **2 temporadas em que o Corinthians foi Robin Hood de verdade** — **2017 e 2023** — o time foi **campeão em apenas uma delas (2017)**. Ou seja: o ano do título coincide com a única vez em que a crença de torcedor realmente se confirmou nos dados.

### Análise 3 — Ano a ano por faixa de tabela (G6 vs Meio vs Z4)

Refinando a análise para olhar não a tradição do clube, mas a posição exata do adversário na tabela daquele ano (G6 = topo, Meio = meio de tabela, Z4 = rebaixamento):

| Ano | G6 | Meio | Z4 | Padrão |
|---|---|---|---|---|
| 2015 | 56,7% | 76,7% | 75,0% | ❌ Anti-Robin |
| 2016 | 33,3% | 42,6% | 83,3% | ❌ Anti-Robin |
| 2017 | 66,7% | 63,6% | 50,0% | 🏹 Robin Hood |
| 2018 | 16,7% | 40,7% | 66,7% | ❌ Anti-Robin |
| 2019 | 36,1% | 53,7% | 58,3% | ❌ Anti-Robin |
| 2020 | 33,3% | 38,3% | 88,9% | ❌ Anti-Robin |
| 2021 | 26,7% | 53,3% | 70,8% | ❌ Anti-Robin |
| 2022 | 41,7% | 61,1% | 70,8% | ❌ Anti-Robin |
| 2023 | 36,1% | 46,3% | 50,0% | ❌ Anti-Robin |
| 2024 | 25,0% | 53,7% | 75,0% | ❌ Anti-Robin |

O padrão se confirma e fica ainda mais evidente nessa visão: em **9 das 10 temporadas**, o Corinthians rendeu pior contra o G6 do que contra o Z4 — inclusive em anos como 2020, quando o aproveitamento contra o Z4 chegou a 88,9%, contra apenas 33,3% no G6. A única exceção foi, mais uma vez, **2017** — justamente o ano do título.

> Vale notar: por esse recorte (posição na tabela naquele ano específico), 2023 aparece como Anti-Robin — diferente da Análise 2, que usa a lista fixa de "12 Grandes" por tradição histórica. Isso mostra como o critério de comparação (tradição vs. posição no ano) muda o resultado, e reforça a importância de deixar clara a metodologia usada em cada análise.

---

## 📈 Análise Adicional — Corinthians vs. Times em Jejum

Uma segunda hipótese testada: será que o Corinthians "ajuda" adversários que estão numa sequência ruim sem vencer (jejum de vitórias)?

Aproveitamento geral do Corinthians no período (2015–2024): **51,5%**

| Jejum do adversário | Jogos | V | E | D | Aproveitamento |
|---|---|---|---|---|---|
| 5+ jogos sem vencer | 38 | 20 | 11 | 7 | 62,3% |
| 7+ jogos sem vencer | 16 | 10 | 5 | 1 | 72,9% |
| 10+ jogos sem vencer | 5 | 2 | 2 | 1 | 53,3% |

Contra adversários em jejum de 7+ jogos, o aproveitamento do Corinthians (72,9%) fica bem acima da média geral (51,5%) — indício de que o time realmente tende a se aproveitar mais de rivais em má fase, ao menos até uma certa extensão do jejum (com apenas 5 jogos na amostra de 10+, o dado de 53,3% já fica mais sujeito a variação por conta do tamanho da amostra).

**Casos mais emblemáticos** (maior jejum do adversário até o confronto):

| Adversário | Jejum (jogos) | Resultado | Data |
|---|---|---|---|
| Juventude | 20 | Derrota | 17/04/2024 |
| Avaí | 16 | Empate | 25/08/2019 |
| Avaí | 14 | Vitória | 27/11/2019 |
| Chapecoense | 10 | Vitória | 08/07/2021 |
| Juventude | 10 | Empate | 04/10/2022 |

O caso do Juventude em 2024 chama atenção: mesmo diante de um adversário com 20 jogos sem vencer, o Corinthians perdeu — mostrando que o "efeito jejum" não é garantia de resultado, é uma tendência estatística, não uma regra.

---

## 📊 Visualizações

*(Gráficos e dashboard a serem adicionados aqui.)*

---

## 💡 Principais Insights

1. **A hipótese testada era: o Corinthians é o Robin Hood do Brasileirão.** Os dados mostraram o contrário — o time é, na verdade, **Anti-Robin Hood**: rende mais contra clubes menores do que contra rivais tradicionais, com uma diferença de 15,4 pontos percentuais.
2. **O padrão é consistente, não pontual** — se repete em 8 de 10 anos, o que descarta a hipótese de acaso ou de uma única temporada atípica.
3. **A metodologia é replicável** — a mesma lógica (comparar performance por segmento de "adversário/cliente/situação") pode ser aplicada a problemas reais de negócio, como analisar performance de vendas por perfil de cliente ou de canal.

---

## 🚀 Aplicação Prática

Este projeto demonstra capacidade de:
- Tratamento e limpeza de dados brutos (incluindo correção de uma inconsistência temporal real na base)
- Construção de lógica de negócio em Python (cálculo de tabela de classificação, categorização de adversários)
- Formulação e teste de hipóteses com dados
- Segmentação e análise comparativa (geral, temporal, por faixa)
- Comunicação clara de resultados

> **Status:** Dashboard interativo em desenvolvimento (Looker Studio). Este README será atualizado com o link assim que estiver publicado.

---

## 👤 Autor

**Cassio Bonfim**
[LinkedIn](https://linkedin.com/in/cassiosilva-233b2bb7) • [GitHub](https://github.com/cassiosilva-lab)
