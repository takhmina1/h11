from django.conf import settings
import requests

def upload_sms():
    xml_data = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <message>
            <login>{settings.NIKITA_LOGIN}</login>
            <pwd>{settings.NIKITA_PASSWORD}</pwd>
            <sender>{settings.NIKITA_SENDER}</sender>
            <text>Список товаров успешно обновлен!</text>
            <phones>
                <phone>{settings.GLOBUS_NUMBER}</phone>
            </phones>
        </message>
    """

    headers = {"Content-Type": "application/xml"}

    url = "https://smspro.nikita.kg/api/message"

    response = requests.post(url, data=xml_data.encode("utf-8"), headers=headers)

    if response.status_code == 200:
        return True
    return False
