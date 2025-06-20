from pathling import PathlingContext
from pathling import Expression as exp
from pathlib import Path
import json


pc = PathlingContext.create(
        enable_extensions=True,
        enable_delta=True,
        enable_terminology=False,
        terminology_server_url="http://localhost/not-a-real-server",
    )


torch_extraction_id = "6997ff12-8d91-4cb2-be4c-24d97ccc18a3"
parquet_input_dir = f'/output/parquet/{torch_extraction_id}'
#res_type = "Condition"


pc.read.parquet

fhir_data = pc.read.parquet(f"{parquet_input_dir}")

result = fhir_data.extract(
            "Condition",
            columns=[
                exp("id", "dia_id"),
                exp("code.coding.code", "diag_code"),
                exp("recordedDate", "recorded_date"),
                exp("subject.reference", "patient")
            ],
        )

result.show(truncate=False)
