# Instructions on how to load the Petagraph CSVs into the Neo4j Desktop Browser


### Step 1. Download Neo4j Desktop: https://neo4j.com/download/

### Step 2. Obtain the Petagraph CSVs or create them using the ingest guide [here]()


### Download the build_petagraph.sh script [here](https://github.com/TaylorResearchLab/Petagraph/blob/main/build_process/build/build_petagraph.sh) and place it in the top level of a new database on the Neo4j Desktop App

### Run the following command from the Neo4j Desktop Terminal 
`chmod 777 build_petagraph.sh; ./build_petagraph.sh`

The build time will vary but shouldnt take more than 20 min.


After the database build is finished, open the Browser and execute this block of Cypher:
```
```
