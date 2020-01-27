import boto3
import click

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

def filter_instances(project):
    if not project: project = 'gabe-test'
    filters = [
        {"Name":"tag:billingProject","Values":[project]}
    ]
    inst = ec2.instances.filter(Filters=filters)

    return inst

@click.group()
def cli():
    '''CLI commands for EC2 instances'''

@cli.group('instances')
def instances():
    '''Commands for instance'''

@cli.group('volumes')
def volumes():
    '''Command for volumes'''

@cli.group('snapshots')
def snapshots():
    '''Command for snapshots'''

@instances.command('list')
@click.option('--project', default=None,
    help="requires a 'billingProject' tag on the instance")
def list_instances(project):
    '''List ec2 instances'''
    inst = filter_instances(project)
    for i in inst:
        tags = { t["Key"]: t["Value"] for t in i.tags or []}
        print(','.join((
            i.id,
            # i.instance_type,
            # i.placement['AvailabilityZone'],
            i.state["Name"],
            # i.public_dns_name,
            tags.get('billingProject', '<no project>'))))

@instances.command('stop')
@click.option('--project', default=None,
    help="requires a 'billingProject' tag on the instance")
def stop_instances(project):
    '''stop ec2 instances'''
    inst = filter_instances(project)
    for i in inst:
        print("Stopping {}...".format(i.id))
        i.stop()

@instances.command('start')
@click.option('--project', default=None,
    help="requires a 'billingProject' tag on the instance")
def start_instances(project):
    '''start ec2 instances'''
    inst = filter_instances(project)
    for i in inst:
        print("Starting {}...".format(i.id))
        i.start()

@volumes.command('list')
@click.option('--project', default=None,
    help="requires a 'billingProject' tag on the attached instance")
def list_volumes(project):
    '''List ec2 volumes'''
    inst = filter_instances(project)
    for i in inst:
        for v in i.volumes.all():
            print(','.join((
                v.id,
                i.id,
                (str(v.size) + 'GB'),
                # i.instance_type,
                # i.placement['AvailabilityZone'],
                v.state,
                # i.public_dns_name,
                # tags.get('billingProject', '<no project>')
            )))

    return

@snapshots.command('list')
@click.option('--project', default=None,
    help="requires a 'billingProject' tag on the attached instance")
def list_snapshots(project):
    '''List ec2 snapshots'''
    inst = filter_instances(project)
    for i in inst:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(','.join((
                    s.id,
                    v.id,
                    i.id,
                    s.progress,
                    s.state,
                    s.start_time.strftime("%c")
                )))

    return

@instances.command('snapshot')
@click.option('--project', default=None,
    help="requires a 'billingProject' tag on the attached instance")
def snapshot_instances(project):
    '''snapshot ec2 instances'''
    inst = filter_instances(project)
    for i in inst:
        print("Stopping {}".format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Creating snapshot of {}".format(v.id))
            v.create_snapshot(Description="Created by ec2util (GABE TEST)")
        print("Starting {}".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    cli()
