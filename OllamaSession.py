import subprocess

class OllamaSession:

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
