from app.adhoc.manage_ec2 import check_instance_state, all_instances, check_instance_running_time
import pandas

EC2_STATE_DESTINATION = r'\\property.local\shared\HOMETRACK_ROOT\Techdev\Reports\ec2_states.csv'


def states_df():
    return pandas.DataFrame(data=list(current_instance_states()), columns=['name', 'state', 'running_time'])


def states_to_csv():
    df = states_df()
    df.to_csv(EC2_STATE_DESTINATION, index=False, header=True)


def current_instance_states():
    for instance_name, instance, in all_instances().items():
        yield(instance_name, check_instance_state(instance), str(check_instance_running_time(instance)))


if __name__ == '__main__':
    states_to_csv()
