from ddgs import DDGS
import re
from OllamaSession import OllamaSession
from datetime import datetime
import datetime

class SmartDataValidator:
    """
    Validateur intelligent utilisant votre OllamaSession existante
    """
    
    def __init__(self, model="mistral:7b"):
        self.ddgs = DDGS()
        self.model = model
    
    def validate_indicator(self, ticker, company_name, indicator_name, yf_value):
        """
        Valide un indicateur en 3 étapes: recherche → extraction LLM → décision
        Retourne: (valeur_finale, raison)
        """
        print(f"🔍 Validation de {indicator_name} pour {ticker}...")
        
        # 1. Recherche web rapide
        search_text = self._quick_search(ticker, company_name, indicator_name)
        if not search_text:
            return yf_value
        print(search_text)
        
        # 2. Extraction avec votre OllamaSession
        llm_value = self._extract_with_your_llm(indicator_name, search_text)

        # 3. Décision intelligente
        return self._smart_decision(yf_value, llm_value, indicator_name)
    
    def _quick_search(self, ticker: str, company_name: str, indicator: str):
        """
        Recherche rapide d'un indicateur économique pour une entreprise donnée.
        Utilise DuckDuckGo Search (ddgs) pour retourner les 10 résultats les plus pertinents.
        
        :param ticker: Le symbole boursier (ex: 'AAPL')
        :param company_name: Nom complet de l’entreprise (ex: 'Apple Inc')
        :param indicator: Indicateur recherché (ex: 'P/E ratio', 'EBITDA', 'Revenue growth', etc.)
        :return: Liste des 10 meilleurs résultats (titre, URL, extrait, date si disponible)
        """
        query_results = []
        now = datetime.datetime.now().year
        search_query = f"{indicator} {company_name} 2025"

        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=10)
            for r in results:
                query_results.append({
                    "title": r.get("title"),
                    "href": r.get("href"),
                    "snippet": r.get("body"),
                    "date": r.get("date", str(now))
                })

        # Tentative d’extraction d’année pour trier les résultats récents d’abord
        def extract_year(result):
            text = (result.get("snippet", "") or "") + " " + (result.get("title", "") or "")
            match = re.search(r'(20\d{2})', text)
            return int(match.group(1)) if match else now

        query_results = sorted(query_results, key=extract_year, reverse=True)
        return query_results
        
    def _extract_with_your_llm(self, indicator, text):
        """Utilise votre OllamaSession existante"""
        prompt = f"""
            Je te donne ce texte contenant des information sur l'indicateur {indicator}, je veux que tu m'extract la valeur de cet indicateur
            Si tu ne trouves pas cette valeur tu ecris 'null' et rien d'autre, sinon tu m'ecris la valeur trouvée sous format numérique
            N'ecris absolument aucun texte 
            Texte: {text[:1500]}
        """
        
        try:
            response = OllamaSession.ask_http(self.model, prompt)
            return self._parse_number(response)
        except:
            return None
    
    def _parse_number(self, text):
        """Extrait le premier nombre trouvé dans le texte, ou None si rien."""
        try:
            match = re.search(r'-?\d+\.?\d*', str(text).strip())
            if match:
                return float(match.group())
            return None
        except:
            return None
        
    def _smart_decision(self, yf_value, llm_value, indicator):
        """Prend la meilleure décision simplement"""
        print(f"La valeur sur Yahoo Finance est {yf_value}")
        print(f"La valeur générée par le LLM est de {llm_value}")
        if not llm_value:
            return self._parse_number(yf_value)
        if not yf_value:
            return self._parse_number(llm_value)
        if not yf_value and not llm_value:
            return None
        if(llm_value>1 and indicator in ["Return on equity", "Return on assets"]) : llm_value /= 100
        ecart = abs(yf_value - llm_value) / yf_value
        print(f"L'ecart entre les deux chiffres est de {ecart}")
        if ecart < 0.1:  # 10% d'écart
            return self._parse_number(yf_value)
        elif ecart < 0.3:  # 30% d'écart
            # Moyenne pondérée
            final = (yf_value * 0.8 + llm_value * 0.2)
            return self._parse_number(final)
        else:
            return self._parse_number(yf_value)