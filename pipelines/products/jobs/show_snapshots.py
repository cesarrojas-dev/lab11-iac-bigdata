"""Resume un metadata.json de Iceberg ya descargado. Solo lee."""
import json
import sys
from datetime import datetime

with open(sys.argv[1], encoding="utf-8") as f:
    meta = json.load(f)

print("location           :", meta["location"])
print("format-version     :", meta["format-version"])
print("current-snapshot-id:", meta["current-snapshot-id"])

schema_id = meta.get("current-schema-id", 0)
schema = next(s for s in meta["schemas"] if s["schema-id"] == schema_id)
print("\nSchema:")
for field in schema["fields"]:
    print(f"  {field['name']:<16} {field['type']}")

print(f"\nSnapshots: {len(meta['snapshots'])}")
for snap in meta["snapshots"]:
    when = datetime.fromtimestamp(snap["timestamp-ms"] / 1000)
    print(f"  id={snap['snapshot-id']}  fecha={when:%Y-%m-%d %H:%M:%S}  "
          f"operacion={snap.get('summary', {}).get('operation')}")
    print(f"    manifest-list={snap['manifest-list']}")
