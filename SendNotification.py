import requests

class SendNotification:        

    @staticmethod
    def send(output = "HAMZA KADIMI", canal="normal"):
        topic = "KADIMIAnalysis" + canal  # choisissez un nom de topic pas trop trivial

        url = f"https://ntfy.sh/{topic}"
        response = requests.post(url, data=output.encode('utf‑8'))

        if response.status_code == 200:
            print("Notification envoyée ✅")
        else:
            print("Erreur lors de l’envoi :", response.status_code, response.text)
        
