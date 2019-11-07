import slack
import ssl
from app.settings.secrets import SLACK_TOKEN


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
slack_client = slack.WebClient(token=SLACK_TOKEN, ssl=ssl_context)


def send_message(channel, message):
    try:
        return slack_client.chat_postMessage(channel=channel, text=message)
    except Exception as e:
        print('Unable to send message via slack...')


if __name__ == '__main__':
    send_message('#pl-test-2', 'hello there')
