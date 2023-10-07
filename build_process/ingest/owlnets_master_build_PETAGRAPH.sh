#!/bin/bash

# Date: Sept 2023
# Author: Ben Stear

######################################
#####  PETAGRAPH BUILD SCRIPT   ######
######################################

# To run this code locally you must first download the github repo: https://github.com/x-atlas-consortia/ubkg-etl
# This script must be run from this directory (I can just cd into it below actually): 
# /Users/stearb/Desktop/DESKTOP_TRANSFER/R03_local/Petagraph_Sept2023/code/ubkg-etl-main/generation_framework
# b/c the OWLNETS-UMLS-GRAPH-12.py script appends the helper module paths to $(PWD), which will result in module not
# found error if its appended to a path that isnt this one.




cd /Users/stearb/Desktop/DESKTOP_TRANSFER/R03_local/Petagraph_Sept2023/code/ubkg-etl-main/generation_framework

BASE_CSV_DIR="/Users/stearb/Desktop/DESKTOP_TRANSFER/R03_local/Petagraph_Sept2023/data/base_csvs/basecontext10Sep2023/"
MAPPING_DATA_DIR="/Users/stearb/Desktop/DESKTOP_TRANSFER/R03_local/Petagraph_Sept2023/data/mapping_files"
ADDITIONAL_DATASETS_DIR="/Users/stearb/Desktop/DESKTOP_TRANSFER/R03_local/Petagraph_Sept2023/data/additional_datasets"
NON_MAPPING_DATA_DIR='/Users/stearb/Desktop/DESKTOP_TRANSFER/DataDistilleryFiles'
# ^ For GTEX, LINCS, GLYGEN, AZIMUTH, STRING, and SCHEART

######################################

### Mapping Datasets:
# CLINVAR		NCBI ClinVar	
# CMAP			Connectivity Map	
# HPOMP		    HPO-MP mapping	
# HGNCHPO		human genotype - phenotype mapping	
# HGNCHCOP		human - mouse orthologs	
# HCOPMP		mouse genotype-phenotype mapping
# RATHCOP		ENSEMBL human to ENSEMBL Rat ortholog	
# MSIGDB		Molecular Signatures Database
# HSCLO		    Chromosome Location Ontology
# GENCODEHSCLO GENCODE-HSCLO mappings

### Additional Datasets:
# GTEXEXP
# GTEXEQTL
# GTEXCOEXP
# GLYGEN
# LINCS
# AZIMUTH
# STRING
# SCHEART
# KF
# 4DN

######################################

: '
printf "\n\nIngesting CLINVAR...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/CLINVAR    $BASE_CSV_DIR CLINVAR;

printf '\n\nIngesting CMAP...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/CMAP     $BASE_CSV_DIR CMAP;

printf '\n\nIngesting GENCODEHSCLO...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/GENCODE_HSCLO   $BASE_CSV_DIR GENCODEHSCLO ;

printf '\n\nIngesting HPOMP...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/HPO_MP     $BASE_CSV_DIR HPOMP ;

printf '\n\nIngesting HSCLO...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/HSCLO     $BASE_CSV_DIR HSCLO ;

printf '\n\nIngesting HGNCHPO...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/human_genotype_phenotype   $BASE_CSV_DIR HGNCHPO ;

printf '\n\nIngesting HGNCHCOP...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/human_mouse_orthologs    $BASE_CSV_DIR HGNCHCOP ;

printf '\n\nIngesting RATHCOP...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/human_rat_ensembl_orthologs  $BASE_CSV_DIR RATHCOP ;

printf '\n\nIngesting MSIGDB...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/MSigDB     $BASE_CSV_DIR MSIGDB ;

printf "\n\nIngesting CLINVAR...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/CLINVAR    $BASE_CSV_DIR CLINVAR;

printf '\n\nIngesting HCOPMP...\n\n'; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py   $MAPPING_DATA_DIR/mouse_genotype_phenotype    $BASE_CSV_DIR HCOPMP ;


########################################################
######### ADDITIONAL (NON-MAPPING) DATASETS  ############
########################################################

printf "\n\nIngesting GTEXEQTL...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py  $NON_MAPPING_DATA_DIR/gtex/gtex_eqtl  $BASE_CSV_DIR GTEXEQTL

