import time
import click
import botocore
import os
import json

SPECIFIED__SERVICE = 0
SPECIFIED__OPERATION = 1
SPECIFIED__INPUT_OUTPUT = 2


def list_dirs(path):
    return [d for d in os.listdir(path) if os.path.isdir("{}/{}".format(path, d))]


def ensure_api_version(api_version, event_source):
    if api_version == "latest":
        data_directory_name = botocore.__file__.replace("__init__.py", "data/{}".format(event_source))
        api_versions_found = list_dirs(data_directory_name)
        if len(api_versions_found) == 0:
            raise Exception("Could not find any api versions for event source: {}".format(event_source))
        if len(api_versions_found) == 1:
            return api_versions_found[0]
        else:
            orderable_times = [time.strptime(api_version_found, '%Y-%m-%d') for api_version_found in api_versions_found]
            orderable_times.sort(reverse=True)
            latest = orderable_times[0]
            return time.strftime('%Y-%m-%d', latest)


def get_data_for_service(service, api_version):
    data_file_path = botocore.__file__.replace("__init__.py", "data/{}/{}/service-2.json".format(service, api_version))
    with open(data_file_path) as data_file:
        data = json.loads(data_file.read())
        return data


def eval_shape(shape_name, data):
    members = data.get('shapes').get(shape_name).get('members')
    if members is None:
        return data.get('shapes').get(shape_name)
    result = {}
    for member_name in members.keys():
        member = members.get(member_name)
        member_name_modified = member_name[0].lower() + member_name[1:]
        result[member_name_modified] = eval_shape(member.get('shape'), data)
    return result


@click.command()
@click.argument('event_source', default="")
@click.option('--api_version',
              help='Version of the service API interacted with which resulted in the Cloudtrail event being triggered',
              default='latest')
def schema(event_source, api_version):
    """Prints the AWS Cloudtrail event that is dispatched when an API call occurs"""
    if event_source == "":
        data_directory_name = botocore.__file__.replace("__init__.py", "data/{}".format(event_source))
        services = list_dirs(data_directory_name)
        print("Services:")
        for service in services:
            print("- {}".format(service))
        return
        # exit(api_versions_found)

    event_sources = event_source.split(".")
    l_event_sources = len(event_sources)

    service_specified = event_sources[SPECIFIED__SERVICE]
    api_version = ensure_api_version(api_version, service_specified)
    data = get_data_for_service(service_specified, api_version)
    operations = data.get('operations')

    if l_event_sources > SPECIFIED__OPERATION:
        operation_specified = event_sources[SPECIFIED__OPERATION]
        if l_event_sources == SPECIFIED__INPUT_OUTPUT:
            exit("You need to specify input or output eg: {}.{}.output".format(service_specified, operation_specified))
        operation = operations[operation_specified]
        if l_event_sources > SPECIFIED__INPUT_OUTPUT:
            input_output_specified = event_sources[SPECIFIED__INPUT_OUTPUT]
            input_output = operation.get(input_output_specified)
            if input_output is None:
                exit("Result\n-----\n{}.{} has no {}".format(service_specified, operation_specified, input_output_specified))
            else:
                evaled = eval_shape(input_output.get('shape'), data)
        else:
            evaled = eval_shape(operation.get('shape'), data)
        print("Description\n------\n{}".format(operation.get('documentation')))
        print("\n\nResult\n------")
        print(json.dumps(evaled, indent=4))
    else:
        print('Operations: \n- {}'.format("\n- ".join(data.get('operations').keys())))
    return


if __name__ == '__main__':
    schema()
