# Petagraph 
A repository for the Petagraph project

The bioarxiv preprint can be found at https://www.biorxiv.org/content/biorxiv/early/2023/02/13/2023.02.11.528088.full.pdf

.

.

.

# Petagraph build instructions

**There are 2 entry points for recreating Petagraph:**

DATASET INGESTION (entry point 1) 

You can start with the Unified Biomedical Knowledge Graph (UBKG) CSVs and run the scripts to process and append the 20 new datasets to create the final, processed Petagraph CSVs, and then complete the database build step below or,

DATABASE BUILD (entry point 2) 

You can start with the final, processed Petagraph CSVs and simply build the database using the Neoj Desktop Application.

If you wish to start from entry point 1 you will need
- Neo4j Desktop Application, `python3`, `git`
  
If you wish to start from entry point 2 you will need
- Neo4j Desktop Application

### Instrustions starting from entry point 1
##### Step 1. Obtain the UBKG CSV files and the 20 sets of node and edge files representing the 20 additional datasets make up Petagraph.

##### Step 2. Run the OWLNETS-UMLS-GRAPH-12.py script

