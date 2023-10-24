# Petagraph 
A repository for the Petagraph project

The bioarxiv preprint can be found at https://www.biorxiv.org/content/biorxiv/early/2023/02/13/2023.02.11.528088.full.pdf

## Put summary, and important links here.

## Petagraph build instructions

#### Petagraph is built on top of the Unified Medical Knowledge Graph (UBKG) so the first step is to generate the UBKG CSVs. Please follow instructions here:

Generate UMLS CSVs: [Build-UMLS](https://github.com/x-atlas-consortia/ubkg-etl/tree/main/source_framework)
Generate UBKG CSVs: [Build-UBKG](https://github.com/x-atlas-consortia/ubkg-etl/tree/main/generation_framework)

# Next
#### Step 1. Download Neo4j Desktop (https://neo4j.com/download/) , Python3 and git.
#### Step 2. Obtain the 20 sets of node and edge files (that represent the 20 additional datasets that differentiate Petagraph from UBKG.
#### Step 3. Run the `ingest_petagraph.sh` script to ingest the 20 datasets.
You will need to change 2 directory paths, one to the location of the UBKG CSVs andd the other to the location of the nodes and edges files of the 20 datasets. This script should take a little over an hour to run. Once the `ingest_petagraph.py` script is done running, the UBKG CSVs are now called the Petagraph CSVs, as the 20 additional datasets have been processed and appended. Now you can build the database...
 

This build process uses Neo4j's bulk import tool to load Petagraph's CSVs into the graph.

#### Step 1. Download Neo4j Desktop (https://neo4j.com/download/) if you haven't already done so, and create a new, empty database.
#### Step 2. CSVs you've just produced. Place the Petagraph CSVs in the import directory of your new database.


#### Step 4. Run the following commands from the Neo4j Desktop Terminal in the top level directory of the new database you've just created. 
```
rm -rf data/databases/*
rm -rf data/transactions/*
bin/neo4j-admin import --verbose  --nodes=Semantic="import/TUIs.csv" --nodes=Concept="import/CUIs.csv" --nodes=Code="import/CODEs.csv" --nodes=Term="import/SUIs.csv" --nodes=Definition="import/DEFs.csv"  --relationships=ISA_STY="import/TUIrel.csv" --relationships=STY="import/CUI-TUIs.csv" --relationships="import/CUI-CUIs.csv" --relationships=CODE="import/CUI-CODEs.csv" --relationships="import/CODE-SUIs.csv" --relationships=PREF_TERM="import/CUI-SUIs.csv" --relationships=DEF="import/DEFrel.csv"  --skip-bad-relationships --skip-duplicate-nodes
```

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




