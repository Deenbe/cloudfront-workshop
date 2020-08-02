## Register a custom domain name with CloudFront Distribution and use ACM to generate public certificate

## Scenario steps
- Route 53: Register a domain
- create a Public Hosted Zone
- navigagte to Certificate Manager, to associate ACM public certificate with CF, you have to create a certificate in **us-east-1** region.
- request a public certificate
- enter domain name = cfworkshop.skillsreinvent.com
    **You need to change skillsreinvent.com with your domain name**
- choose DNS validation
- select **Create record in Route53**, click Create and then Continue.
- once you have a certificate in an **Issued** state, you can use it with the CloudFront.
- go back to your CloudFront Distribution
- click your Distribution and click on Edit
- inside the **Alternate Domain Names (CNAMEs)** textarea box, provide the domain name that you have associated with the certificate i.e. cfworkshop.skillsreinvent.com
- for **SSL Certificate**, select **Custom SSL Certificate** and select the certificate that you created in ACM.
- for **Custom SSL Client Support**, select **Clients that Support Server Name Indication (SNI) - (Recommended)**
- click **Yes, Edit**
- wait for your distribution to be deployed, once it is in Deployed state, go back to Route53
- click on your hosted zone that you created
- create a Record Set in your public hosted zone
- record Name = cfworkshop.skillsreinvent.com
- Value/Route traffic to: Alias to CloudFront distribution
- Enter your Distribution Domain name and create
- Try to access your distribition with your domain name

http://cfworkshop.skillsreinvent.com/index-secondary.html





