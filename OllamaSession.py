import subprocess
import requests

class OllamaSession:

    @staticmethod
    def ask_http(model: str, prompt: str) -> str:
        print(f"Interrogation du modèle LLM {model} en cours ...")
        
        try:
            # Utilisation de l'API HTTP d'Ollama
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False  # Important pour avoir la réponse complète en une fois
                },
                timeout=160
            )
            
            if response.status_code != 200:
                print("❌ Erreur Ollama API :", response.text)
                return "Erreur : impossible d'obtenir une réponse du modèle."
            
            # Parser la réponse JSON
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

    @staticmethod
    def ask(model: str, prompt: str) -> str:
        print(f"Chargement du modèle LLM {model} en cours ...")
        try:
            # Exécution du modèle via Ollama (local)
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt,              # ⚠️ envoyer une string, pas des bytes
                capture_output=True,
                text=True,       # important : text=True pour gérer str
                encoding="utf-8",          
                timeout=160
            )

            if result.returncode != 0:
                print("❌ Erreur Ollama :", result.stderr)
                return "Erreur : impossible d'obtenir une réponse du modèle."

            response = result.stdout.strip()

            print("\n📊 Analyse technique générée :")
            print(response)

            return response

        except subprocess.TimeoutExpired:
            print("⏰ Timeout : le modèle a mis trop de temps à répondre.")
            return "Erreur : délai dépassé."
        except Exception as e:
            print("❌ Erreur inattendue :", e)
            return str(e)
