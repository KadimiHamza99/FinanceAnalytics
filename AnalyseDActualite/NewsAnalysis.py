import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from bs4 import BeautifulSoup
import numpy as np

class NewsAnalysis:
    """
    Analyse des actualités récentes pour un ticker.
    Utilise FinBERT pour évaluer le sentiment global et donner un score /100.
    """

    def __init__(self, ticker, api_key="a2acf0a7c36e4aabb50cce04a723de94"):
        self.ticker = ticker
        self.api_key = api_key

        # Chargement du modèle FinBERT
        model_name = "yiyanghkust/finbert-tone"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)


    def _get_recent_news(self, company_name):
        """Utilise NewsAPI pour obtenir les dernières actualités sur les entreprises de PEA"""
        news = []
        # 1️⃣ NewsAPI
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": f"\"{company_name}\"",
            "language": "fr",
            "sortBy": "publishedAt",
            "pageSize": 20,
            "apiKey": self.api_key,
            "domains": "lesechos.fr,latribune.fr,bfmbusiness.com,reuters.com,bloomberg.com,investing.com,lefigaro.fr,capital.fr,wsj.com,nytimes.com,cnbc.com,ft.com,marketwatch.com,cnn.com,foxbusiness.com"
        }
        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            articles = r.json().get("articles", [])
            for a in articles:
                # Utiliser le champ "content" si disponible
                content = a.get('content', '')
                if not content:
                    # Si le contenu n'est pas disponible, suivre le lien pour obtenir le contenu complet
                    try:
                        article_response = requests.get(a['url'])
                        article_response.raise_for_status()
                        soup = BeautifulSoup(article_response.text, 'html.parser')
                        # Extraire le contenu de l'article (cette partie dépend de la structure de la page web)
                        article_body = soup.find('article').get_text() if soup.find('article') else 'Content not available'
                        content = article_body
                    except Exception as e:
                        content = f"Could not fetch content: {e}"
                news.append(f"{a['title']}. {content}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erreur NewsAPI : {e}")
        # Nettoyage doublons
        unique_news = list({n for n in news})
        return unique_news




    def _sentiment_finbert(self, text):
        """Retourne un score de sentiment entre -1 et +1, en incluant les sentiments neutres"""
        tokens = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**tokens)
        print(f"OUTPUT : {outputs}")
        scores = softmax(outputs.logits.detach().numpy()[0])
        print(f"SCORES : {scores}")
        labels = ["négatif", "neutre", "positif"]
        sentiment = dict(zip(labels, scores))
        print(sentiment)
        # Calcul du score de sentiment en incluant les sentiments neutres
        sentiment_score = (sentiment["positif"] * 1) + (sentiment["neutre"] * 0.5) + (sentiment["négatif"] * -1)
        # Normalisation du score de sentiment pour qu'il soit entre -1 et +1
        sentiment_score = sentiment_score / (sentiment["positif"] + sentiment["neutre"] + sentiment["négatif"])
        return sentiment_score

    def run(self, company_name):
        """Exécute l'analyse complète et renvoie un score entre 0 et 100"""
        news = self._get_recent_news(company_name)
        print(f"NEWS : {news}")
        if not news:
            return None, 50  # Score neutre s’il n’y a pas d’actualité

        sentiments = [self._sentiment_finbert(n) for n in news]
        avg_sentiment = np.mean(sentiments)
        print(f"AVERAGE SCORE : {avg_sentiment}")
        score = round((avg_sentiment + 1) * 50, 2)  # normalisation [-1,1] → [0,100]

        interpretation = (
            "🟢 Actualités globalement positives"
            if score > 60 else
            "🟠 Actualités mitigées"
            if score > 40 else
            "🔴 Actualités négatives"
        )

        return {"Score": score, "Interprétation": interpretation}, score
