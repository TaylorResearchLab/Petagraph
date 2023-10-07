

# start db and execute constraints from the shell:

#  $ bin/cypher-shell
# gives this error:
# The operation couldn’t be completed. Unable to locate a Java Runtime.
# Please visit http://www.java.com for information on installing Java.
# https://inboundfound.com/neo4j-cli-cypher-shell/

# cd /Users/stearb/Library/Application\ Support/Neo4j\ Desktop/Application/relate-data/dbmss/dbms-90e3a101-4416-4df0-9863-b8e100970fac


#cd import;
: '
large_files=("CUI-CUIs")
small_files=("CODEs" "CUI-CODEs" "CODE-SUIs" "SUIs" "CUIs" "DEFs" "CUI-SUIs" "DEFrel" "CUI-TUIs" "TUIs" "TUIrel")

for file in "${small_files[@]}"; do
	printf -- "\n\n----------------------------";
	printf -- "\nDeduplicating ${file}.csv...\n"; 
	echo "----------------------------";
	sleep 2;
    awk "NR>1 !x[$0]++" ${file}.csv > /dev/null; # suppress output
    printf -- "Done with ${file}.csv\n";
    printf -- '----------------------------\n';
	sleep 2;
done
'


rm -rf data/databases/*
rm -rf data/transactions/*

# bin/neo4j-admin database import full
bin/neo4j-admin import --verbose  --nodes=Semantic="import/TUIs.csv" --nodes=Concept="import/CUIs.csv" --nodes=Code="import/CODEs.csv" --nodes=Term="import/SUIs.csv" --nodes=Definition="import/DEFs.csv"  --relationships=ISA_STY="import/TUIrel.csv" --relationships=STY="import/CUI-TUIs.csv" --relationships="import/CUI-CUIs.csv" --relationships=CODE="import/CUI-CODEs.csv" --relationships="import/CODE-SUIs.csv" --relationships=PREF_TERM="import/CUI-SUIs.csv" --relationships=DEF="import/DEFrel.csv"  --skip-bad-relationships --skip-duplicate-nodes









'''



MATCH (log2_node:Code {SAB:"LOG2FCBINS"}) WITH log2_node ,split(log2_node.CODE,",") as bin 
SET log2_node.lowerbound = toFloat(bin[0]) 
SET  log2_node.upperbound = toFloat(bin[1]);


match (expbins_code:Code {SAB:'EXPBINS'})-[:CODE]-(expbins_cui:Concept)
WITH expbins_code ,split(expbins_code.CODE,'.') as bin 
set expbins_code.lowerbound = toFloat(bin[0]+'.'+bin[1])
set expbins_code.upperbound = toFloat(bin[2]+'.'+bin[3])

MATCH (pval_node:Code {SAB:'PVALUEBINS'}) WITH pval_node, split(pval_node.CODE,'.') AS bin
SET pval_node.lowerbound = toFloat(bin[0]) 
SET  pval_node.upperbound = toFloat(bin[1]);


'''