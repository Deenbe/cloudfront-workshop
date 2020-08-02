import json
 
def lambda_handler(event, context):
    response = event["Records"][0]["cf"]["response"]
    headers = response["headers"]
 
    headerNameSrc = "X-Amz-Meta-Last-Modified"
    headerNameDst = "Last-Modified"
 
    if headers.get(headerNameSrc.lower(), None):
        headers[headerNameDst.lower()] = [headers[headerNameSrc.lower()][0]]
        print(f"Response header {headerNameDst.lower()} was set to {headers[headerNameSrc.lower()][0]}")
 
    return response
