rm -rf data/databases/*
rm -rf data/transactions/*

# Replace "bin/neo4j-admin import" with "bin/neo4j-admin database import full" 
# if you are running Neo4j 5.x

bin/neo4j-admin import --verbose  --nodes=Semantic="import/TUIs.csv" --nodes=Concept="import/CUIs.csv" --nodes=Code="import/CODEs.csv" --nodes=Term="import/SUIs.csv" --nodes=Definition="import/DEFs.csv"  --relationships=ISA_STY="import/TUIrel.csv" --relationships=STY="import/CUI-TUIs.csv" --relationships="import/CUI-CUIs.csv" --relationships=CODE="import/CUI-CODEs.csv" --relationships="import/CODE-SUIs.csv" --relationships=PREF_TERM="import/CUI-SUIs.csv" --relationships=DEF="import/DEFrel.csv"  --skip-bad-relationships --skip-duplicate-nodes


'''
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
'''
