## Cypher queries to produce graph figures for "Petagraph: A large-scale unifying knowledge graph framework for integrating biomolecular and biomedical data"
#### Python and R Code to produce non-cypher Figures can be found [here](https://github.com/TaylorResearchLab/Petagraph/tree/main/scripts/code)

##### Figure 1. Example of the Concept-Code-Term schema
```
MATCH (c:Concept)-[:CODE]-(s:Code {CODE:'HGNC:11998'})-[r]-(t:Term)
RETURN * 
```

##### Figure 2. Petagraph Data Ingestion Workflow. 
- Figure 2 was made using an online workflow tool called [Canva](https://www.canva.com)

##### Figure 3. 
Dataset interconnectedness jupyter notebook?
[here](https://github.com/TaylorResearchLab/Petagraph/tree/main/scripts/code)

##### Figure 4.
Tahas mean deviation plot
[here](https://github.com/TaylorResearchLab/Petagraph/tree/main/scripts/code)

##### Figure 5.
Tahas heatmaps
[here](https://github.com/TaylorResearchLab/Petagraph/tree/main/scripts/code)

##### Figure 6.
Tahas shortest path -- cypher and code

##### Figure 7.
Recursive ASD query 
```
WITH '0010403' AS parent
MATCH (P_code:Code {SAB:'MP',CODE:parent})<-[:CODE]-(P_concept:Concept)<-[:isa *1.. {SAB:'MP'}]-(C_concept:Concept)
WITH collect(C_concept.CUI) + P_concept.CUI AS terms UNWIND terms AS uterms 
WITH collect(DISTINCT uterms) AS phenos
MATCH (mp_concept:Concept)-[:`RO:0002331`]-(hcop_concept:Concept)-[:RO_HOM0000020]-(hgnc_concept:Concept)-[:CODE]->(human_gene:Code {SAB:'HGNC'})
WHERE mp_concept.CUI IN phenos WITH hgnc_concept, human_gene
MATCH (gene_symbol:Term)-[:PREF_TERM]-(hgnc_concept)-[:RO_0001025]-(gtex_concept:Concept)-[:RO_0001025]-(uberon_concept:Concept)-[:CODE]-(uberon_code:Code {SAB:'UBERON'})
WHERE uberon_code.CODE IN ['0006566','0006631'] WITH *
MATCH (gtex_code:Code {SAB:'GTEX_EQTL'})-[:CODE]-(gtex_concept)-[:p_value]-(pval_concept:Concept)-[:CODE]-(pval_code:Code) WHERE pval_code.upperbound  <  0.05
WITH distinct split(gtex_code.CODE,'-') AS data
RETURN data[0] AS SNP, data[1]+' '+data[2]+' '+data[3] AS tissue, data[-1] AS gene
```

##### Figure 8. -- cypher and python
Expression levels for the human glycosyltransferase gene family. 
```
MATCH (glyco_concept:Concept)<-[:is_glycotransferase]-(hgnc_concept:Concept)-[:CODE]-(human_gene:Code {SAB:'HGNC'})-[:PT]->(gene_symbol:Term)
MATCH (gtex_code:Code {SAB:'GTEX_EXP'})-[:CODE]-(gtex_cui:Concept)-[:`RO:0002206`]-(hgnc_concept)
MATCH (exp_code:Code)-[:CODE]-(exp_cui:Concept)-[:has_expression]-(gtex_cui)-[:`RO:0002206`]-(ub_cui:Concept)-[:CODE]-(ub_code:Code {SAB:'UBERON'})-[:PT]-(ub_term:Term)
RETURN DISTINCT split(gene_symbol.name, ' gene')[0] AS symbol,human_gene.CODE AS hgnc_id, ub_term.name AS tissue, ub_code.CODE AS uberon_CODE, exp_code.CODE AS tpm
```

##### Figure 9: Query results on heart-defect phenotype-associated glycosylation targets.
Query results on heart-defect phenotype-associated glycosylation targets.
Taha - cypher and code

##### Figure 10.
Single cell developmental heart use case
```
MATCH (p:Code {CODE:'0010403'})<-[:CODE]-(m:Concept)<-[:isa *1..{SAB:'MP'}]-(n:Concept)-[: `RO:0002331`]-(o:Concept)-[:RO_HOM0000020]->(q:Concept)-[:CODE]->(l:Code {SAB:'HGNC'}), (t:Term)-[:PREF_TERM]-(q)-[:`RO:0002206`]-(c:Concept)-[:log2FC]-(rs:Concept)-[:CODE]-(s:Code {SAB:'LOG2FC_BINS'}), (c)-[:CODE]-(r:Code)
return * limit 1
```


##### Figure 11.
Figure 11: Querying possible drug-tissue interactions for rofecoxib using CMAP, LINCS L1000 and GTEX_EXP datasets. 
taha cypher and code
