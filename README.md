## AWS CloudFront workshop

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
- Clone this repository
```
$ git clone https://github.com/vikasbajaj/cloudfront-workshop.git
```
- Create a EC2 Key Pair in your AWS Account in the region where you will create AWS resources as part of this workshop

- Install Postman on your laptop. We'll use Postman to send HTTP requests to CloudFront Distribution.
[Postman](https://www.postman.com/)