printf "\n\nIngesting GTEXEXP...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py $NON_MAPPING_DATA_DIR/gtex/gtex_exp   $BASE_CSV_DIR  GTEXEXP

printf "\n\nIngesting KF...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py  $NON_MAPPING_DATA_DIR/KidsFirst/combined_files $BASE_CSV_DIR KF

printf "\n\nIngesting HUBMAP-AZIMUTH...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py  $NON_MAPPING_DATA_DIR/HUBMAP_AZ  $BASE_CSV_DIR HMAZ 

printf "\n\nIngesting SCHEART...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py  $NON_MAPPING_DATA_DIR/scHeart  $BASE_CSV_DIR SCHEART 

printf "\n\nIngesting STRING...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py $ADDITIONAL_DATASETS_DIR/STRING   $BASE_CSV_DIR  STRING

printf "\n\nIngesting GLYGEN (combined)...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py $ADDITIONAL_DATASETS_DIR/GLYGEN   $BASE_CSV_DIR  GLYGEN

printf "\n\nIngesting 4DN...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py $ADDITIONAL_DATASETS_DIR/4DN   $BASE_CSV_DIR  4DN

printf "\n\nIngesting LINCS...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py $ADDITIONAL_DATASETS_DIR/LINCS   $BASE_CSV_DIR  LINCS

printf "\n\nIngesting GLYGEN...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py $ADDITIONAL_DATASETS_DIR/GLYGEN_TAHA_BEN   $BASE_CSV_DIR  GLYGEN
'
#####################################

printf "\n\nIngesting GTEXCOEXP (reduced dataset)...\n\n"; sleep 3;
python3 owlnets_umls_graph/OWLNETS-UMLS-GRAPH-12.py $NON_MAPPING_DATA_DIR/gtex/gtex_coexp_reduced   $BASE_CSV_DIR  GTEXCOEXP

: '
# After the database has been built, execute these Cypher queries:

v5 INDEXING

CREATE CONSTRAINT FOR (n:Semantic) REQUIRE n.TUI IS UNIQUE;
CREATE CONSTRAINT FOR (n:Semantic) REQUIRE n.STN IS UNIQUE;
CREATE CONSTRAINT FOR (n:Semantic) REQUIRE n.DEF IS UNIQUE;
CREATE CONSTRAINT FOR (n:Semantic) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:Concept) REQUIRE n.CUI IS UNIQUE;
CREATE CONSTRAINT FOR (n:Code) REQUIRE n.CodeID IS UNIQUE;
CREATE INDEX FOR (n:Code) ON (n.SAB);
CREATE INDEX FOR (n:Code) ON (n.CODE);
CREATE CONSTRAINT FOR (n:Term) REQUIRE n.SUI IS UNIQUE;
CREATE INDEX FOR (n:Term) ON (n.name);
CREATE INDEX FOR (n:Definition) ON (n.SAB);
CREATE INDEX FOR (n:Definition) ON (n.DEF);
CREATE CONSTRAINT FOR (n:NDC) REQUIRE n.ATUI IS UNIQUE;
CREATE CONSTRAINT FOR (n:NDC) REQUIRE n.NDC IS UNIQUE;
CREATE FULLTEXT INDEX Term_name FOR (n:Term) ON EACH [n.name];



v4 INDEXING
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


MATCH (pval_node:Code {SAB:"PVALUEBINS"})
WITH pval_node, split(pval_node.CODE,".") AS bin
SET pval_node.lowerbound = toFloat(bin[0])
SET pval_node.upperbound = toFloat(bin[1]);

MATCH (expbins_code:Code {SAB:"EXPBINS"})-[:CODE]-(expbins_cui:Concept)
WITH expbins_code ,split(expbins_code.CODE,".") as bin
SET expbins_code.lowerbound = toFloat(bin[0]+"."+bin[1])
SET expbins_code.upperbound = toFloat(bin[2]+"."+bin[3]);

MATCH (log2_node:Code {SAB:"LOG2FCBINS"})
WITH log2_node ,split(log2_node.CODE,",") as bin
SET log2_node.lowerbound = toFloat(bin[0])
SET log2_node.upperbound = toFloat(bin[1]);


'






