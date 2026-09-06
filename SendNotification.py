import requests

class SendNotification:        

    @staticmethod
    def send(output="HAMZA KADIMI", canal="normal") -> bool:
        topic = "KADIMIAnalysis" + canal  # choisissez un nom de topic pas trop trivial

        url = f"https://ntfy.sh/{topic}"
        try:
            response = requests.post(
                url,
                data=output.encode("utf-8"),
                timeout=15,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"Notification non envoyée : {error}")
            return False

        if response.ok:
            print("Notification envoyée ✅")
            return True
        else:
            print("Erreur lors de l’envoi :", response.status_code, response.text)
            return False
