from pathling import PathlingContext
from pathling import Expression as exp
from pathlib import Path
import json


def convert_to_bundles_for_import(input_dir, output_dir):

    file_counter = 0
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for ndjson_file in input_dir.glob("*.ndjson"):
        with ndjson_file.open("r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    output_file = output_dir / f"{ndjson_file.stem}_{line_number:05}.json"
                    with output_file.open("w", encoding="utf-8") as out_f:
                        json.dump(data, out_f, indent=2)
                    file_counter += 1
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON in {ndjson_file.name} line {line_number}: {e}")


def read_in_and_convert_to_parquet(bundles_dir, parquet_output_dir):
    pc = PathlingContext.create(
        enable_extensions=True,
        enable_delta=True,
        enable_terminology=False,
        terminology_server_url="http://localhost/not-a-real-server",
    )

    bundles_pl = pc.read.bundles(bundles_dir, ['Observation', 'Patient', 'Condition'])

    bundles_pl.write.parquet(parquet_output_dir, "overwrite")

    result = bundles_pl.extract(
            "Condition",
            columns=[
                exp("id", "dia_id"),
                exp("code.coding.code", "diag_code"),
                exp("recordedDate", "recorded_date"),
                exp("subject.reference", "patient")
            ],
        )

    result.show(truncate=False)

    return bundles_pl


def read_in_and_convert_to_table(bundles_dir, table_output_dir):
    pc = PathlingContext.create(
        enable_extensions=True,
        enable_delta=True,
        enable_terminology=False,
        terminology_server_url="http://localhost/not-a-real-server",
    )

    bundles_pl = pc.read.bundles(bundles_dir, ['Observation', 'Patient', 'Condition'])
    bundles_pl.write.tables(table_output_dir)


torch_extraction_id = "6997ff12-8d91-4cb2-be4c-24d97ccc18a3"
input_dir = f'/torch/output/{torch_extraction_id}'
bundles_dir = "./torch/bundles"
parquet_output_dir = f'/output/parquet/{torch_extraction_id}'
tables_output_dir = f'/output/tables/{torch_extraction_id}'

convert_to_bundles_for_import(input_dir, bundles_dir)
read_in_and_convert_to_parquet(bundles_dir, parquet_output_dir)


dir_path = Path(bundles_dir)
for file in dir_path.iterdir():
    if file.is_file():
        file.unlink()

#read_in_and_convert_to_table(bundles_dir, tables_output_dir)
