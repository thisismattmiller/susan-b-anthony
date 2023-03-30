#!/bin/bash

rm -fr ./lambda_deploy
rm deploy.zip
mkdir ./lambda_deploy


cp 'lambda_function.py' ./lambda_deploy/
# cp 'embeddings.binary' ./lambda_deploy/
# cp 'docs.csv.gz' ./lambda_deploy/


cd ./lambda_deploy

zip -r9 ../deploy.zip *

