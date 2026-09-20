# FinanceAnalytics

FinanceAnalytics est un outil d'aide à l'analyse d'actions. Il combine des
données Yahoo Finance, une analyse fondamentale pondérée par secteur, une
analyse technique et une lecture des niveaux de Fibonacci. Le programme
produit un rapport dans le terminal et peut envoyer des alertes via ntfy.

> **Avertissement :** le résultat est un support d'analyse et non un conseil
> financier. Les données peuvent être absentes, retardées ou incorrectes.
> Toute décision doit être confrontée aux publications de l'entreprise, au
> contexte macroéconomique et au profil de risque de l'investisseur.

## Exécution

```bash
python -m pip install -r requirements.txt
python main.py CS.PA TTE.PA
python main.py --file tickers.txt
```

## Dashboard web local

Pour piloter le service depuis une interface graphique, lancez :

```bash
python web_app.py
```

Puis ouvrez [http://127.0.0.1:8765](http://127.0.0.1:8765). Saisissez un ou
plusieurs tickers séparés par des virgules et cliquez sur **Lancer l'analyse**.
Le dashboard réutilise les analyses existantes et affiche les scores, les
indicateurs, la recommandation technique et les zones Fibonacci.

Le fichier de tickers accepte un symbole par ligne. Les lignes vides et les
lignes dont le premier caractère utile est `#` sont ignorées.

## Stratégie d'analyse

### 1. Collecte et préparation

`yfinance` fournit les informations financières de l'entreprise et un
historique quotidien sur douze mois. Les champs absents ne sont pas remplacés
par une valeur optimiste : l'indicateur est affiché comme indisponible et sa
pondération est retirée du calcul concerné. Pour les cours, les colonnes
multi-indexées éventuellement renvoyées par Yahoo sont normalisées en séries
numériques simples.

### 2. Analyse fondamentale

L'analyse fondamentale cherche à répondre à cinq questions :

1. **Rentabilité :** l'entreprise transforme-t-elle son capital et son chiffre
   d'affaires en bénéfices et en flux de trésorerie ? Sont étudiés ROE, ROA,
   marges, croissance des bénéfices et FCF Yield.
2. **Liquidité :** peut-elle honorer ses engagements à court terme ? Current
   Ratio, Quick Ratio et flux de trésorerie opérationnel rapporté aux dettes
   courantes sont utilisés.
3. **Solvabilité :** la structure de dette est-elle soutenable ? Dette/Equity,
   Dette/EBITDA, dette/actifs, valeur comptable et couverture des intérêts
   mesurent le levier et la capacité de remboursement.
4. **Valorisation :** le prix payé est-il cohérent avec les bénéfices, la
   croissance et les actifs ? Forward P/E, Trailing P/E, Price to Book, PEG,
   rendement et taux de distribution sont comparés aux seuils sectoriels.
5. **Risque et marché :** quelle est l'exposition à la volatilité et au
   consensus ? Beta, position dans le range des 52 semaines et avis
   d'analystes complètent l'étude.

Chaque indicateur reçoit une note de 0 à 10 selon des seuils adaptés à son
secteur. Les poids sont également sectoriels : par exemple, le ROE et le
Price to Book sont plus importants pour les services financiers, tandis que
la dette et le dividende pèsent davantage pour les utilities et l'immobilier.
Le score fondamental est une moyenne pondérée normalisée sur 100. Une donnée
manquante ne doit donc ni créer un faux signal positif, ni rendre le score
artificiellement supérieur à 100.

### 3. Analyse technique

L'analyse technique est orientée vers une entrée moyen terme (quelques
semaines à plusieurs mois), pas vers le trading intraday. Elle est
volontairement prudente pour les actions françaises, souvent sensibles aux
gaps, aux publications et aux volumes faibles. Elle combine :

- **RSI (14)** et **stochastique** pour identifier les zones de survente ou de
  surachat et les retournements précoces ;
- **MACD** pour distinguer un croisement haussier sous zéro d'une tendance déjà
  mature ;
- **Bandes de Bollinger** pour situer le cours dans sa dispersion récente ;
- **OBV** pour confirmer ou infirmer le mouvement par les volumes ;
- **EMA 50/EMA 200** pour confirmer le régime de tendance ;
- **ADX** pour mesurer la force de tendance, sans confondre force et direction.
- **ATR (14)** et la moyenne de volume sur 20 séances pour contextualiser le
  risque et éviter les stops fixes.

Les notes sont pondérées puis renormalisées sur le poids réellement disponible.
Fibonacci contribue directement à ce score, puis intervient une seconde fois
comme filtre de cohérence : un score élevé n'est pas retenu comme signal
d'achat si la tendance est baissière, si la zone offre trop peu de marge de
sécurité ou si le ratio risque/rendement est défavorable.
Cette normalisation est importante lorsque l'historique ne permet pas de
calculer un indicateur ou lorsque Fibonacci est invalide.

### 4. Fibonacci et gestion du risque

Sur les 63 dernières séances (environ trois mois de cotation, ou la totalité
si elle est plus courte), le programme identifie le plus haut et le plus bas,
vérifie que le range représente au moins 4 % du cours, puis calcule les
retracements 23,6 %, 38,2 %, 50 %, 61,8 % et 78,6 %. Une tendance est
reconnue seulement lorsque la variation, la pente et l'alignement EMA50/EMA200
convergent.

- En tendance haussière, la zone d'entrée privilégie le retracement
  38,2–61,8 % et les extensions servent d'objectifs.
- En tendance baissière, l'outil ne propose pas automatiquement de vente à
  découvert ni de cible short ; il attend une confirmation de retournement.
- En tendance neutre, la zone autour de 50 % est privilégiée.

Le support, la résistance, le stop-loss et les objectifs sont calculés
ensemble. Le stop utilise l'ATR et un niveau technique afin de tenir compte de
la volatilité réelle. La sortie finale est une seule recommandation technique
intégrée : signal confirmé, configuration à surveiller, ou absence de signal.
Le ratio risque/rendement est informatif : il ne garantit pas l'atteinte d'un
objectif et doit être confronté à la liquidité, aux frais, au spread et aux
gaps d'ouverture d'Euronext.

### 5. Score global et alertes

Lorsque les deux analyses sont disponibles, le score global vaut :

```text
75 % × score fondamental + 25 % × score technique
```

Ce choix donne la priorité à la qualité économique de l'entreprise et utilise
la technique pour le timing. Les seuils d'affichage sont `80` (excellent),
`65` (bon), `50` (moyen) et inférieur à `50` (faible). Aucun score global n'est
produit si l'une des deux composantes manque.

Les alertes ntfy sont réservées aux opportunités combinant une bonne note
fondamentale et un signal technique suffisant, ou aux valeurs suivies dans le
portefeuille. Une notification échouée ne bloque pas le rapport local.

## Organisation du code

- `main.py` : interface en ligne de commande et résolution des tickers.
- `StockAnalyzer.py` : orchestration et restitution du rapport.
- `StockAnalysisUtils.py` : rendu des tableaux, formatage des scores et
  construction des notifications.
- `AnalyseFondamentale/` : métriques, pondérations sectorielles et
  interprétations.
- `AnalyseTechnique/` : indicateurs, Fibonacci et scoring technique.
- `Formatter.py` et `TablePrinter.py` : présentation uniquement.
- `tests/` : tests de fiabilité des scores, des données manquantes et des
  notifications.
