import boto3
import os
from os import environ
from chef import autoconfigure, Node, Search
import argparse
import sys

def isValidAndNonEmptyString(str):
    return str != None or len(str)>0;


parser = argparse.ArgumentParser()

parser.add_argument("--aws-region", required=True, help="aws region used for ec2")
parser.add_argument("--dry-run", help="display what is planned to be done, do not perform any action", default=False)
parser.add_argument("--chef-environment", help="limit the scope of cleanup to a single chef environment", default="*")

args = parser.parse_args()

assert isValidAndNonEmptyString(environ.get('AWS_ACCESS_KEY_ID')), "AWS_ACCESS_KEY_ID must be set"
assert isValidAndNonEmptyString(environ.get('AWS_SECRET_ACCESS_KEY')), "AWS_SECRET_ACCESS_KEY must be set" 

api = autoconfigure()

print("connected {0} chef url: ".format(api.url))

session = boto3.Session(region_name=args.aws_region)
ec2 = session.resource('ec2')

print("connected to ec2 with key {0}".format(environ.get('AWS_ACCESS_KEY_ID')))

ec2_alive_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopping','pending','initializing','running','stopped']}])

ec2_alive_instance_ids = map(lambda ec2_instance: ec2_instance.instance_id, ec2_alive_instances)
chef_nodes = Search('node', "chef_environment:{0}".format(args.chef_environment))
chef_node_names = map(lambda chef_node: chef_node.object.name, chef_nodes)

def is_ec2_node_defined_in_region(ec2_instance_id_to_be_found, ec2_instance_ids):
    is_ec2_node_defined = False
    for ec2_instance_id in ec2_instance_ids:
        if(ec2_instance_id == ec2_instance_id_to_be_found):
            is_ec2_node_defined = True
    return is_ec2_node_defined

if (len(chef_nodes) == 0):
    print("No chef nodes registered... doing nothing")
else:
    print("{0} chef nodes found".format(len(chef_nodes)))
    for chef_node_row in chef_nodes:
        chef_node_name = chef_node_row.object.name
        chef_node = Node(chef_node_name)
        if chef_node.has_key('ec2'):
            chef_node_ec2_instance_id = chef_node['ec2']['instance_id']
            if(is_ec2_node_defined_in_region(chef_node_ec2_instance_id, ec2_alive_instance_ids)):
                print "chef node: {0} {1} exists as a live EC2 node: NO DELETION IN CHEF org".format(chef_node_name,chef_node_ec2_instance_id)
            else:
                print "chef node: {0} {1} exists in chef org, but not in ec2, hence WILL BE DELETED FROM CHEF org".format(chef_node_name,chef_node_ec2_instance_id)
                if(args.dry_run):
                    print "chef node: {0} would have been deleted from {0} -- avoid --dry-run option to delete it".format(api.url)
                else:
                    chef_node.delete()
                    print "chef node: {0} HAS BEEN DELETED IN CHEF org".format(chef_node_name)






