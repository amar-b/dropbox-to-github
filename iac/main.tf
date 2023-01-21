
variable "aws_region" {
  default = "us-east-2"
}
variable "DROPBOX_CLIENT_ID" {
  description = "Dropbox client id"
}
variable "DROPBOX_CLIENT_SECRET" {
  description = "Dropbox client secret"
}
variable "DROPBOX_FOLDER_PATH" {
  description = "Dropbox folder path"
}
variable "DROPBOX_REFRESH_TOKEN" {
  description = "drop box long-lived refresh token"
}
variable "GITHUB_REPO_NAME" {
  description = "repo name in Github"
}
variable "GITHUB_TOKEN" {
  description = "Github personal access token"
}
variable "GITHUB_USER_NAME" {
  description = "Github username"
}

provider "aws" {
  region = "${var.aws_region}"
}

resource "aws_iam_role" "role" {
name               = "dropbox-to-github-lambda-execution-role"
assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "role_policy" {
  role        = aws_iam_role.role.name
  policy_arn  = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "lambda" {
  filename         = "lambda_function.zip"
  function_name    = "dropbox-to-github"
  role             =  aws_iam_role.role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  depends_on       = [aws_iam_role_policy_attachment.role_policy]
  memory_size      = 1024
  timeout          = 120
  environment {
    variables = {
        DBX_TO_GH_TMP_PATH = "/tmp"
        DROPBOX_CLIENT_ID = "${var.DROPBOX_CLIENT_ID}"
        DROPBOX_CLIENT_SECRET = "${var.DROPBOX_CLIENT_SECRET}"
        DROPBOX_FOLDER_PATH = "${var.DROPBOX_FOLDER_PATH}"
        DROPBOX_REFRESH_TOKEN = "${var.DROPBOX_REFRESH_TOKEN}"
        GITHUB_REPO_NAME = "${var.GITHUB_REPO_NAME}"
        GITHUB_TOKEN = "${var.GITHUB_TOKEN}"
        GITHUB_USER_NAME = "${var.GITHUB_USER_NAME}"
    }
  }
}
