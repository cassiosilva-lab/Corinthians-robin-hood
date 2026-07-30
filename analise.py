"""
🏹 Corinthians: O Robin Hood do Brasileirão?
Análise do desempenho do Corinthians no Brasileirão Série A (2015-2024)

Autor: Cassio Bonfim
Dataset: Campeonato Brasileiro de Futebol - Série A (Kaggle - adaoduque)
"""

import pandas as pd

# =============================================================
# 1. CARREGAMENTO E TRATAMENTO DOS DADOS
# =============================================================

df = pd.read_csv('campeonato-brasileiro-full.csv', encoding='utf-8')
df['data_parsed'] = pd.to_datetime(df['data'], dayfirst=True)

# ATENÇÃO: O Brasileirão de 2020 foi disputado durante a pandemia de COVID-19.
# O campeonato iniciou em agosto/2020 e terminou em fevereiro/2021.
# Sem esse tratamento, o São Paulo aparecia como campeão de 2020 (incorreto),
# pois os jogos de jan-mar/2021 eram contabilizados no ano de 2021.
# Solução: atribuir os jogos de jan-mar/2021 ao campeonato de 2020.

def ano_campeonato(data):
    if data.year == 2021 and data.month <= 3:
        return 2020
    return data.year

df['ano_camp'] = df['data_parsed'].apply(ano_campeonato)

# Filtrar escopo: 2015 a 2024
df = df[(df['ano_camp'] >= 2015) & (df['ano_camp'] <= 2024)]
df = df.sort_values('data_parsed').reset_index(drop=True)

print(f"Total de jogos no período: {len(df)}")

# =============================================================
# 2. CALCULAR TABELA DE CLASSIFICAÇÃO FINAL POR ANO
# =============================================================

jogos = []
for _, row in df.iterrows():
    ano = row['ano_camp']
    mandante, visitante, vencedor = row['mandante'], row['visitante'], row['vencedor']
    if vencedor == mandante:
        jogos.append({'ano': ano, 'clube': mandante, 'pts': 3})
        jogos.append({'ano': ano, 'clube': visitante, 'pts': 0})
    elif vencedor == '-':
        jogos.append({'ano': ano, 'clube': mandante, 'pts': 1})
        jogos.append({'ano': ano, 'clube': visitante, 'pts': 1})
    else:
        jogos.append({'ano': ano, 'clube': mandante, 'pts': 0})
        jogos.append({'ano': ano, 'clube': visitante, 'pts': 3})

tabela = pd.DataFrame(jogos).groupby(['ano', 'clube']).sum().reset_index()
tabela['posicao'] = tabela.groupby('ano')['pts'].rank(method='min', ascending=False).astype(int)

# Categorizar posição final: G6 (1-6), Meio (7-16), Z4 (17-20)
def categoria(pos):
    if pos <= 6: return 'G6'
    elif pos >= 17: return 'Z4'
    else: return 'Meio'

tabela['categoria'] = tabela['posicao'].apply(categoria)

# =============================================================
# 3. FILTRAR JOGOS DO CORINTHIANS
# =============================================================

cort = df[(df['mandante'] == 'Corinthians') | (df['visitante'] == 'Corinthians')].copy()
cort['adversario'] = cort.apply(
    lambda r: r['visitante'] if r['mandante'] == 'Corinthians' else r['mandante'], axis=1
)
cort['ano'] = cort['ano_camp']

def resultado(row):
    if row['vencedor'] == 'Corinthians': return 'V'
    elif row['vencedor'] == '-': return 'E'
    else: return 'D'

cort['resultado'] = cort.apply(resultado, axis=1)

print(f"Total de jogos do Corinthians 2015-2024: {len(cort)}")

# =============================================================
# 4. DEFINIR OS 12 GRANDES DO FUTEBOL BRASILEIRO
# =============================================================

# Critério: tradição e títulos históricos no futebol brasileiro
# Independente do momento vivido pelo clube no período analisado
# (ex: Vasco e Cruzeiro passaram pela Série B, mas seguem sendo grandes)

grandes = [
    'Palmeiras', 'Sao Paulo', 'Santos', 'Flamengo', 'Fluminense',
    'Vasco', 'Botafogo-RJ', 'Gremio', 'Internacional', 'Cruzeiro', 'Atletico-MG'
]

cort['tipo'] = cort['adversario'].apply(lambda x: 'Grande' if x in grandes else 'Pequeno')

# Juntar com categoria e posição do adversário na tabela final daquele ano
cort = cort.merge(
    tabela[['ano', 'clube', 'posicao', 'categoria']],
    left_on=['ano', 'adversario'],
    right_on=['ano', 'clube'],
    how='left'
)

# =============================================================
# 5. FUNÇÃO DE APROVEITAMENTO
# =============================================================

def aproveitamento(serie_resultados):
    v = (serie_resultados == 'V').sum()
    e = (serie_resultados == 'E').sum()
    d = (serie_resultados == 'D').sum()
    j = len(serie_resultados)
    aprov = round((v * 3 + e) / (j * 3) * 100, 1)
    return v, e, d, j, aprov

# =============================================================
# 6. ANÁLISE 1 — 12 GRANDES FIXOS vs RESTO (GERAL)
# =============================================================

print("\n" + "=" * 60)
print("ANÁLISE 1 — 12 GRANDES FIXOS vs RESTO (2015-2024)")
print("=" * 60)

