import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spark_session import build_spark

SILVER_TABLE = "lakehouse.silver.products"
GOLD_TABLE = "lakehouse.gold.product_category_summary"

spark = build_spark("ucv-query-iceberg")

print("\n=== SILVER ===")
spark.table(SILVER_TABLE).printSchema()
spark.table(SILVER_TABLE).show(20, truncate=False)
print("Silver rows:", spark.table(SILVER_TABLE).count())

print("\n=== GOLD ===")
spark.table(GOLD_TABLE).printSchema()
spark.table(GOLD_TABLE).show(50, truncate=False)
print("Gold rows:", spark.table(GOLD_TABLE).count())

spark.stop()
