# User Guide for Petagraph

## Guide for exploring Petagraph using Cypher
---------
* This guide is meant to be an introduction for how to write Cypher queries to explore Petagraph. A basic understanding of Cypher is assumed. If you are unfamiliar with Cypher please refer to the [Neo4j docs](https://neo4j.com/developer/cypher/). 
--------
## Introduction

### The simplest way to find a Code in the graph is to search for it using it's source abbreviation (SAB).

#### 1. How can I return a Code node from a specific ontology/dataset, for example an HGNC Code?
Specify the `HGNC` as the SAB property:
```cypher
MATCH (hgnc_code:Code {SAB:'HGNC'})
RETURN * 
LIMIT 1
```

You can also specify properties outside the Node syntax using the `WITH` keyword,
```cypher
WITH 'HGNC' AS HGNC_SAB
MATCH (hgnc_code:Code {SAB:HGNC_SAB})
RETURN * 
LIMIT 1
```
or using the `WHERE` keyword:

```cypher
MATCH (hgnc_code:Code) WHERE hgnc_code.SAB = 'HGNC'
RETURN * 
LIMIT 1
```

...or filter to include multiple SABs:
```cypher
MATCH (code:Code) WHERE code.SAB CONTAINS 'GTEX'
RETURN DISTINCT code.SAB
```

(the query above should return `GTEXEXP` and `GTEXEQTL`).

#### 2. How can I return a Code node and its Concept node from a specific ontology/dataset, for example an HGNC Code node and its Concept node?
Every Code node is connected to a Concept node by a 'CODE' relationship:
```cypher
MATCH (hgnc_code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)
RETURN * 
LIMIT 1
```

#### 3. To return the human-readable string that a Code represents you can return the Term node along with the Code. 
Note: Not all Code nodes have Terms attached to them. If a Code does have Term nodes then it will almost always have a 'preferred term'. This 'preferred term' is always attached to it's Code by the 'PT' relationship:

```cypher
MATCH (hgnc_code:Code {SAB:'HGNC'})-[:PT]-(term:Term)
RETURN * 
LIMIT 1
```

You can also directly access the 'preferred term' through the corresponding Concept node through a 'PREF_TERM' relationship:
```cypher
MATCH (hgnc_code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[:PREF_TERM]-(term:Term)
RETURN * 
LIMIT 1
```

#### 4. Ontologies/datasets are connected to one another through Concept-Concept relationships, so you must query the concept space to find these relationships.
Return an `HGNC` to `GO` path (code)-(concept)-(concept)-(code):
```cypher
MATCH (code1:Code {SAB:'HGNC'})-[:CODE]-(concept1:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code {SAB:'GO'})
RETURN * 
LIMIT 1
```

#### 5. Another way to query relationships between 2 ontologies/datasets without necessarily including the Code nodes (and specifying SABs) on either end of the query is to know the SAB of the relationship and/or TYPE of relationship. It's important to realize that while every Code has an SAB that identifies what ontology/dataset it belongs to, relationships in the graph also have SABs.

In this example, the 'type' of relationship is `process_involves_gene` and the SAB is `NCI`:
```cypher
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r:process_involves_gene {SAB:'NCI'}]-(concept2:Concept)-[:CODE]-(code2:Code {SAB:'GO'})
RETURN * 
LIMIT 1
```

It can be helpful to return the 'type' and 'SAB' of the relationship between Concepts of interest. You can easily do this by returning them in a table. For example, if you want to find all the unique relationship 'types' and 'SABs' between the `HGNC` and `GO` datasets you can write something like this:

```cypher
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code {SAB:'GO'})
RETURN DISTINCT code.SAB, type(r), r.SAB, code2.SAB
```

#### 6. How can I find out what relationships exist between my ontology/dataset and other ontologies/datasets?
If you simply want to find the relationship 'types' and 'SABs' between a dataset of interest (for example `HGNC`) and all other datasets you can write something like this: 
```cypher
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code)
RETURN DISTINCT code.SAB AS hgnc_start_code, type(r) AS edge_TYPE, r.SAB AS edge_SAB,  code2.SAB AS SAB_end_code
LIMIT 10
```

we can also go a step further and return the Terms on either end of this query:

```cypher
MATCH (hgnc_term:Term)-[:PT]-(code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code)-[:PT]-(term2:Term)
RETURN DISTINCT hgnc_term.name AS gene_name, code.SAB AS hgnc_start_code, type(r) AS edge_TYPE, r.SAB AS edge_SAB,  code2.SAB AS SAB_end_code, term2.name AS end_term
LIMIT 10
```


## Example Use Cases

### <ins>GlyGen, KF and GTEx</ins>

Birth defects could be caused by dysregulation of glycosylation (PMC6331365). Certain heart defects have been shown to be associated with loss of glycosylation (e.g. heterotaxy, PMC3869867). KF heart defect cohort (711 subjects) may have evidence of genetic variants affecting glycosylation genes. A question could be, which KF deleterious variants could lead to loss of glycosylation by affecting glycoenzymes and glycoenzyme expression, specifically for those genes found in the GTEx heart dataset ?

Query Description: Intersection of `GLYGEN`, `KF` and `GTEX`. The query retrieves Glycoreactions {SAB:”GLYCOSYLTRANSFERASE.REACTION”} and subsequently Glycoenzymes data from GLYCANS dataset. Associated genes, their expression and variant count are obtained from `GTEXEXP` and `KF` datatsets respectively. 

```cypher
WITH "Myocardium of left ventricle" AS tissue_name
MATCH (glycoreaction_code:Code)<-[:CODE]-(glycoreaction_concept:Concept)-[r1:has_enzyme_protein {SAB:"GLYCANS"}]->(glycoenzyme_concept:Concept)-[r2:gene_product_of]->(gene_concept:Concept)-[r3]-(bin_concept:Concept)-[:CODE]->(bin_code:Code {SAB:"KFGENEBIN"}),(tissue_concept:Concept)-[r4:expresses {SAB:"GTEXEXP"}]->(gtexexp_concept:Concept)-[r5 {SAB:"GTEXEXP"}]->(gene_concept:Concept),(gtexexp_concept:Concept)-[r6:has_expression {SAB:"GTEXEXP"}]->(exp_concept:Concept)-[:CODE]-(exp_code:Code),
(gene_concept:Concept)-[:PREF_TERM]->(gene:Term),
(glycoenzyme_concept:Concept)-[:PREF_TERM]->(glycoenzyme:Term),
(tissue_concept:Concept)-[:PREF_TERM]-(tissue:Term {name:tissue_name})
RETURN * LIMIT 1
```

The following query will return a table version of the previous query:
```cypher
WITH "Myocardium of left ventricle" AS tissue_name
MATCH (glycoreaction_code:Code)<-[:CODE]-(glycoreaction_concept:Concept)-[r1:has_enzyme_protein {SAB:"GLYCANS"}]->(glycoenzyme_concept:Concept)-[r2:gene_product_of]->(gene_concept:Concept)-[r3]-(bin_concept:Concept)-[:CODE]->(bin_code:Code {SAB:"KFGENEBIN"}),(tissue_concept:Concept)-[r4:expresses {SAB:"GTEXEXP"}]->(gtexexp_concept:Concept)-[r5 {SAB:"GTEXEXP"}]->(gene_concept:Concept),(gtexexp_concept:Concept)-[r6:has_expression {SAB:"GTEXEXP"}]->(exp_concept:Concept)-[:CODE]-(exp_code:Code),
(gene_concept:Concept)-[:PREF_TERM]->(gene:Term),
(glycoenzyme_concept:Concept)-[:PREF_TERM]->(glycoenzyme:Term),
(tissue_concept:Concept)-[:PREF_TERM]-(tissue:Term {name:tissue_name})
RETURN DISTINCT gene.name,tissue.name,glycoenzyme.name,bin_code.value AS variant_count,exp_code.CODE AS liver_expression
```

# Example Cypher Queries 

### <ins>Genotype Tissue Expression (GTEx)</ins>

This query shows the `GTEXEXP` node and its three edges as linked to an `HGNC` node, an `UBERON` node and an `EXPBINS` node. The `EXPBINS` node contains the median TPM value from `GTEX` (the upperbound and lowerbound properties).
```cypher
MATCH (gtex_cui:Concept)-[r0:CODE]-(gtex_exp_code:Code {SAB:'GTEXEXP'}) 
MATCH (gtex_cui)-[r1:expressed_in]-(hgnc_concept:Concept)-[r2:CODE]-(hgnc_code:Code {SAB:'HGNC'})
MATCH (gtex_cui)-[r3:expressed_in]-(ub_concept:Concept)-[r4:CODE]-(ub_code:Code {SAB:'UBERON'})
MATCH (gtex_cui)-[r5:has_expression]-(expbin_concept:Concept)-[r6:CODE]-(expbin_code:Code {SAB:'EXPBINS'})
RETURN * LIMIT 1
```

This query shows the `GTEXEQTL` node and its three edges as linked to an `HGNC` node, an `UBERON` node and a `PVALUEBINS` node. The `PVALUEBINS` node contains the p-value for the eQTL (the upperbound and lowerbound properties).
```cypher
MATCH (gtex_cui:Concept)-[r0:CODE]-(gtex_exp_code:Code {SAB:'GTEXEQTL'}) 
MATCH (gtex_cui)-[r1]-(hgnc_concept:Concept)-[r2:CODE]-(hgnc_code:Code {SAB:'HGNC'})
MATCH (gtex_cui)-[r3:located_in]-(ub_concept:Concept)-[r4:CODE]-(ub_code:Code {SAB:'UBERON'})
MATCH (gtex_cui)-[r5:p_value]-(pvalbin_concept:Concept)-[r6:CODE]-(pvalbin_code:Code {SAB:'PVALUEBINS'} ) 
RETURN * LIMIT 1
```

### <ins>The Human BioMolecular Atlas Program (HuBMAP)</ins>

The query extracts genes associated with the HubMAP Azimuth dataset (node SAB: `AZ`, edge SAB: `HMAZ`) clusters in human heart, liver and kidney tissues.

```cypher
MATCH (azimuth_term:Term)-[:PT]-(azimuth_code:Code {SAB:"AZ"})-[:CODE]-(azimuth_concept:Concept)-[r1 {SAB:"HMAZ"}]->(gene_concept:Concept)-[:CODE]-(gene_code:Code {SAB:"HGNC"}), (azimuth_concept:Concept)-[:isa]->(CL_concept:Concept)-[:CODE]-(CL_code:Code {SAB:"CL"})-[:PT]-(CL_term:Term) RETURN * LIMIT 1
```


### <ins>Gabriella Miller Kids First (GMKF)</ins>

Show the `belongs_to_cohort` relationship between a `KFPT` node (Kids First Patient) and a `KFCOHORT` (Kids First Cohort) node as well as the `KFGENEBIN` node:
```cypher
MATCH (kf_pt_code:Code {SAB:'KFPT'})-[r0:CODE]-(kf_pt_cui)-[r1:belongs_to_cohort]-(kf_cohort_cui:Concept)-[r2:CODE]-(kf_cohort_code:Code {SAB:'KFCOHORT'})
MATCH (kf_pt_cui)-[r3:has_phenotype]-(hpo_cui)-[r4:CODE]-(hpo_code:Code {SAB:'HPO'})
MATCH (kf_cohort_cui)-[r5:belongs_to_cohort]-(kfgenebin_cui)-[r6:CODE]-(kfgenebin_code:Code {SAB:'KFGENEBIN'})
MATCH (kfgenebin_cui)-[r7:gene_has_variants]-(hgnc_cui:Concept)-[r8:CODE]-(hgnc_code:Code {SAB:'HGNC'})
RETURN * LIMIT 1
```

### <ins>The Library of Integrated Network-Based Cellular Signatures (LINCS)</ins>

Show the `LINCS` relationship which maps `HGNC` nodes to `PUBCHEM` nodes (there is also a `negatively_regulated_by` relationship) and finding a second PUBCHEM compound which is `in_similarity_relationship_with` the first compound: 
```cypher
MATCH (hgnc_cui:Concept)-[:CODE]->(hgnc_code:Code {SAB:'HGNC'})-[]->(hgnc_term:Term)
MATCH (hgnc_cui)-[:positively_regulated_by {SAB:'LINCS'}]-(pubchem_cui_1:Concept)-[:CODE]-(pubchem_code_1:Code {SAB:'PUBCHEM'})
MATCH (pubchem_cui_1:Concept)-[:in_similarity_relationship_with {SAB:'LINS'}]-(pubchem_cui_2:Concept)-[:CODE]-(pubchem_code_2:Code {SAB:'PUBCHEM'})
RETURN * LIMIT 1 
```


## Tips and Tricks

- You might notice that some queries have a `MATCH` statement for every line while other queries have a single `MATCH` statement followed by several patterns seperated by a comma...Both styles produce identical query plans, they just represent two different syntax styles.

- Most of the queries in this tutorial should not take long to run (<10 seconds). But in general, to speed up the run time of a query it can be helpful to start with the smaller dataset or even a single node if possible. For example, if you know you want to search for a specific gene and the phenotypes it is related to, you would first want to `MATCH` on the gene and then on the relationships to the `HPO` dataset.

Here is an example using Cypher:

This query, where we `MATCH` on the `HGNC` gene of interest first, returns results in ~30ms.
```cypher
MATCH (hgnc_code:Code {CODE:'7881'})
MATCH (hgnc_code)-[:CODE]-(hgnc_cui)-[r]-(hpo_cui:Concept)-[:CODE]-(hpo_code:Code {SAB:'HPO'})
RETURN DISTINCT hgnc_code.CodeID, hpo_code.CodeID
```

meanwhile, this query, where we `MATCH` on the `HPO` dataset first, returns results in ~700ms.
```cypher
MATCH (hpo_cui)-[:CODE]-(hpo_code:Code {SAB:'HPO'})
MATCH (hpo_cui)-[r]-(hgnc_cui)-[:CODE]-(hgnc_code:Code {CODE:'7881'})
RETURN DISTINCT hgnc_code.CodeID, hpo_code.CodeID
```
The total run time for both queries is short because `HPO` is a small dataset, but the first query still runs over 20x faster. The speed up will be magnified if you are dealing with some of the larger datasets in the graph such as `GTEX` and `ERCC`.

Also, note that run times will vary from system to system but the relative speed up should be consistent. Additionally, Neo4j performs query caching, so if you are timing your own query run times just know that after you run a query for the first time Neo4j will cache the query and any identical queries submitted afterwards will be checked and (if found) returned much more quickly. This can make finding an 'average' run time of a query difficult and misleading if you're simply running the same query again and again. You can read about Neo4j's query caching [here](https://neo4j.com/developer/kb/understanding-the-query-plan-cache/).


