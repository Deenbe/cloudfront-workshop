import random

def lambda_handler(event, context):

    # Generate HTTP redirect response with 302 status code and Location header.
    request = event['Records'][0]['cf']['request']
    requesturi = request['uri']
    print(f"HTTP Redirect called ---- Request uri set to {requesturi}")
    if random.random() < 0.75:
        response = {
            'status': '302',
            'statusDescription': 'Found',
            'headers': {
                'location': [{
                    'key': 'Location',
                    'value': 'http://docs.aws.amazon.com/lambda/latest/dg/lambda-edge.html'
                }]
            }
        }
        return response
    else:
        return request