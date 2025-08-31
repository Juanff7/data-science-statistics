import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
#descarga datos de tigo(TIGO) desde 2020
ticker = "TIGO"

data = yf.download(ticker, start="2020-01-01", end="2025-08-18")
if data.empty:
    raise ValueError("No se han encontrado ninguna dato")

data.index = pd.DataFrame(data.index)

#============Retornos de logaritmos======================
data["ret_log"] = np.log(data["Close"]).diff()
df = data.dropna(subset=["ret_log"]).copy()
df["year"] = df.index.year

#============ ESTADISTICOS DESCRIPTIVOS ====================
print("=== Resumen global (retornos de logaritmos) ===")
print(df["ret_log"].describe(percentiles=[0.25, 0.50, 0.75]))

# STATS POR AÑO CON IQR Y Skew ############
def Stat_year(x : pd.Series) -> pd.Series:
    x = x.dropna()
    q1 =x.quantile(0.25); q3 =x.quantile(0.75)
    return pd.Serie({
        "Count": x.size,
        "Mean": x.mean(),
        "Median": x.median(),
        "Std": x.std(ddof=1),
        "var": x.var(ddof=1),
        "Min": x.min(),
        "Q1": q1,
        "Q3": q3,
        "Iqr": q3 - q1,
        "Max": x.max(),
        "Range": x.max() - x.min(),
        "Skew": x.skew(),
    })

year_stat = df.groupby("year")["ret_log"].apply(Stat_year)
print("Estadisticas por año ( ret_log) ====")
print(year_stat)

#======== Respuestas pedidas ==========
best_year = year_stat.year["mean"].idxmax()
best_year_mean =year_stat.loc[best_year,"mean"]
low_vol_year = year_stat["std"].idxmin()
low_vol_std = year_stat.loc[low_vol_year,"std"]
global_skew = skew(df["ret_log"], bias= False)



