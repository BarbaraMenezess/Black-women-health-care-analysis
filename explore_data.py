
import basedosdados as bd

TABLE_ID = "microdados"

print("Looking up columns for SIM microdata...", flush=True)

try:
    result = bd.get_columns(table_id=TABLE_ID, page_size=100)
    print(result)
except Exception as error:
    print("ERROR:", repr(error), flush=True)



