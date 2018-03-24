### Chef ghosts ec2 nodes cleaner

a small utility to delete in a single command any node defined in chef, but not existing as a live node in EC2. a kind of *chef node cleanup routine*.

I created this because I am a terraform user and when an EC2 node is terminated (from an autoscale group...), there was no easy way to get the corresponding node in chef deleted also. This script does the job... although a lambda function coupled with AWS SNS would be better, but it would be a bit more work to implement.

## How to use ?

### Pre requisites

- python
- chefdk
- chef org access configured
- python packages installed: pychef, boto3
- AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables defined

### Command line usage

 help:
```
python ./clean_chef_ghosts_ec2nodes.py--help
```

usage example:
```
python ./clean_chef_ghosts_ec2nodes.py --aws-region us-east-1 --chef-environment production
```

usage with terraform null resource provider:
```
resource "null_resource" "chef_node_cleaner" {
  provisioner "local-exec" {
    command = "python ./clean_chef_ghosts_ec2nodes.py –aws-region ${aws_region} –chef-environment ${environment}"
  }
}
```