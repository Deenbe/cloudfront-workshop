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


Cloufront

- In the CloudFront console, choose Create Distribution.

- On the Select a delivery method for your content page, under Web, choose Get Started.

- On the Create Distribution page, for Origin Domain Name, paste your API's invoke URL, but remove the stage name. For example: https://qm85x0naai.execute-api.ap-southeast-2.amazonaws.com

- For Origin Path, enter your API's stage name with a slash in front of it (/stageName). Or, if you want to enter the stage name yourself when invoking the URL, don't enter an Origin Path.
  - enter /demo
- For Minimum Origin SSL Protocol, it's a best practice to choose TLSv1.2 only. 

- For Origin Protocol Policy, choose HTTPS Only. API Gateway doesn't support unencrypted (HTTP) endpoints.

- Allowed HTTP Methods: GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE

- Cache Policy: Managed-CachingDisabled

- Origin Request Policy: Click Create a new policy
  - Name: Cloudfront-Workshop-Origin-Policy
  - Headers: Choose the following
    - Access-Control-Request-Headers
    - Access-Control-Request-Method
    - Origin
  - Cookies: All
  - QueryString: All
- Leave all the setting as is and "Create Distribution"
- Once Distribution is "Deployed"
- Open Postman and test
- Createa GET request and for url add the following
  - CLOUD_DISTRIBUTION_DOMAIN_NAME/images?image_name=property-1.jpeg
- 



distribution-identity-secret=cloudfront-workshop-17aug



https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html


https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#generate-a-signed-url-for-amazon-cloudfront

https://cryptography.io/en/latest/

https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/



https://www.freecodecamp.org/news/escaping-lambda-function-hell-using-docker-40b187ec1e48/

https://www.thetopsites.net/article/53583089.shtml


https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-cloudfront-distribution/

https://stackoverflow.com/questions/56181978/restrict-direct-api-gateway-calls-unless-its-from-cloudfront



https://stackoverflow.com/questions/32825413/how-do-you-add-cloudfront-in-front-of-api-gateway