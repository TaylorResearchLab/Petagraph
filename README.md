# Petagraph 
A repository for the Petagraph project

The bioarxiv preprint can be found at https://www.biorxiv.org/content/biorxiv/early/2023/02/13/2023.02.11.528088.full.pdf

## Petagraph build instructions

**There are 2 entry points for recreating Petagraph:**

**DATASET INGESTION** (entry point 1):

Start with the Unified Biomedical Knowledge Graph (UBKG) CSVs and run the scripts to process and append the 20 new datasets to create the final, processed Petagraph CSVs, and then complete the database build step below or,

**DATABASE BUILD** (entry point 2):

Start with the final, processed Petagraph CSVs and simply build the database using the Neoj Desktop Application.

If you wish to start from entry point 1 you will need Neo4j Desktop Application, Python3 and Git.

If you wish to start from entry point 2 you will need Neo4j Desktop Application.

### Instrustions for **DATASET INGESTION** (entry point 1)
#### Step 1. Download Neo4j Desktop (https://neo4j.com/download/) , Python3 and git.
#### Step 2. Obtain the UBKG CSV files and the 20 sets of node and edge files representing the 20 additional datasets make up Petagraph.
#### Step 3. Run the `ingest_petagraph.sh` script to ingest the 20 datasets.
You will need to change 2 directory paths, one to the location of the UBKG CSVs andd the other to the location of the nodes and edges files of the 20 datasets. This script should take a little over an hour to run. Once the `ingest_petagraph.py` script is done running, the UBKG CSVs are now called the Petagraph CSVs, as the 20 additional datasets have been processed and appended. Now you can build the database...

### Instructions for **DATABASE BUILD** (entry point 2)

This build process uses Neo4j's bulk import tool to load Petagraph's CSVs into the graph.

#### Step 1. Download Neo4j Desktop (https://neo4j.com/download/) if you havent already done so, and create a new, empty database.

#### Step 2. If you skipped the ingestion step you'll need to obtain the Petagraph CSVs, otherwise you can use the CSVs you've just produced. Place the Petagraph CSVs in the import directory of your new database.

#### Step 3.Download the build_petagraph.sh script [here](https://github.com/TaylorResearchLab/Petagraph/blob/main/build_process/build/build_petagraph.sh) and place it in the top level directory of a new database on the Neo4j Desktop App

#### Step 4. Run the following commands from the Neo4j Desktop Terminal of the new database you've just created.
`chmod 777 build_petagraph.sh; ./build_petagraph.sh`

The build time will vary but shouldnt take more than 20 min.

### Step 5. After the database build is finished, start the database, open the Browser and execute this block of Cypher:
This sets contraints and indices on Node types to speed up query execution time. The last three queries create properties on numerical Code nodes.

```cypher
MATCH (n:Term) WHERE size((n)--())=0 DELETE (n);
CREATE CONSTRAINT ON (n:Semantic) ASSERT n.TUI IS UNIQUE;
CREATE CONSTRAINT ON (n:Semantic) ASSERT n.STN IS UNIQUE;
CREATE CONSTRAINT ON (n:Semantic) ASSERT n.DEF IS UNIQUE;
CREATE CONSTRAINT ON (n:Semantic) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT ON (n:Concept) ASSERT n.CUI IS UNIQUE;
CREATE CONSTRAINT ON (n:Code) ASSERT n.CodeID IS UNIQUE;
CREATE INDEX FOR (n:Code) ON (n.SAB);
CREATE INDEX FOR (n:Code) ON (n.CODE);
CREATE CONSTRAINT ON (n:Term) ASSERT n.SUI IS UNIQUE;
CREATE INDEX FOR (n:Term) ON (n.name);
CREATE INDEX FOR (n:Definition) ON (n.SAB);
CREATE INDEX FOR (n:Definition) ON (n.DEF);
CREATE CONSTRAINT ON (n:NDC) ASSERT n.ATUI IS UNIQUE;
CREATE CONSTRAINT ON (n:NDC) ASSERT n.NDC IS UNIQUE;
CALL db.index.fulltext.createNodeIndex("Term_name",["Term"],["name"]);

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

# Step 6. Optionally go through the tutorial to learn how to query Petagraph!




