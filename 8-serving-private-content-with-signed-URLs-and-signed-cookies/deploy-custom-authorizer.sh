#!/usr/bin/env bash

set -e

if [ -z $WORKSHOP_NAME ]; then
    echo "WORKSHOP_NAME environment variable is not set. Set environment variables by executing the following command $ source vars.env"
    exit 1
fi

if [ -z $LAMBDA_FUNCTION_BUCKET_NAME ]; then
    echo "LAMBDA_FUNCTION_BUCKET_NAME variable is not set. Set environment variables by executing the following command $ source vars.env"
    exit 1
fi

if [ -z $IMAGES_BUCKET_NAME ]; then
    echo "IMAGES_BUCKET_NAME variable is not set. Set environment variables by executing the following command $ source vars.env"
    exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd)"

copy_custom_authorizer_lambda_deployment_package(){
    mkdir deployment_package_custom_authorizer_lambda
    cd deployment_package_custom_authorizer_lambda
    cp ../LambdaFunction/Custom_Authorizer.js .
    zip -r9 Custom_Authorizer.zip .
    aws s3 cp ./Custom_Authorizer.zip s3://${LAMBDA_FUNCTION_BUCKET_NAME}/Custom_Authorizer.zip
    cd ..
    echo "Custom Authorizer Lambda uploaded........."
}
copy_get_image_lambda_deployment_package(){
    mkdir deployment_package
    python3 -m venv v-env
    python3 -m venv v-env
    source v-env/bin/activate
    pip3 install cryptography
    deactivate
    cd v-env/lib/python3.7/site-packages
    mv _cffi_backend.cpython-37m-x86_64-linux-gnu.so _cffi_backend.so
    cp ../../../../LambdaFunction/Get_Image.py . 
    zip -r9 Get_Image.zip .
    cp Get_Image.zip ../../../../deployment_package/
    cd ../../../..
    rm -rf v-env
    aws s3 mb s3://${LAMBDA_FUNCTION_BUCKET_NAME}
    aws s3 cp deployment_package/Get_Image.zip s3://${LAMBDA_FUNCTION_BUCKET_NAME}/Get_Image.zip
    echo "Get Image Lambda uploaded........."
}
copy_images(){
    #aws s3 mb s3://${IMAGES_BUCKET_NAME}
    cd property-images
    for path in ./*; do
        filename=`echo ${path##*/}`
        echo "copying file ...... ${filename}"
        aws s3 cp ${filename} s3://${IMAGES_BUCKET_NAME}/${filename}
    done
    cd ..
}
deploy_stack() {
    echo '************** Deploying Lambda Functions CloudFormation Stack ****************'
         
    aws cloudformation deploy \
    --no-fail-on-empty-changeset \
    --stack-name "cloudfront-presigned-content-with-authorizer-lab-stack" \
    --template-file "${DIR}/cloudformation-stack/cloudfront-distribution-with-custom-authorizer.yaml" \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides "ImageBucket=${IMAGES_BUCKET_NAME}" "LambdaFunctionBucketName=${LAMBDA_FUNCTION_BUCKET_NAME}"
}
delete_stack() {
    echo "Deleting Cloud Formation stack"
    aws cloudformation delete-stack --stack-name "cloudfront-presigned-content-with-authorizer-lab-stack"
    echo 'Waiting for the stack to be deleted, this may take a few minutes...'
    aws cloudformation wait stack-delete-complete --stack-name "cloudfront-presigned-content-with-authorizer-lab-stack"
    echo 'Done'
}
delete_s3_buckets() {
    
    if ! aws s3api head-bucket --bucket $LAMBDA_FUNCTION_BUCKET_NAME 2>&1 | grep -q 'Not Found'; then
        echo '******************** Deleting Lambda Zip file and bucket ********************'
        aws s3 rm s3://${LAMBDA_FUNCTION_BUCKET_NAME}/Get_Image.zip
        aws s3 rm s3://${LAMBDA_FUNCTION_BUCKET_NAME}/Custom_Authorizer.zip
        aws s3 rb s3://${LAMBDA_FUNCTION_BUCKET_NAME}
        rm -rf deployment_package
        rm -rf deployment_package_custom_authorizer_lambda
    fi

    if ! aws s3api head-bucket --bucket $IMAGES_BUCKET_NAME 2>&1 | grep -q 'Not Found'; then
        echo '******************** Deleting JPEG files from S3 bucket ********************'
        cd property-images
        for path in ./*; do
           echo $path
           filename=`echo ${path##*/}`
           echo "removing file ...... ${filename}"
           aws s3 rm s3://${IMAGES_BUCKET_NAME}/${filename}
        done
        cd ..
    fi
}

action=${1:-"deploy"}

if [ "$action" == "delete" ]; then
    delete_s3_buckets
    delete_stack
    exit 0
fi

if [ "$action" == "deploy" ]; then
    echo '********************** Uploading Lambda Zip file to S3 ***********************'
    copy_get_image_lambda_deployment_package
    copy_custom_authorizer_lambda_deployment_package
    deploy_stack
    copy_images
    exit 0
fi