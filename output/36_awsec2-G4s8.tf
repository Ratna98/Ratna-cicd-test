# Generated Terraform for node awsec2-G4s8 (awsec2)







resource "aws_iam_role" "awsec2-G4s8_role" {
  name = "awsec2-G4s8-role"
  assume_role_policy = jsonencode({
    "Version":"2012-10-17",
    "Statement":[{"Action":"sts:AssumeRole","Principal":{"Service":"ec2.amazonaws.com"},"Effect":"Allow"}]
  })
}

resource "aws_iam_role_policy" "awsec2-G4s8_policy" {
  name = "awsec2-G4s8-policy"
  role = aws_iam_role.awsec2-G4s8_role.id
  policy = jsonencode({
    "Version":"2012-10-17",
    "Statement":[
    
      {
        "Effect":"Allow",
        "Action": [],
        "Resource": "*"
      }
    
    ]
  })
}

resource "aws_instance" "awsec2-G4s8" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
}


# Wiring: S3 -> Lambda event permission


