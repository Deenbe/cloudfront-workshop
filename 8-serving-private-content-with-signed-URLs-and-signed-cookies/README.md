## Private Content With Signed URL

### Introduction

### Learning Objectives

### Prerequisites
- Create an EC2 instance, select Amazon Linux 2
- Assign it an admin role as we will deploy this from EC2 due to a constraint with cryptography library that we are using to generate pre-signed url
- Login into EC2 instance and install git
```
$ sudo yum install git
```
- Install Python 3.7
```
$ sudo yum install python37
```
- Clone this repository
```
$ git clone https://github.com/vikasbajaj/cloudfront-workshop.git
```

- change directory to cloudfront-workshop/8-serving-private-content-with-signed-URLs-and-signed-cookies and run the following

```
$ source vars.env
```
- change directory LambdaFunction 

  - replace xxxxxxxxxx for secret_name with the secret name that you store in AWS Secret manager to store your CloudFront private key.

  - replace xxxxxxxxx for key_id with the CloudFront key name

- Deploy stack using the following

````
$ ./deploy.sh deploy
````






https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html


https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#generate-a-signed-url-for-amazon-cloudfront

https://cryptography.io/en/latest/

https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/



https://www.freecodecamp.org/news/escaping-lambda-function-hell-using-docker-40b187ec1e48/

https://www.thetopsites.net/article/53583089.shtml