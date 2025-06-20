# dse-example


## Run

1. Start the fhir server and torch in the respective folders using `docker compose -p dse-example up -d`
2. Download some mii example data using `bash get-mii-testdata.sh`
3. Upload testdata to your fhir server `bash upload-testdata.sh`
4. Access your fhir server to verify your testdata upload using your browser `http://localhost:8081/Condition`
5. Execute an example torch CRTDL: 
```
cd torch
bash execute-crtdl.sh -f queries/example-crtdl.json
```
6. See your extraction being passed to the output folder output/<your-job-id>
7. Start up the parquet converter `docker compose -p dse-example up -d` in the `parquet-converter` folder
8. Ssh into the container `docker exec -it parquet-converter-parquet-converter-1 bash``
9. execute the conversion to parquet from torch `cd /src` and `python3 test-parquet-conversion.py`
