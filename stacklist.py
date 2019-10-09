from datetime import datetime
import logging
import sys
import boto3
import botocore

cf = boto3.client('cloudformation')  # pylint: disable=C0103


def stacks_list():
    stacks = cf.list_stacks()['StackSummaries']
    return(stacks)


def stack_exists(stack_name):
    stacks = cf.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False

def parse_template(template):
    with open(template) as template:
        template_data = template.read()
    cf.validate_template(TemplateBody = template_data)
    return template_data




def main(stack_name,template):

    template_data = parse_template(template)
    
    params = {
        'StackName': stack_name,
        'TemplateBody': template_data
    }


    try:
        if stack_exists(stack_name):
            print('We have found a stack with the name given as parameter.Updating stack {}'.format(stack_name))
            stack_result = cf.update_stack(**params)
            waiter = cf.get_waiter('stack_update_complete')
        else:
            print('Creating stack {}'.format(stack_name))
            stack_result = cf.create_stack(**params)
            waiter = cf.get_waiter('stack_create_complete')
        
        print('Waiting for the stack to be ready')
        waiter.wait(StackName = stack_name)

        print(cf.describe_stacks(StackName=stack_result['StackId']))

    except botocore.exceptions.ClientError as e:
        error_message = e.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print('Will not update the stack as no changes were performed in the given template compared to the original configuration')
        else:
            raise




if __name__ == '__main__':
    main(*sys.argv[1:])





