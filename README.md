# dse-example


## Run

1. Start the fhir server and torch in the respective folders using `docker compose -p dse-example up -d`
2. Upload testdata to your fhir server `bash upload-testdata.sh`
3. Access your fhir server to verify your testdata upload using your browser `http://localhost:8081/fhir/Condition | jq .`
4. Enter the torch container and set correct file access rights `docker exec -it --user=root dse-example-torch-1 bash` and in the container set output to 1001 `chown -R 1001:1001 output`
4. Execute an example torch CRTDL: 
```
cd torch
bash execute-crtdl.sh -f queries/example-crtdl.json
```
5. See your extraction being passed to the output folder output/<your-job-id>
6. Start up the parquet converter `docker compose -p dse-example up -d` in the `parquet-converter` folder
7. Ssh into the container `docker exec -it dse-example-parquet-converter-1 bash`
8. execute the conversion to parquet from torch `cd /src` and `python3 test-parquet-conversion.py`
