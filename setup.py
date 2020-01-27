from setuptools import setup
setup(
  name="ec2util",
  version="0.1.0",
  author="Gabriel Landes",
  author_email="gklandes@gmail.com",
  description="AWS Boto3 based CLI tool developed during training",
  license="GPLv3+",
  packages=["ec2util"],
  url="https://github.com/gklandes/awssnapshotdemo.git",
  install_requires=[
    'click',
    'boto3'
  ],
  entry_points='''
    [console_scripts]
    ec2util=ec2util.ec2util:cli
  '''
)