import boto3
from botocore.config import Config

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    config=Config(s3={"addressing_style": "path"}),
)

response = s3.list_objects_v2(
    Bucket="ucv-data-platform",
    Prefix="products/bronze/"
)

items = response.get("Contents", [])
for item in items:
    print(item["Key"], item["Size"])

print(f"Total Bronze files: {len(items)}")