for tipo in ['Grande', 'Pequeno']:
    sub = cort[cort['tipo'] == tipo]['resultado']
    v, e, d, j, ap = aproveitamento(sub)
    print(f"{tipo:10s} | J:{j:3d} | V:{v:3d} E:{e:3d} D:{d:3d} | Aproveitamento: {ap}%")

# =============================================================
# 7. ANÁLISE 2 — ANO A ANO: GRANDES vs PEQUENOS
# =============================================================

print("\n" + "=" * 60)
print("ANÁLISE 2 — ANO A ANO | 12 GRANDES vs PEQUENOS")
print("=" * 60)
print(f"{'Ano'} | {'Grandes':>9} | {'Pequenos':>9} | Padrão")
print("-" * 52)

for ano in sorted(cort['ano'].unique()):
    g = cort[(cort['ano'] == ano) & (cort['tipo'] == 'Grande')]['resultado']
    p = cort[(cort['ano'] == ano) & (cort['tipo'] == 'Pequeno')]['resultado']
    _, _, _, _, ag = aproveitamento(g)
    _, _, _, _, ap = aproveitamento(p)
    padrao = '🏹 Robin Hood' if ag > ap else '❌ Anti-Robin'
    print(f"{ano} | {ag:>8}% | {ap:>8}% | {padrao}")

# =============================================================
# 8. ANÁLISE 3 — ANO A ANO: G6 vs MEIO vs Z4
# =============================================================

print("\n" + "=" * 60)
print("ANÁLISE 3 — ANO A ANO | G6 vs MEIO vs Z4")
print("=" * 60)
print(f"{'Ano'} | {'G6':>7} | {'Meio':>7} | {'Z4':>7} | Padrão")
print("-" * 55)

for ano in sorted(cort['ano'].unique()):
    cats = {}
    for cat in ['G6', 'Meio', 'Z4']:
        sub = cort[(cort['ano'] == ano) & (cort['categoria'] == cat)]['resultado']
        cats[cat] = aproveitamento(sub)[4] if len(sub) > 0 else None

    g6 = f"{cats['G6']}%" if cats['G6'] is not None else '-'
    meio = f"{cats['Meio']}%" if cats['Meio'] is not None else '-'
    z4 = f"{cats['Z4']}%" if cats['Z4'] is not None else '-'
    padrao = '🏹 Robin Hood' if (cats['G6'] and cats['Z4'] and cats['G6'] > cats['Z4']) else '❌ Anti-Robin'
    print(f"{ano} | {g6:>7} | {meio:>7} | {z4:>7} | {padrao}")

# =============================================================
# 9. ANÁLISE 4 — TIMES EM JEJUM
# =============================================================

print("\n" + "=" * 60)
print("ANÁLISE 4 — CORINTHIANS vs TIMES EM JEJUM")
print("=" * 60)

# Recalcular sequência sem ganhar jogo a jogo
df_seq = df.copy()
seq = {}
seq_list = []

for _, row in df_seq.iterrows():
    mandante, visitante, vencedor = row['mandante'], row['visitante'], row['vencedor']
    seq_m = seq.get(mandante, 0)
    seq_v = seq.get(visitante, 0)
    seq_list.append({
        'data': row['data'],
        'mandante': mandante,
        'visitante': visitante,
        'vencedor': vencedor,
        'seq_mandante': seq_m,
        'seq_visitante': seq_v
    })
    if vencedor == mandante:
        seq[mandante] = 0
        seq[visitante] = seq.get(visitante, 0) + 1
    elif vencedor == visitante:
        seq[visitante] = 0
        seq[mandante] = seq.get(mandante, 0) + 1
    else:
        seq[mandante] = seq.get(mandante, 0) + 1
        seq[visitante] = seq.get(visitante, 0) + 1

df_seq = pd.DataFrame(seq_list)

# Filtrar jogos do Corinthians onde adversário estava em jejum
cort_jejum = df_seq[
    ((df_seq['mandante'] == 'Corinthians') & (df_seq['seq_visitante'] >= 5)) |
    ((df_seq['visitante'] == 'Corinthians') & (df_seq['seq_mandante'] >= 5))
].copy()

cort_jejum['adversario'] = cort_jejum.apply(
    lambda r: r['visitante'] if r['mandante'] == 'Corinthians' else r['mandante'], axis=1
)
cort_jejum['seq_adv'] = cort_jejum.apply(
    lambda r: r['seq_visitante'] if r['mandante'] == 'Corinthians' else r['seq_mandante'], axis=1
)
cort_jejum['resultado'] = cort_jejum.apply(
    lambda r: 'V' if r['vencedor'] == 'Corinthians' else ('E' if r['vencedor'] == '-' else 'D'), axis=1
)

# Aproveitamento geral do Corinthians
_, _, _, _, aprov_geral = aproveitamento(cort['resultado'])
print(f"Aproveitamento GERAL do Corinthians 2015-2024: {aprov_geral}%")
print()
print(f"{'Jejum':>8} | J  | V  | E  | D  | Aprov%")
print("-" * 42)

for limite in [5, 7, 10]:
    sub = cort_jejum[cort_jejum['seq_adv'] >= limite]['resultado']
    if len(sub) == 0:
        continue
    v, e, d, j, ap = aproveitamento(sub)
    print(f"{limite:>5}+ jgs | {j:<3}| {v:<3}| {e:<3}| {d:<3}| {ap}%")

print()
print("Casos mais emblemáticos (maior jejum do adversário):")
top = cort_jejum.nlargest(5, 'seq_adv')[['adversario', 'seq_adv', 'resultado', 'data']]
print(top.to_string(index=False))
