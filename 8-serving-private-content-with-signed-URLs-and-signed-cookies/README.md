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

- Once deployed, open the Postman test harness and run "Access Premium Property Images" request as shown in the image below

- Note: there are two request params that we are passing
  - image_name=property-1.jpeg
  - user_name=vik

![](./images/access-premium-images.png)

- You should see **You are trying to access premium property images, you need to subscribe for premium membership** message as shown in the image below.

![](./images/access-premium-images-access-denied.png)

- Now we will resend the request with a user name who has (let's assume) got the premium membership
- change the user name to **king-kong** (pls don't ask me why this name :-) )
  - image_name=property-1.jpeg
  - user_name=king-kong

- As shwon below in the image

![](./images/access-premium-images-valid-user.png)

- you should see a response returing **Pre-Signed URL** as you accessed the image with a paid user name, as shown below

![](./images/access-premium-images-valid-user-presigned-url.png)

- Copy presigned URL and access the 



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