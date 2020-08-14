import boto3
import json

client = boto3.client('ssm')
response = client.get_parameter(
    Name='cloudfront-distribution',
    WithDecryption=False
)
print(response)