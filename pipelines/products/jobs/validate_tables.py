import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyspark.sql import functions as F
from spark_session import build_spark

SILVER_TABLE = "lakehouse.silver.products"
GOLD_TABLE = "lakehouse.gold.product_category_summary"


def check(name, ok):
    print(f"[{'OK' if ok else 'FAIL'}] {name}")


spark = build_spark("ucv-validate-iceberg")

silver = spark.table(SILVER_TABLE)
gold = spark.table(GOLD_TABLE)

print("\n=== VALIDACION SILVER ===")
total = silver.count()
null_ids = silver.filter(F.col("product_id").isNull()).count()
bad_price = silver.filter(~(F.col("price") > 0)).count()
distinct_ids = silver.select("product_id").distinct().count()
duplicates = total - distinct_ids

print(f"Filas Silver: {total}")
print(f"product_id nulos: {null_ids}")
print(f"price <= 0 o nulo: {bad_price}")
print(f"product_id duplicados: {duplicates}")
check("product_id no nulo", null_ids == 0)
check("price > 0", bad_price == 0)
check("product_id sin duplicados", duplicates == 0)

print("\n=== VALIDACION GOLD ===")
gold_rows = gold.count()
distinct_cat = gold.select("category").distinct().count()
null_cat = gold.filter(F.col("category").isNull()).count()
bad_count = gold.filter(~(F.col("product_count") > 0)).count()
bad_avg = gold.filter(~(F.col("average_price") > 0)).count()

print(f"Filas Gold: {gold_rows}")
print(f"Categorias distintas: {distinct_cat}")
check("Una fila por category", gold_rows == distinct_cat)
check("category no nula", null_cat == 0)
check("product_count > 0", bad_count == 0)
check("average_price > 0", bad_avg == 0)

print("\n=== SUMA DE CONTROL ===")
gold_sum = gold.agg(F.sum("product_count")).first()[0]
print(f"Suma product_count Gold: {gold_sum} | Filas Silver: {total}")
check("Gold suma lo mismo que Silver", gold_sum == total)

spark.stop()
