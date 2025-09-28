import pandas as pd
import numpy as np
import datetime

# --- Configurações da Simulação ---
DIAS_SIMULACAO = 7
INTERVALO_MINUTOS = 15
DATA_INICIAL = datetime.datetime.now() - datetime.timedelta(days=DIAS_SIMULACAO)

# --- Funções para gerar dados lógicos ---

# Simula a temperatura com variação diária (mais quente durante o dia)
def gerar_temperatura(timestamps):
    temperaturas = []
    for ts in timestamps:
        # Ciclo de 24h (2*pi radianos), com pico de calor às 15h
        hora_em_rad = ((ts.hour - 15) % 24) * (2 * np.pi / 24)
        variacao_diaria = -np.cos(hora_em_rad) * 2  # Variação de +/- 2 graus
        ruido_aleatorio = np.random.normal(0, 0.2)
        temperaturas.append(22.5 + variacao_diaria + ruido_aleatorio)
    return temperaturas

# Simula a luminosidade (em lux), zerando à noite
def gerar_luminosidade(timestamps):
    luminosidades = []
    for ts in timestamps:
        if 7 <= ts.hour < 19: # Luz apenas entre 7h e 19h
            hora_em_rad = ((ts.hour - 13) % 24) * (2 * np.pi / 24)
            variacao_diaria = (-np.cos(hora_em_rad) + 1) * 400 # Pico de 800 lux
            ruido_aleatorio = np.random.normal(0, 25)
            luminosidades.append(max(0, variacao_diaria + ruido_aleatorio))
        else:
            luminosidades.append(0) # Sem luz à noite
    return luminosidades

# Simula a ocupação (0 ou 1), com maior probabilidade em horário comercial e dias de semana
def gerar_ocupacao(timestamps):
    ocupacoes = []
    for ts in timestamps:
        # Fim de semana tem baixa probabilidade de ocupação
        if ts.weekday() >= 5: # 5 = Sábado, 6 = Domingo
            probabilidade = 0.05
        # Horário comercial (8h às 18h) tem alta probabilidade
        elif 8 <= ts.hour < 18:
            probabilidade = 0.85
        # Fora do horário comercial tem baixa probabilidade
        else:
            probabilidade = 0.10
        
        ocupacoes.append(1 if np.random.rand() < probabilidade else 0)
    return ocupacoes

# --- Geração do DataFrame ---

print("Iniciando a geração de dados simulados...")

# 1. Criar a série de timestamps
total_registros = (DIAS_SIMULACAO * 24 * 60) // INTERVALO_MINUTOS
timestamps = pd.to_datetime([DATA_INICIAL + datetime.timedelta(minutes=x*INTERVALO_MINUTOS) for x in range(total_registros)])

# 2. Criar um DataFrame para cada tipo de sensor
df_temp = pd.DataFrame({
    'timestamp': timestamps,
    'sensor_id': 'sensor_temp_01',
    'valor': gerar_temperatura(timestamps)
})

df_luz = pd.DataFrame({
    'timestamp': timestamps,
    'sensor_id': 'sensor_luz_01',
    'valor': gerar_luminosidade(timestamps)
})

df_ocup = pd.DataFrame({
    'timestamp': timestamps,
    'sensor_id': 'sensor_ocup_01',
    'valor': gerar_ocupacao(timestamps)
})

# 3. Concatenar todos os dataframes em um só
df_final = pd.concat([df_temp, df_luz, df_ocup], ignore_index=True)

# 4. Salvar em CSV
nome_arquivo = 'smart_office_data.csv'
df_final.to_csv(nome_arquivo, index=False, date_format='%Y-%m-%d %H:%M:%S')

print(f"Arquivo '{nome_arquivo}' gerado com sucesso com {len(df_final)} registros.")
print("\nAmostra dos dados gerados:")
print(df_final.head())