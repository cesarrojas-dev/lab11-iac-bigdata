"""Busca el metadata.json vigente de Gold y genera tmp_lab13/gold_table.json.

No publica nada: la publicacion se hace con AWS CLI.
"""
import json
import os
import re

import boto3
from botocore.config import Config

BUCKET = "ucv-data-platform"
TABLE_PREFIX = "products/gold/product_category_summary/"
PATTERN = re.compile(r"/v(\d+)\.metadata\.json$")


def latest_metadata(keys):
    """Devuelve la clave con el numero de version mas alto (v10 > v9)."""
    found = [(int(m.group(1)), k) for k in keys if (m := PATTERN.search(k))]
    if not found:
        raise SystemExit("No hay metadata.json en Gold. Ejecute antes silver_to_gold.py.")
    return max(found)[1]


def main():
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
        config=Config(s3={"addressing_style": "path"}),
    )
    pages = s3.get_paginator("list_objects_v2").paginate(
        Bucket=BUCKET, Prefix=TABLE_PREFIX + "metadata/"
    )
    keys = [o["Key"] for page in pages for o in page.get("Contents", [])]
    location = f"s3://{BUCKET}/{latest_metadata(keys)}"
    table = {
        "Name": "product_category_summary",
        "TableType": "EXTERNAL_TABLE",
        "Parameters": {"table_type": "ICEBERG", "metadata_location": location},
        "StorageDescriptor": {"Location": f"s3://{BUCKET}/{TABLE_PREFIX}"},
    }
    os.makedirs("tmp_lab13", exist_ok=True)
    with open("tmp_lab13/gold_table.json", "w", encoding="utf-8") as f:
        json.dump(table, f, indent=2)
    print("Metadata vigente:", location)
    print("Archivo generado: tmp_lab13/gold_table.json")


if __name__ == "__main__":
    main()
