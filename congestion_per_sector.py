import polars as pl

# Carregando o DataFrame
file_path = "./proc_data/df_c100.csv"
df = pl.read_csv(file_path)

# Obtendo valores únicos dos setores
unique_sectors = df.select("sector").unique().to_series()

print("Number of flights: ", df.height)

# Criando uma lista para armazenar os resultados
results = []

# Convertendo colunas para arrays para acelerar o acesso
df_id = df["id"].to_numpy()
df_ctime = df["c_time"].to_numpy()
df_atot = df["atot"].to_numpy()
df_sector = df["sector"].to_numpy()

# Iterando para calcular o congestionamento
for i in range(df.height):
    ref_id = df_id[i]
    print(f"Flight {i} - {ref_id}")
    ref_ctime = df_ctime[i]
    congestion = {str(sector): 0 for sector in unique_sectors}

    # Comparando apenas os voos relevantes
    mask = (df_ctime < ref_ctime) & (ref_ctime < df_atot)
    relevant_flights = df.filter(mask)

    # Contabilizando o congestionamento por setor
    for sector in relevant_flights["sector"].to_numpy():
        congestion[str(sector)] += 1

    # Adicionando o resultado para o voo atual
    result_row = {"id": ref_id, **congestion}
    results.append(result_row)

# Convertendo a lista de resultados para um DataFrame Polars
results_df = pl.DataFrame(results)

# Salvando os resultados em CSV
output_path = "./proc_data/congestion_per_sector.csv"
results_df.write_csv(output_path)

print(f"Congestion data saved to {output_path}")