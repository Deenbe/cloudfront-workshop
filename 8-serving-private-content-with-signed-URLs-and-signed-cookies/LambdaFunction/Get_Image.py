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
    secret_name = "xxxxxxxxxxxxxxxxxx"
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
        #print(get_secret_value_response)
        #print(get_secret_value_response["SecretString"])
        return str(get_secret_value_response["SecretString"])
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
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


def get_image(event, context):
    event_string = json.dumps(event)
    print(event_string)
    image_name = event["queryStringParameters"]["image_name"]
    bucket_name = "presigned-images-cf-lab"
    try:
        key_id = 'xxxxxxxxxxxxxxxxxxx'
        url = 'http://d2949o5mkkp72v.cloudfront.net/hello.txt'
        expire_date = datetime.datetime(2017, 1, 1)
        cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

        # Create a signed url that will be valid until the specfic expiry date
        # provided using a canned policy.
        signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
        print("****************Pre-signed URL is ****************")
        print(signed_url)
        print("****************Pre-signed URL end ****************")
        print("looking for image name is {0} from bucket {1}".format(image_name,bucket_name))
        s3 = boto3.resource('s3')
        object = s3.Object(bucket_name,image_name).load()
        msg = "Image with name : " + image_name + " exists"
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": msg,
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
        