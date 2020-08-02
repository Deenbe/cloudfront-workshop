#!/usr/bin/env bash

set -e

if [ -z $WORKSHOP_NAME ]; then
    echo "WORKSHOP_NAME environment variable is not set. Set environment variables by executing the following command $ source vars.env"
    exit 1
fi

if [ -z $KEY_PAIR ]; then
    echo "KEY_PAIR variable is not set. Set environment variables by executing the following command $ source vars.env"
    exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd)"

make_s3_lambda_buckets(){
    echo '*******************************************************************************'
    echo '********************** Uploading Lambda Zip files to S3 ***********************'
    echo '*******************************************************************************'
    mkdir zipfiles
    cd LambdaFunctions
    for path in ./*; do
        filename=`echo ${path##*/} | tr '[:upper:]' '[:lower:]'`
        filename_without_extension=$(echo "$filename" | cut -f 1 -d '.')
        zip ${filename_without_extension}.zip ${filename}
        cp ${filename_without_extension}.zip ../zipfiles/
        rm ${filename_without_extension}.zip
        aws s3 mb s3://lambda-${filename_without_extension}-${WORKSHOP_NAME} --region us-east-1
        aws s3 cp ../zipfiles/${filename_without_extension}.zip s3://lambda-${filename_without_extension}-${WORKSHOP_NAME}/${filename_without_extension}.zip --region us-east-1
    done
    echo '******************** Lambda Zip files uploaded to S3 Completed ***************'
}
deploy_stack() {
    echo '*******************************************************************************'
    echo '************** Deploying Lambda Functions CloudFormation Stack ****************'
    echo '*******************************************************************************'
    for path in ./*; do
        
        filename=`echo ${path##*/} | tr '[:upper:]' '[:lower:]'`
        filename_without_extension=$(echo "$filename" | cut -f 1 -d '.')
        ext="${filename##*.}"
        
        lambda_runtime="python3.8"
        lambda_handler="${filename_without_extension}.lambda_handler"
        

        if [ $ext == "js" ]; then
            lambda_runtime="nodejs12.x"
            lambda_handler="index.handler"
        fi
        
        aws cloudformation deploy \
        --no-fail-on-empty-changeset \
        --stack-name "lambda-${filename_without_extension}-${WORKSHOP_NAME}" \
        --template-file "${DIR}/cloudformation-stack/deploy-lambdas.yaml" \
        --capabilities CAPABILITY_IAM \
        --region us-east-1 \
        --parameter-overrides "LambdaRuntime=${lambda_runtime}" "Handler=${lambda_handler}" "BucketName=lambda-${filename_without_extension}-${WORKSHOP_NAME}" "FunctionName=${filename_without_extension}" "ZipfileName=${filename_without_extension}.zip"

    done
}
delete_stack() {
    echo "Deleting Cloud Formation stack"
    for path in zipfiles/*; do
        filename=`echo ${path##*/} | tr '[:upper:]' '[:lower:]'`
        filename_without_extension=$(echo "$filename" | cut -f 1 -d '.')

        aws cloudformation delete-stack --stack-name "lambda-${filename_without_extension}-${WORKSHOP_NAME}" --region us-east-1
        echo 'Waiting for the stack to be deleted, this may take a few minutes...'
        echo 'Done'
    done
}
delete_s3_buckets() {
    echo '*******************************************************************************'
    echo '******************** Deleting Lambda Zip files and Buckets ********************'
    echo '*******************************************************************************'
    cd zipfiles
    for path in ./*; do
        filename=`echo ${path##*/} | tr '[:upper:]' '[:lower:]'`
        filename_without_extension=$(echo "$filename" | cut -f 1 -d '.')
        aws s3 rm s3://lambda-${filename_without_extension}-${WORKSHOP_NAME}/${filename_without_extension}.zip --region us-east-1
        aws s3 rb s3://lambda-${filename_without_extension}-${WORKSHOP_NAME} --region us-east-1
    done
    cd ..
    rm -rf zipfiles
    echo '******************** Lambda Zip files and S3 buckets Deleted *****************'
}

action=${1:-"deploy"}

if [ "$action" == "delete" ]; then
    delete_stack
    delete_s3_buckets
    exit 0
fi

if [ "$action" == "deploy" ]; then
    make_s3_lambda_buckets
    deploy_stack
    exit 0
fi