# Terraform CI/CD Dynamic Template Generator

This project dynamically generates Terraform (`.tf`) files for AWS services based on a JSON graph input containing **nodes** (services) and **edges** (relationships/operations).  
Each generated `.tf` file includes only the **required resources, IAM roles, policies, and permissions** using the **least-privilege principle**.

---

# 📘 Features

### ✔ Dynamic Terraform generation  
Automatically creates `.tf` files under `output/` based on JSON input.

### ✔ Least-Privilege IAM  
Permissions are derived from edge operations (e.g., `read`, `write`, `events`).

### ✔ Extensible service mapping  
New AWS services or operations can be added without modifying the generator.

### ✔ Jinja2 templating  
All Terraform code is generated using Jinja2 templates.

### ✔ CI/CD with GitHub Actions  
Pipeline automatically:
- Runs generator  
- Produces Terraform files  
- Runs `terraform init`, `fmt`, and `validate`

---

# 📂 Project Structure

Ratna-cicd-test/
│
├── generator/
│ └── generator.py
│
├── generator_map/
│ └── service_map.json 
│
├── templates/
│ ├── resource.tf.j2 
│ └── iam_policy.json.j2 
│
├── examples/
│ ├── example1_single_target.json 
│ └── example2_multiple_targets.json
│
├── output/ # Generated TF files
│
├── samples_tf/ # Sample final TF outputs
│
└── .github/workflows/
└── cicd.yml # GitHub Actions CI
📦 Deliverables (Included in Repo)

✔ Dynamic generator script

✔ Mapping file

✔ Templates

✔ Example JSON inputs

✔ Generated sample TF files

✔ Fully working CI/CD pipeline

✔ This README documentation

🏁 Summary

This project provides a complete system to:

Convert architecture JSON definitions into Terraform

Build least-privilege IAM permissions

Automate generation through CI/CD

Extend easily to any AWS service
