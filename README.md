# dse-example


## Run Extraction

1. Start the fhir server and torch in the respective folders using `docker compose -p dse-example up -d`
2. Upload testdata to your fhir server `bash upload-testdata.sh`
3. Access your fhir server to verify your testdata upload using your browser `http://localhost:8088/fhir/Condition | jq .`
4. Enter the torch container and set correct file access rights `docker exec -it --user=root dse-example-torch-1 bash` and in the container set output to 1001 `chown -R 1001:1001 output`
4. Execute an example torch CRTDL: 
```
cd torch
bash execute-crtdl.sh -f queries/example-crtdl.json
```
5. See your extraction being passed to the output folder output/<your-job-id>

## Convert Extraction to parquet

Rquires an extraction to have been executed already

1. Start up the export converter `docker compose -p dse-example up -d` in the `export-converter` folder
2. Ssh into the container `docker exec -it dse-example-export-converter-1 bash`
3. In the `test-export-conversion.py` change the `torch_extraction_id` in line `69` to your extraction id.
4. Execute the conversion to export from torch `cd /src` and `python3 test-parquet-conversion.py` and `python3 test-csv-conversion.py`


## Run DIMP (De-Identification, Minimization, Pseudonymization)

Rquires an extraction to have been executed already

1. Start the pseudonymization service (vfps) `docker compose -p dse-example up -d` and the DIMP service (fhir-pseudonymizer) `docker compose -p dse-example up -d` in the respectice folders
2. Create a `patient-identifiers` namespace in vfps:

```bash
curl --request POST \
  --url http://localhost:8080/v1/namespaces \
  --header 'content-type: application/json' \
  --data '{
  "name": "patient-identifiers",
  "pseudonymGenerationMethod": "PSEUDONYM_GENERATION_METHOD_UNSPECIFIED",
  "pseudonymLength": 32,
  "pseudonymPrefix": "string",
  "pseudonymSuffix": "string",
  "description": "string"
}'
```

3. Execute the dimp bash script under `dimp/dimp.sh -e {your-export-id-here}`
4. view your extraction files under `dimp/extraction-transfer/{your-export-id-here}` 
4.1 original files with filenames `{uuid}.ndjson` dimped files with filenames `dimped_{uuid}.ndjson`



