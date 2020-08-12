import boto3
import json

def get_image(event, context):
    image_name = event["queryStringParameters"]["image_name"]
    bucket_name = "presigned-images-cf-lab"
    try:
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
        