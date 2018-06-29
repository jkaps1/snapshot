import boto3
import click

session = boto3.Session(profile_name='default')
ec2=session.resource('ec2')

def filter_instances(project):
        instances = []

        if project:
            filters = [{'Name':'tag:project', 'Values':[project]}]
            instances = ec2.instances.filter(Filters=filters)
        else:
            instances=ec2.instances.all()
        return instances

@click.group()
def instances():
    "Commands for Instances"

@instances.command('list')
@click.option('--project', default=None,help="Only for tags (project:val")
def list_instances(project):
    "List Instances"
    instances=filter_instances(project)

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        #print (tags.get('project'))
        print(', '.join((i.id,
                         i.instance_type,
                         i.placement['AvailabilityZone'],
                         i.state['Name'],
                         tags.get('project','<no project>')
                         )))
    return

@instances.command('stop')
@click.option('--project', default=None,help="Only for tags (project:val")
def stop_instances(project):
    "Stop EC2 instances"
    instances=filter_instances(project)
    for i in instances:
        print ("Stopping {0}...".format(i.id))
        i.stop()
    return
@instances.command('start')
@click.option('--project', default=None,help="Only for tags (project:val")
def stop_instances(project):
    "Stop EC2 instances"
    instances=filter_instances(project)
    for i in instances:
        print ("Starting {0}...".format(i.id))
        i.start()
    return


if __name__ == '__main__':
    instances()
