#!/usr/bin/env bash

set -e

if [ -z $WORKSHOP_NAME ]; then
    echo "WORKSHOP_NAME environment variable is not set."
    exit 1
fi
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd)"
EC2_DNS_NAME=""

deploy_stack() {
    echo "Deploying Cloud Formation stack: \"${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1\" containing EC2..."
    aws cloudformation deploy \
        --no-fail-on-empty-changeset \
        --stack-name "${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1"\
        --template-file "${DIR}/cloudformation-stack/cloudfront-lab.yaml" \
        --capabilities CAPABILITY_IAM \
        --parameter-overrides "WorkshopName=${WORKSHOP_NAME}" "KeyPair=${KEY_PAIR}"
}
load_values_from_stack() {
    images_bucket_name=$(aws cloudformation describe-stacks \
        --stack-name="${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1" \
        --query="Stacks[0].Outputs[?OutputKey=='S3BucketImages'].OutputValue" \
        --output=text)

    html_bucket_name=$(aws cloudformation describe-stacks \
        --stack-name="${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1" \
        --query="Stacks[0].Outputs[?OutputKey=='S3BucketHtml'].OutputValue" \
        --output=text)
    html_secondary_bucket_name=$(aws cloudformation describe-stacks \
        --stack-name="${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1" \
        --query="Stacks[0].Outputs[?OutputKey=='S3BucketHtmlSecondary'].OutputValue" \
        --output=text)

    css_bucket_name=$(aws cloudformation describe-stacks \
        --stack-name="${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1" \
        --query="Stacks[0].Outputs[?OutputKey=='S3BucketCSS'].OutputValue" \
        --output=text)
    ec2_dns=$(aws cloudformation describe-stacks \
        --stack-name="${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1" \
        --query="Stacks[0].Outputs[?OutputKey=='EC2DNSName'].OutputValue" \
        --output=text)

    export IMAGES_BUCKET_NAME=${images_bucket_name}
    export HTML_BUCKET_NAME=${html_bucket_name}
    export HTML_SECONDARY_BUCKET_NAME=${html_secondary_bucket_name}
    export CSS_BUCKET_NAME=${css_bucket_name}
    EC2_DNS_NAME=$ec2_dns
} 

load_s3_files(){
    aws s3 cp s3/html/index.html s3://$HTML_BUCKET_NAME/index.html
    aws s3 cp s3/html/index-secondary.html s3://$HTML_SECONDARY_BUCKET_NAME/index-secondary.html
    aws s3 cp s3/html/403.html s3://$HTML_BUCKET_NAME/403.html
    aws s3 cp s3/html/504.html s3://$HTML_BUCKET_NAME/504.html
    aws s3 cp s3/html/502.html s3://$HTML_BUCKET_NAME/502.html
    

    aws s3 cp s3/images/cloudfront.jpg s3://$IMAGES_BUCKET_NAME/cloudfront.jpg
    aws s3 cp s3/images/control-pixel.jpg s3://$IMAGES_BUCKET_NAME/control-pixel.jpg
    aws s3 cp s3/images/treatment-pixel.jpg s3://$IMAGES_BUCKET_NAME/treatment-pixel.jpg
    aws s3 cp s3/css/style.css s3://$CSS_BUCKET_NAME/style.css
    aws s3 cp s3/css/style-error.css s3://$CSS_BUCKET_NAME/style-error.css
    aws s3 cp s3/css/new-style.css s3://$CSS_BUCKET_NAME/new-style.css
}

delete_s3_objects(){
    aws s3 rm s3://$HTML_BUCKET_NAME/index.html
    aws s3 rm s3://$HTML_SECONDARY_BUCKET_NAME/index-secondary.html
    aws s3 rm s3://$HTML_BUCKET_NAME/403.html
    aws s3 rm s3://$HTML_BUCKET_NAME/504.html
    aws s3 rm s3://$HTML_BUCKET_NAME/502.html
    
    aws s3 rm s3://$IMAGES_BUCKET_NAME/cloudfront.jpg
    aws s3 rm s3://$IMAGES_BUCKET_NAME/control-pixel.jpg
    aws s3 rm s3://$IMAGES_BUCKET_NAME/treatment-pixel.jpg
    aws s3 rm s3://$CSS_BUCKET_NAME/style.css
    aws s3 rm s3://$CSS_BUCKET_NAME/style-error.css
    aws s3 rm s3://$CSS_BUCKET_NAME/new-style.css
}
delete_stack() {
    echo "Deleting Cloud Formation stack"
    aws cloudformation delete-stack --stack-name "${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1"
    echo 'Waiting for the stack to be deleted, this may take a few minutes...'
    aws cloudformation wait stack-delete-complete --stack-name "${WORKSHOP_NAME}-distribution-with-multiple-origins-stack-1"
    echo 'Done'
}


action=${1:-"deploy"}

if [ "$action" == "delete" ]; then
    load_values_from_stack
    delete_s3_objects
    delete_stack
    exit 0
fi

if [ "$action" == "deploy" ]; then
    deploy_stack
    load_values_from_stack
    load_s3_files
    echo 'EC2 Public DNS name is ---- > ' $EC2_DNS_NAME
    exit 0
fi