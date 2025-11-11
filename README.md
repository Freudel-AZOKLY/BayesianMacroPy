# BayesianMacroPy
BayesianMacroPy est un projet centré sur l'économétrie bayésienne avec Python et IA. Il réunie théorie, analyse empirique des déterminants du PIB par habitant, implémentation pratique avec PyMC/ArviZ, et comparaison prédictive avec le Machine Learning pour un workflow macroéconomique rigoureux et reproductible.



````markdown
# Analyse Macroéconomique Panel - Données WDI

## Résumé du Projet

Ce projet vise à analyser les indicateurs macroéconomiques des pays entre 2000 et 2023 à l’aide de **Python**. Les principaux indicateurs étudiés sont le **PIB par habitant**, les **dépenses publiques totales**, les **dépenses en éducation et santé**, et le **taux de chômage**.  

L'objectif est de révéler des **relations structurelles**, d’identifier les tendances et d’extraire des **insights significatifs** grâce à des analyses descriptives, des matrices de corrélation et une **Analyse en Composantes Principales (ACP)**.

---

## Source des Données

- **World Development Indicators (WDI) - Banque Mondiale**
- Indicateurs utilisés :
  - `NY.GDP.PCAP.CD` → PIB par habitant (USD courant)
  - `GC.XPN.TOTL.GD.ZS` → Dépenses publiques totales (% PIB)
  - `SE.XPD.TOTL.GD.ZS` → Dépenses en éducation (% PIB)
  - `SH.XPD.CHEX.GD.ZS` → Dépenses en santé (% PIB)
  - `SL.UEM.TOTL.ZS` → Taux de chômage (% force de travail totale)

Les données sont récupérées automatiquement via la bibliothèque Python [`wbgapi`](https://pypi.org/project/wbgapi/).

---

## Environnement

- **Python version :** 3.11.9
- **Packages requis :**
  ```bash
  pip install pandas numpy matplotlib seaborn scikit-learn wbgapi
````

---

## Étapes du Workflow

1. **Acquisition des données**

   * Téléchargement des indicateurs WDI pour tous les pays disponibles (2000-2023) via `wbgapi`.

2. **Préparation et nettoyage**

   * Transformation du format *wide* vers *long*.
   * Pivot pour avoir chaque indicateur comme colonne.
   * Renommage des variables pour plus de lisibilité.
   * Suppression des lignes avec valeurs manquantes.
   * Création de variables dérivées :

     * `log_gdp = log(PIB par habitant)`
     * `edu_health = dépense éducation * dépense santé`

3. **Analyse descriptive**

   * Statistiques descriptives : moyenne, médiane, écart-type, minimum, maximum.
   * Matrice de corrélation et heatmap.
   * Visualisation des distributions par histogrammes.

4. **Analyse en Composantes Principales (ACP)**

   * Standardisation des variables.
   * Réalisation de l’ACP sur 6 composantes principales.
   * Analyse de la variance expliquée.
   * Visualisation du cercle des corrélations (PC1 vs PC2).

---

## Utilisation

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/username/BayesianMacroPy.git
   cd BayesianMacroPy
   ```

2. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

3. Lancer l’analyse :

   ```bash
   python macro_panel_analysis.py
   ```

---

## Résultats

* **Statistiques descriptives** : résumé des principales variables.
* **Matrice de corrélation et heatmap** : visualisation des relations entre variables.
* **Histogrammes** : distribution des indicateurs clés.
* **ACP** : variance expliquée et cercle des corrélations pour interprétation des composantes.

---

## Licence

Ce projet est sous licence MIT.

---

## Auteur

Freudel AZOKLY


Veux‑tu que je fasse ça ?
```
