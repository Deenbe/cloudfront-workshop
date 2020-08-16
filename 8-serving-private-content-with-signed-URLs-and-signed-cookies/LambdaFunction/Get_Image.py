import boto3
import json
import datetime
import base64
from botocore.exceptions import ClientError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner

def get_secret():
    secret_name = "cloudfrontkey"
    region_name = "ap-southeast-2"

    
    session = boto3.session.Session()
    # Reads a cloudfront private key from the secret manager, you need to create a secret manually with the name "cloudfrontkey"
    # storing cloudfront private key
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return str(get_secret_value_response["SecretString"])
    except ClientError as e:
        raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

def rsa_signer(message):
    private_key = serialization.load_pem_private_key(
        get_secret().encode(),
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

def getCloudFrontDistributionName():
    client = boto3.client('ssm')
    #cf-distribution-name parameter created in Systems Manager Parameter Store by Cloudformation stack
    cf_distrubution = client.get_parameter(
        Name='cf-distribution-name',
        WithDecryption=False
    )
    return cf_distrubution['Parameter']['Value']

def getCloudFrontKeyId():
    client = boto3.client('ssm')
    #you need to create a parameter manually in the parameter store with the name CloudFrontAccessKeyID, storing Cloudfront accesskey id
    cloudfront_access_keyid = client.get_parameter(
        Name='CloudFrontAccessKeyID',
        WithDecryption=False
    )
    return cloudfront_access_keyid['Parameter']['Value']

def getImagesBucketName():
    client = boto3.client('ssm')
    #images-bucket parameter created in Systems Manager Parameter Store by Cloudformation stack
    images_bucket = client.get_parameter(
        Name='images-bucket',
        WithDecryption=False
    )
    return images_bucket['Parameter']['Value']
    

def get_image(event, context):
    event_string = json.dumps(event)
    print(event_string)
    image_name = event["queryStringParameters"]["image_name"]
    user_name = event["queryStringParameters"]["user_name"]
    if user_name != 'king-kong':
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "You are trying to access premium property images, you need to subscribe for premium membership.",
            }),
              "headers":{ 'Access-Control-Allow-Origin' : '*' }
        }

    bucket_name = getImagesBucketName()
    print("Bucket name is {0}".format(bucket_name))
    
    try:
        #key_id = 'xxxxxxxxxxxxxxxxxxx'
        # reading value from parameter store
        key_id = getCloudFrontKeyId()
        print("Cloudfront Access key id is {0}".format(key_id))

        # reading value from parameter store    
        cf_distribution_name = getCloudFrontDistributionName()
        print("Cloudfront distribution name is {0}".format(cf_distribution_name))

        url = "https://" + cf_distribution_name + "/" + image_name
        expire_date = datetime.datetime(2020, 10, 10)
        cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

        # Create a signed url that will be valid until the specfic expiry date
        # provided using a canned policy.
        signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
        print("Pre-signed URL is {0}".format(signed_url))
                
        s3 = boto3.resource('s3')
        object = s3.Object(bucket_name,image_name).load()
        msg = "Image with name : " + image_name + " exists"
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": signed_url,
            }),
            "headers":{ 'Access-Control-Allow-Origin' : '*' }
        }
    except BaseException as error:
        print("*** Failure to retrieve Car Image - Please check your request ***")
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": str(error),
            }),
            "headers":{ 'Access-Control-Allow-Origin' : '*' }
        }
        