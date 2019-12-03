from app.core.aws import ec2
from app.core.slack_client import send_message
from app.settings.envs import DATA_ENGINEERING_CHANNEL
import argparse
import time
import datetime
from datetime import tzinfo


def check_instance_state(instance):
    return instance.state['Name']


def check_instance_running_time(instance):
    current_time = datetime.datetime.utcnow()
    if check_instance_state(instance) == 'running':
        return current_time - instance.launch_time.replace(tzinfo=None)
    else:
        return current_time - current_time


def instance_running_hours(instance):
    running_time = check_instance_running_time(instance)
    days = running_time.days
    hours, remainder = divmod(running_time.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f'{(days * 24) + hours}:{minutes:02}'


def monitor_instance_state(instance, expected_state):
    current_state = check_instance_state(instance)
    while expected_state != current_state:
        print(f'{get_instance_name(instance)} is {current_state}...')
        current_state = check_instance_state(instance)
        time.sleep(5)


def get_instance_name(instance):
    return [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'][0]


def all_instances():
    return {get_instance_name(i): i for i in ec2.instances.all()}


def start_instance(instance):
    if check_instance_state(instance) == 'running':
        print('Instance is already running.')
        return
    print(f'Starting instance {get_instance_name(instance)}...')
    instance.start()
    #monitor_instance_state(instance, 'running')
    send_message(DATA_ENGINEERING_CHANNEL, f'EC2 instance {get_instance_name(instance)} has been started.')
    print('Instance started!')


def stop_instance(instance):
    if check_instance_state(instance) == 'stopped':
        print('Instance has already been stopped.')
        return
    elif check_instance_state(instance) != 'running':
        print('Instance is already in a state of flux. Try again shortly.')
        return
    print(f'Stopping instance {get_instance_name(instance)}...')
    instance.stop()
    #monitor_instance_state(instance, 'stopped')
    send_message(DATA_ENGINEERING_CHANNEL, f'EC2 instance {get_instance_name(instance)} has been stopped.')
    print('Instance stopped!')


def get_instance(instance_name):
    try:
        instance = all_instances().get(instance_name)
        return instance
    except Exception as e:
        print(f'Unable to get instance {instance_name} - \n{e}')


def process_action(state):
    actions = {
        'start': start_instance,
        'stop': stop_instance,
    }
    return actions[state.lower()]


def action_instance(instance_name, state):
    instance = get_instance(instance_name)
    if not instance:
        print(f'Instance {instance_name} does not exist.')
        return
    print(f'Found instance {instance_name}...')
    action = process_action(state)
    action(instance)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instance_name', help='Name of the ec2 instance')
    parser.add_argument('state', choices=['start', 'stop'], help='START or STOP instance')

    args = parser.parse_args()
    action_instance(**vars(args))

