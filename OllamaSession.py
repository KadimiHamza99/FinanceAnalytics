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
                timeout=180
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
        print(f"Interrogation du modèle LLM {model} en cours ...")

        try:
            # Utilisation de la commande Ollama en ligne de commande
            process = subprocess.Popen(
                ["ollama", "run", model, prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            stdout, stderr = process.communicate(timeout=620)

            if process.returncode != 0:
                return f"Erreur : {stderr}"

            response_text = stdout.strip()
            print(response_text)
            return response_text
        except subprocess.TimeoutExpired:
            process.kill()
            return f"Erreur : délai dépassé après 620 secondes."
        except Exception as e:
            print("❌ Erreur inattendue :", e)
            return str(e)