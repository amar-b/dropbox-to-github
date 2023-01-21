pip3 install --target ./package dropbox dulwich
cd package
zip -r ../lambda_function.zip .
cd ..
rm -rf package
zip lambda_function.zip *.py

aws lambda update-function-code \
    --function-name dropbox-to-github \
    --zip-file fileb://lambda_function.zip \
    --no-cli-pager
rm lambda_function.zip