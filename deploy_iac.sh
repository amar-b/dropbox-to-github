pip3 install --target ./package dropbox dulwich
cd package
zip -r ../lambda_function.zip .
cd ..
rm -rf package
zip lambda_function.zip *.py

mv lambda_function.zip iac/lambda_function.zip
cd iac/
terraform init
terraform plan
terraform apply -auto-approve
#terraform destroy -auto-approve
rm lambda_function.zip
cd ..