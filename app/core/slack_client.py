import slack
import ssl
from app.settings.envs import SLACK_TOKEN


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
slack_client = slack.WebClient(token=SLACK_TOKEN, ssl=ssl_context)


def send_message(channel, message):
    return slack_client.chat_postMessage(channel=channel, text=message)


if __name__ == '__main__':
    send_message('#pl-test', 'hello there')
