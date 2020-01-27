# EC2 Instances Controls
## List
`pipenv run python ec2util/ec2util.py instances list`

## Start
`pipenv run python ec2util/ec2util.py instances start`

## Stop
`pipenv run python ec2util/ec2util.py instances stop`

## Snapshot
`pipenv run python ec2util/ec2util.py instances snapshot`

# Volume Controls
## List
`pipenv run python ec2util/ec2util.py volumes list`

# Snapshot Controls
## List
`pipenv run python ec2util/ec2util.py snapshots list`

## Limit to Project
Use `--project=NAME` where NAME is the value of the "billingProject" tag to use
EX: `pipenv run python stop ec2util/ec2util.py instances list --project=some_tag`
Default value should be set in the environment
