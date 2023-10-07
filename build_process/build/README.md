# Instructions on how to load the Petagraph CSVs into the Neo4j Desktop Browser


### Step 1. Download Neo4j Desktop: https://neo4j.com/download/

### Step 2. Obtain the Petagraph CSVs or create them using the ingest guide [here]()


### Download the build_petagraph.sh script [here](https://github.com/TaylorResearchLab/Petagraph/blob/main/build_process/build/build_petagraph.sh) and place it in the top level of a new database on the Neo4j Desktop App

### Run the following command from the Neo4j Desktop Terminal 
`chmod 777 build_petagraph.sh; ./build_petagraph.sh`

The build time will vary but shouldnt take more than 20 min.


After the database build is finished, open the Browser and execute this block of Cypher:
```
MATCH (log2_node:Code {SAB:"LOG2FCBINS"}) WITH log2_node ,split(log2_node.CODE,",") as bin 
SET log2_node.lowerbound = toFloat(bin[0]) 
SET  log2_node.upperbound = toFloat(bin[1]);

MATCH (expbins_code:Code {SAB:'EXPBINS'})-[:CODE]-(expbins_cui:Concept)
WITH expbins_code ,split(expbins_code.CODE,'.') as bin 
set expbins_code.lowerbound = toFloat(bin[0]+'.'+bin[1])
set expbins_code.upperbound = toFloat(bin[2]+'.'+bin[3]);

MATCH (pval_node:Code {SAB:'PVALUEBINS'}) WITH pval_node, split(pval_node.CODE,'.') AS bin
SET pval_node.lowerbound = toFloat(bin[0]) 
SET  pval_node.upperbound = toFloat(bin[1]);
```
