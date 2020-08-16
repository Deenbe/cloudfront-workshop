https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/field-level-encryption.html



https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/



- Get a public key-private key pair. You must obtain and add the public key before you start setting up field-level encryption in CloudFront.

```
$ openssl genrsa -out private_key.pem 2048
```
- The resulting file contains both the public and the private key. To extract the public key from that file, run the following command:

```
$ openssl rsa -pubout -in private_key.pem -out public_key.pem
```

- Create a field-level encryption profile. Field-level encryption profiles, which you create in CloudFront, define the fields that you want to be encrypted.

- Create a field-level encryption configuration. A configuration specifies the profiles to use, based on the content type of the request or a query argument, for encrypting specific data fields. You can also choose the request-forwarding behavior options that you want for different scenarios.For example, you can set the behavior for when the profile name specified by the query argument in a request URL doesn’t exist in CloudFront.

- Link to a cache behavior. Link the configuration to a cache behavior for a distribution, to specify when CloudFront should encrypt data.