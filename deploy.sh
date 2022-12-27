pip install --target ./package dropbox dulwich
cd package
zip -r ../lambda_function.zip .
cd ..
rm -rf package
zip lambda_function.zip lambda_function.py
aws lambda update-function-code \
    --function-name  KnowledgeRepoToGit \
    --zip-file fileb://lambda_function.zip \
    --no-cli-pager
rm lambda_function.zip