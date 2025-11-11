Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
# Installer wbgapi si nécessaire : pip install wbgapi

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import wbgapi as wb

# 1. Téléchargement des données WDI (2000-2023, panel pays-année)

indicators = {
    "NY.GDP.PCAP.CD": "gdp_pc",          # PIB par habitant (USD courant)
    "GC.XPN.TOTL.GD.ZS": "gov_spend",   # Dépenses publiques totales (% PIB)
    "SE.XPD.TOTL.GD.ZS": "edu_spend",   # Dépenses en éducation (% PIB)
    "SH.XPD.CHEX.GD.ZS": "health_spend",# Dépenses en santé (% PIB)
    "SL.UEM.TOTL.ZS": "unemp"            # Taux de chômage (%)
}

start_year = 2000
end_year = 2023

# On récupère les données pour tous les pays disponibles
df_raw = wb.data.DataFrame(indicators, time=range(start_year, end_year+1), labels=True)
df_raw.reset_index(inplace=True)

# 1. Garder uniquement les colonnes utiles
df_raw = df_raw[['Country', 'Series', *[f"YR{y}" for y in range(2000, 2024)]]]

# 2. Conversion du format wide vers long (années deviennent une colonne)
df_long = df_raw.melt(id_vars=['Country', 'Series'], var_name='Year', value_name='Value')

# 3. Nettoyage du nom d'année (YR2023 → 2023)
df_long['Year'] = df_long['Year'].str.extract(r'(\d+)').astype(int)

# 4. Pivot pour que chaque indicateur soit une colonne
df_pivot = df_long.pivot_table(index=['Country', 'Year'], columns='Series', values='Value').reset_index()

# 5. Renommer les indicateurs pour plus de lisibilité
df_pivot = df_pivot.rename(columns={
    'GDP per capita (current US$)': 'gdp_pc',
    'Expense (% of GDP)': 'gov_spend',
    'Government expenditure on education, total (% of GDP)': 'edu_spend',
    'Current health expenditure (% of GDP)': 'health_spend',
    'Unemployment, total (% of total labor force) (modeled ILO estimate)': 'unemp'
})

print(df_pivot.columns.tolist())
# 6. Supprimer les lignes avec valeurs manquantes sur les variables clés
df = df_pivot.dropna(subset=['gdp_pc', 'gov_spend', 'edu_spend', 'health_spend', 'unemp'])
df = df_pivot.dropna(subset=['gdp_pc', 'gov_spend', 'edu_spend', 'health_spend', 'unemp']).copy()

# Création variable transformée log_gdp (log naturel du PIB par habitant)
df['log_gdp'] = np.log(df['gdp_pc'])

# Création interaction edu_health = edu_spend * health_spend
df['edu_health'] = df['edu_spend'] * df['health_spend']

# 3. Analyse descriptive

desc_stats = df[['log_gdp', 'gov_spend', 'edu_spend', 'health_spend', 'unemp', 'edu_health']].describe()

print("\n=== Statistiques descriptives ===")
print(desc_stats)


# Sélection des variables d'intérêt
variables = ['log_gdp', 'gov_spend', 'edu_spend', 'health_spend', 'unemp', 'edu_health']

# Calcul de la matrice de corrélation
corr_matrix = df[variables].corr()

# Affichage de la matrice de corrélation
print("\nMatrice de corrélation :")
print(corr_matrix)

# Heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', center=0)
plt.title("Matrice de corrélation entre variables")
plt.show()



# Visualisation distributions
plt.figure(figsize=(14, 8))
for i, col in enumerate(['log_gdp', 'gov_spend', 'edu_spend', 'health_spend', 'unemp', 'edu_health'], 1):
    plt.subplot(2, 3, i)
    sns.histplot(df[col], kde=True, bins=30, color='skyblue')
    plt.title(f'Distribution de {col}')
plt.tight_layout()
plt.show()

# 4. Analyse en Composantes Principales (ACP)
... 
... # Variables à inclure dans l'ACP (exclu gdp_pc non transformé, on garde log_gdp)
... X = df[['log_gdp', 'gov_spend', 'edu_spend', 'health_spend', 'unemp', 'edu_health']]
... 
... # Standardisation
... scaler = StandardScaler()
... X_scaled = scaler.fit_transform(X)
... 
... # PCA
... pca = PCA(n_components=6)
... pca.fit(X_scaled)
... 
... # Variance expliquée par composante
... explained_var = pca.explained_variance_ratio_
... 
... print("\n=== Variance expliquée par composante ===")
... for i, var_ratio in enumerate(explained_var, 1):
...     print(f"PC{i} : {var_ratio:.3f}")
... 
... # Cercle des corrélations
... loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
... 
... plt.figure(figsize=(8,8))
... plt.axhline(0, color='grey', lw=1)
... plt.axvline(0, color='grey', lw=1)
... 
... for i, varname in enumerate(X.columns):
...     plt.arrow(0, 0, loadings[i,0], loadings[i,1], 
...               head_width=0.05, head_length=0.05, fc='red', ec='red')
...     plt.text(loadings[i,0]*1.15, loadings[i,1]*1.15, varname, color='black', ha='center', va='center')
... 
... plt.xlabel(f'PC1 ({explained_var[0]*100:.1f}%)')
... plt.ylabel(f'PC2 ({explained_var[1]*100:.1f}%)')
... plt.title("Cercle des corrélations - ACP")
... plt.grid()
... plt.axis('equal')
... plt.show()
