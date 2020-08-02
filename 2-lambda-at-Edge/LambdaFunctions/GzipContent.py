import json
import zlib
import base64

CONTENT = """
<\!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Simple Lambda@Edge Static Content Response</title>
</head>
<body>
    <p>Hello from Lambda@Edge!</p>
</body>
</html>
"""

def lambda_handler(event, context): 
    # Generate HTTP OK response using 200 status code with a gzip compressed content HTML body
    buf = zlib.compress(CONTENT.encode('utf-8'))
    base64EncodedBody = base64.b64encode(buf).decode('utf-8')
    response = {
        'headers': {
            'content-type': [
                {
                    'key': 'Content-Type',
                    'value': 'text/html; charset=utf-8'
                }
            ],
            'content-encoding': [
                {
                    'key': 'Content-Encoding',
                    'value': 'gzip'
                }
            ]
        },
        'body': base64EncodedBody,
        'bodyEncoding': 'base64',
        'status': '200',
        'statusDescription': 'OK'
    }
    return response