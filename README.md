## Chef ghost nodes cleaner for EC2

a small utility to delete in a single command any node defined in chef, but not existing as a live node in EC2. a kind of *chef node cleanup routine*.

I created this because I am a terraform user and when an EC2 node is terminated (from an autoscale group...), there is no easy way to get the corresponding node deleted in Chef org.

This script does the job... although an AWS lambda function coupled with AWS SNS topic would be more efficient, but also a bit more work to implement.

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