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

def 
def get_secret():
    # make sure you have a CloudFront Private Key stored in Secrets Manager with with name "cloudfrontkey"
    secret_name = "cloudfrontkey"
    region_name = "ap-southeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
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
    cf_distrubution = client.get_parameter(
        Name='cf-distribution-name',
        WithDecryption=False
    )
    return cf_distrubution['Parameter']['Value']

def getImagesBucketName():
    client = boto3.client('ssm')
    images_bucket = client.get_parameter(
        Name='images-bucket',
        WithDecryption=False
    )
    return images_bucket['Parameter']['Value']
    
getCloudFrontAccessKeyId():
    client = boto3.client('ssm')
    cloudfrontAccessKeyId = client.get_parameter(
        Name='CloudFrontAccessKeyID',
        WithDecryption=False
    )
    return cloudfrontAccessKeyId['Parameter']['Value']

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
        key_id = getCloudFrontAccessKeyId()
        print("Cloudfront Access Key Id is {0}".format(key_id))
        cf_distribution_name = getCloudFrontDistributionName()
        print("Cloudfront distribution name is {0}".format(cf_distribution_name))
        url = "https://" + cf_distribution_name + "/" + image_name
        expire_date = datetime.datetime(2020, 10, 10)
        cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

        # Create a signed url that will be valid until the specfic expiry date
        # provided using a canned policy.
        signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
        print(signed_url)
        print("looking for image name is {0} from bucket {1}".format(image_name,bucket_name))
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
        