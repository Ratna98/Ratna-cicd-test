# Generated Terraform for node awslambda-1 (awslambda)





resource "aws_iam_role" "awslambda-1_exec_role" {
  name = "awslambda-1-exec-role"
  assume_role_policy = jsonencode({
    "Version":"2012-10-17",
    "Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]
  })
}

resource "aws_iam_role_policy" "awslambda-1_exec_policy" {
  name = "awslambda-1-exec-policy"
  role = aws_iam_role.awslambda-1_exec_role.id
  policy = jsonencode({
    "Version":"2012-10-17",
    "Statement":[
      {
        "Effect":"Allow",
        "Action":["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],
        "Resource":"arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_lambda_function" "awslambda-1" {
  filename      = "lambda2.zip"
  function_name = "exampleLambdaFunction2"
  handler       = "app.handler"
  runtime       = "python3.9"
  role          = aws_iam_role.awslambda-1_exec_role.arn
}




# Wiring: S3 -> Lambda event permission


resource "aws_lambda_permission" "awslambda-1_allow_s3" {
  statement_id  = "AllowExecutionFromS3_awss3-0"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.awslambda-1.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::example-bucket-456"
}

