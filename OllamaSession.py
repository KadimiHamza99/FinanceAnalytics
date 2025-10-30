import requests
import time

class OllamaSession:
    def __init__(self, base_url="http://localhost:11434", timeout=180):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def wait_for_server(self, max_retries=10, retry_interval=5):
        for _ in range(max_retries):
            try:
                response = self.session.get(f"{self.base_url}", timeout=10)
                if response.status_code == 200:
                    print("Serveur Ollama est prêt.")
                    return True
            except requests.exceptions.RequestException as e:
                print(f"Tentative de connexion au serveur Ollama : {e}")
            time.sleep(retry_interval)
        print("Impossible de se connecter au serveur Ollama après plusieurs tentatives.")
        return False

    def ask_http(self, model: str, prompt: str) -> str:
        if not self.wait_for_server():
            return "Erreur : impossible de se connecter au serveur Ollama."

        print(f"Interrogation du modèle LLM {model} en cours ...")

        try:
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=self.timeout
            )

            if response.status_code != 200:
                print("❌ Erreur Ollama API :", response.text)
                return "Erreur : impossible d'obtenir une réponse du modèle."

            result = response.json()
            response_text = result.get("response", "").strip()

            print(response_text)
            return response_text
        except requests.exceptions.Timeout:
            print("⏰ Timeout : le modèle a mis trop de temps à répondre.")
            return "Erreur : délai dépassé."
        except requests.exceptions.ConnectionError:
            print("❌ Erreur de connexion : assurez-vous que Ollama est démarré (ollama serve)")
            return "Erreur : impossible de se connecter au serveur Ollama."
        except Exception as e:
            print("❌ Erreur inattendue :", e)
            return str(e)