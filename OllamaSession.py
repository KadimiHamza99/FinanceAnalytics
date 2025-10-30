import subprocess

class OllamaSession:

    @staticmethod
    def ask(prompt: str) -> str:
        print(f"Interrogation du modèle LLM mistral:7b en cours ...")

        try:
            # Utilisation de la commande Ollama en ligne de commande
            result = subprocess.run(
                ["ollama", "run", "mistral:7b", prompt],
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=160
            )

            response_text = result.stdout.strip()
            print(response_text)
            return response_text
        except subprocess.TimeoutExpired:
            print("⏰ Timeout : le modèle a mis trop de temps à répondre.")
            return "Erreur : délai dépassé."
        except subprocess.CalledProcessError as e:
            print("❌ Erreur de processus :", e.stderr)
            return f"Erreur : {e.stderr}"
        except Exception as e:
            print("❌ Erreur inattendue :", e)
            return str(e)