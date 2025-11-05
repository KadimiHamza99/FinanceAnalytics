from ddgs import DDGS
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from scipy.special import softmax
import numpy as np
import torch
import requests
from bs4 import BeautifulSoup


class NewsAnalysis:
    """
    Analyse des actualités récentes pour un ticker PEA.
    Utilise les flux RSS ZoneBourse + Boursorama pour extraire les news,
    puis FinBERT pour évaluer le sentiment global (score /100).
    """

    def __init__(self, ticker):
        self.ticker = ticker

        # Chargement du modèle FinBERT
        model_name = "yiyanghkust/finbert-tone"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        # 🔹 Traduction FR → EN (rapide et légère)
        self.translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

        # Label order from FinBERT: [neutral, positive, negative]
        self.labels = ["neutral", "positive", "negative"]

    # ============================================================
    def _get_recent_news(self, company_name):
        """
        Récupère les articles complets récents liés à une entreprise.
        1. Recherche des actualités via DuckDuckGo (DDGS)
        2. Télécharge et extrait le texte complet de chaque article
        Retourne : [{title, url, content}]
        """
        articles = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        query = f"{company_name} zonebourse"

        try:
            with DDGS() as ddgs:
                results = ddgs.news(query, max_results=10)
                for res in results:
                    url = res.get("url")
                    title = res.get("title", "").strip()

                    if not url:
                        continue

                    try:
                        response = requests.get(url, headers=headers, timeout=10)
                        if response.status_code != 200:
                            continue

                        soup = BeautifulSoup(response.text, "html.parser")

                        # Supprime les balises non pertinentes
                        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form", "aside"]):
                            tag.extract()

                       # Récupère le texte principal
                        content = soup.get_text(separator=" ", strip=True)

                        # Nettoyage du texte
                        content = ' '.join(content.split())

                        # Tronquer à 500 caractères maximum
                        content = content[:500]

                        # Ajouter l'article (même si court)
                        articles.append({
                            "title": title,
                            "url": url,
                            "content": content
                        })

                    except Exception as e:
                        print(f"Erreur pour {url}: {e}")

        except Exception as e:
            print(f"Erreur lors de la récupération des actualités : {e}")

        return articles

    # ============================================================

    def _sentiment_finbert(self, text):
        """Retourne un score de sentiment entre -1 et +1 basé sur FinBERT-Tone."""
        print("texte pour analyse de sentiment :", text)
        # --- Vérification du type d’entrée ---
        if not isinstance(text, str):
            if isinstance(text, dict) and "content" in text:
                text = text["content"]
            elif isinstance(text, list) and len(text) > 0 and isinstance(text[0], str):
                text = " ".join(text)
            else:
                raise ValueError(f"Le texte doit être une chaîne. Reçu : {type(text)}")

        # 1️⃣ Traduction FR → EN
        try:
            translated = self.translator(text, max_length=512)[0]["translation_text"]
        except Exception:
            translated = text  # fallback (si déjà anglais)
        
        print(f"Texte traduit pour analyse : {translated[:100]}...")

        # 2️⃣ Inférence FinBERT
        tokens = self.tokenizer(translated, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**tokens)

        probs = torch.nn.functional.softmax(outputs.logits, dim=1).numpy()[0]
        sentiment = dict(zip(self.labels, probs))

        # 3️⃣ Score pondéré (-1 à +1)
        score = sentiment["positive"] - sentiment["negative"]

        # 4️⃣ Label dominant
        label_map = {"positive": "positif", "neutral": "neutre", "negative": "négatif"}
        label = label_map[self.labels[np.argmax(probs)]]

        return {
            "score": float(score),
            "label": label,
            "probs": {
                "positif": float(sentiment["positive"]),
                "neutre": float(sentiment["neutral"]),
                "négatif": float(sentiment["negative"]),
            },
            "text_en": translated
        }

    def run(self, company_name):
        """Exécute l'analyse complète et renvoie un score entre 0 et 100."""
        news = self._get_recent_news(company_name)
        print(f"📰 {len(news)} actualités récentes trouvées pour {company_name}")
        # print(news)
        if not news:
            print(f"⚠️ Aucune actualité trouvée pour {company_name}")
            return {"Score": 50, "Interprétation": "⚪ Aucune actualité récente"}, 50

        sentiments = [self._sentiment_finbert(n) for n in news]
        avg_sentiment = sum(sentiment["score"] for sentiment in sentiments) / len(sentiments)
        print(f"Score moyen de sentiment: {avg_sentiment}")
        score = round((np.tanh(avg_sentiment * 1.5) + 1) * 50, 2)  # [-1,1] → [0,100]
        
        interpretation = (
            "🟢 Actualités globalement positives"
            if score > 60 else
            "🟠 Actualités mitigées"
            if score > 40 else
            "🔴 Actualités négatives"
        )

        return {"Score": score, "Interprétation": interpretation}, score
