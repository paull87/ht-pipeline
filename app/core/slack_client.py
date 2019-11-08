from app.core.aws import publish_sns


def send_message(channel, message):
    try:
        payload = {
            'channel': channel,
            'message': message,
        }
        return publish_sns('ht-slack-bot', payload)
    except Exception as e:
        print('Unable to send message via slack...')


if __name__ == '__main__':
    send_message('#pl-test', 'test message')
