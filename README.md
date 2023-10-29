![example workflow](https://github.com/TaylorResearchLab/Petagraph/actions/workflows/petagraph_qc_tests.yml/badge.svg)
# Petagraph 

Over the past decade, there has been substantial growth in both the quantity and complexity of available biomedical data. In order to harness this extensive data and alleviate the challenges associated with data integration, we developed Petagraph, a biomedical knowledge graph that encompasses over 30 million nodes and 160 million relationships. Petagraph provides a cohesive data environment that enables users to efficiently analyze, annotate, and discern relationships within and across complex multi-omics and other types of biomedical datasets. Constructed with the Unified Biomedical Knowledge Graph (UBKG), Petagraph leverages more than 180 ontologies and standards that support a diversity of genomics data types. We have curated and embedded millions of quantitative genomics data within Petagraph’s ontological scaffold and demonstrate  how  queries on Petagraph can generate meaningful results across various research contexts and use cases.

The bioarxiv preprint can be found at https://www.biorxiv.org/content/biorxiv/early/2023/02/13/2023.02.11.528088.full.pdf

## Installing Petagraph
This installation process was tested on an Apple MacBook Pro 2023 16GB Memory running Ventura macOS 13.6. Software Versions used for testing: `Neo4j Desktop 1.5.7`, `Neo4j 4.3.23`, `Python3.x`, `git 2.39.3`.

### Petagraph is built on top of the Unified Medical Language System ([UMLS](https://www.nlm.nih.gov/research/umls/index.html)) Unified Medical Knowledge Graph ([UBKG](https://github.com/x-atlas-consortia/ubkg-etl)) so the first step is to generate the UMLS and UBKG CSVs:

Instructions to generate UMLS CSVs: [Build-UMLS](https://github.com/x-atlas-consortia/ubkg-etl/tree/main/source_framework) 

Instructions to generate UBKG CSVs: [Build-UBKG](https://github.com/x-atlas-consortia/ubkg-etl/tree/main/generation_framework)

#### 1. Download software: 
- Download and install `Neo4j Desktop` (https://neo4j.com/download/), `Python3` and `git`.
#### 2. Download data:
   - Download the Datasets.zip file (250 MB zipped and 2.7GB unzipped) containing the 20 sets of node and edge files from our OSF project site, https://osf.io/6jtc9/. These nodes and edges files represent the 20 additional datasets we've added to the UBKG.

     <img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/main_readme_figures/Screenshot%202023-10-26%20at%209.12.07%20AM.png" alt="drawing" width="500"/>

#### 3. Download and run the `ingest_petagraph.sh` script to ingest the 20 datasets.
The `ingest_petagraph.sh` script is located [here](https://github.com/TaylorResearchLab/Petagraph/blob/main/build_scripts/ingest_petagraph.sh).
You will need to change 2 directory paths within the `ingest_petagraph.sh` script, one to the location of the UBKG CSVs and the other to the location of the nodes and edges files of the 20 datasets. This script should take a little over an hour to run. Once the `ingest_petagraph.sh` script is done running, the UBKG CSVs are now called the Petagraph CSVs, as the 20 additional datasets have been processed and appended.
 
#### 4. Create a new, empty database in Neo4j Desktop and move the CSVs you've just produced. into the import directory of your new database. 
To create a new database, click the Add menu in the upper right hand corner of the Neo4j Desktop Application home screen and select local DBMS. Once the new database has been created, click the 3 little dots to the right of the new database name to bring up the drop down menu, select folders -> import, and place the Petagraph CSVs in the import folder.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/main_readme_figures/create_new_dbms.png" alt="drawing" width="500"/>

Then open up the database drop down menu again and open up the Neo4j terminal to run the code in step 5.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/main_readme_figures/import_folder.png" alt="drawing" width="500"/>

#### 5. Run the following commands from the Neo4j Desktop Terminal in the top level directory of the new database you've just created. 
```bash
$ rm -rf data/databases/*;
$ rm -rf data/transactions/*;
$ bin/neo4j-admin import --verbose  --nodes=Semantic="import/TUIs.csv" --nodes=Concept="import/CUIs.csv" --nodes=Code="import/CODEs.csv" --nodes=Term="import/SUIs.csv" --nodes=Definition="import/DEFs.csv"  --relationships=ISA_STY="import/TUIrel.csv" --relationships=STY="import/CUI-TUIs.csv" --relationships="import/CUI-CUIs.csv" --relationships=CODE="import/CUI-CODEs.csv" --relationships="import/CODE-SUIs.csv" --relationships=PREF_TERM="import/CUI-SUIs.csv" --relationships=DEF="import/DEFrel.csv"  --skip-bad-relationships --skip-duplicate-nodes
```
The build time will vary but shouldnt take more than 20 min.

### Step 6. After the database build is finished, start the database, open the Browser and execute this block of Cypher:
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




