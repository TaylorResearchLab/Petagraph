## Cypher queries to produce graph figures for "Petagraph: A large-scale unifying knowledge graph framework for integrating biomolecular and biomedical data"

##### Figure 1. Petagraph Data Ingestion Workflow. 
- Figure 1 was made using an online workflow tool called [Canva](https://www.canva.com)

##### Figure 2. Example of the Concept-Code-Term schema
```
MATCH (c:Concept)-[:CODE]-(s:Code {CODE:'HGNC:11998'})-[r]-(t:Term)
RETURN * 
```

##### Figure 3. 
Dataset interconnectedness jupyter notebook?
[here](https://github.com/TaylorResearchLab/Petagraph/tree/main/scripts/code)


##### Figure 4.
Semantic type statistics in Petagraph.
```
MATCH (s:Semantic)<-[:STY]-(c:Concept)
RETURN s1.name as STY, Count(c1) As Count
```

##### Figures 5, 6, 7.
Heatmap representation of relationship statistics of 55 selected semantic types.
```
MATCH (s1:Semantic)<-[:STY]-(c1:Concept)-[r]->(c2:Concept)-[:STY]->(s2:Semantic)
RETURN s1.name as STY1, s2.Name as STY2
```

##### Figure 8.
Shortest Path Lengths in Petagraph. Probability density of associated Concept to Concept node shortest path lengths for 1 million pairwise combinations of human gene Concept nodes in Petagraph.
```
MATCH (O1:Code {SAB:'HGNC'})<-[R1:CODE]-(C1:Concept)-[:PREF_TERM]->(T1:Term),
(T2:Term)<-[:PREF_TERM]-(C2:Concept)-[R2:CODE]->(O2:Code {SAB:'HGNC'}),
p = shortestpath((C1)-[*]->(C2)) RETURN T1.name AS Gene_1,T2.name AS Gene_2,length(p) AS Shoretest_Path_Length
```

##### Figure 9: Query results on heart-defect phenotype-associated glycosylation targets.
Common Neighbors Scores in Petagraph. Here we show a comparison between the Common Neighbors scores for genes connected with direct links in Petagraph (blue) versus random selections from all genes regardless of their direct connectivity.
```
```

##### Figure 10.
Validation using local graph structure.
```
//Petagraph Subgraph Projection
MATCH (source:Concept)-[r]->(target:Concept) with gds.graph.project('sg', source, target) AS g RETURN g.graphName AS gr, g.nodeCount AS N, g.relationshipCount AS rels

//Petagraph Transitivity (Local Clustering Coefficient)
CALL gds.localClusteringCoefficient.stream('sg')
YIELD nodeId, localClusteringCoefficient
RETURN gds.util.asNode(nodeId).CUI AS CUI, localClusteringCoefficient
ORDER BY localClusteringCoefficient DESC, CUI
```

##### Figure 11.
Validation using embeddings and dimensionality reduction.
```
//Petagraph Subgraph Projection
MATCH (source:Concept)-[r]->(target:Concept) with gds.graph.project('sg', source, target) AS g RETURN g.graphName AS gr, g.nodeCount AS N, g.relationshipCount AS rels
//Petagraph Node2Vec
CALL gds.node2vec.stream('sg',{embeddingDimension: 100}) YIELD nodeId, embedding RETURN gds.util.asNode(nodeId).Name AS Name,labels(gds.util.asNode(nodeId)) AS Label, embedding
```

##### Figure 12.
Contribution of major datasets on link prediction. Impact of dataset removal on global transitivity and degree assortativity in subgraphs around human genes (1 hop) in Petagraph.
```
//Petagraph Subgraph Projection
MATCH (source:Concept)-[r]->(target:Concept) with gds.graph.project('sg', source, target) AS g RETURN g.graphName AS gr, g.nodeCount AS N, g.relationshipCount AS rels

//Petagraph Transitivity (Local Clustering Coefficient)
CALL gds.localClusteringCoefficient.stream('sg')
YIELD nodeId, localClusteringCoefficient
RETURN gds.util.asNode(nodeId).CUI AS CUI, localClusteringCoefficient
ORDER BY localClusteringCoefficient DESC, CUI
```

##### Figure 13.
Validation with Use Case 1. Comparison of ROC and PRC curves calculated for the link prediction scores vs. the presence or absence of direct links (binary classifier) between Tetralogy of Fallot (HP:0001636) phenotype and human genes in Petagraph. 
```
//Total Neighbors Algorithm
MATCH (o1:Code {CODE:"HP:0001636"})<-[:CODE]-(c1:Concept), (t2:Term)<-[:SYN]-(o2:Code {SAB:"HGNC"})<-[:CODE]-(c2:Concept)
RETURN distinct o2.CODE as HGNC_ID, gds.alpha.linkprediction.totalNeighbors(c1, c2) AS TN_score
//Preferntial Attachment Algorithm
MATCH (o1:Code {CODE:"HP:0001636"})<-[:CODE]-(c1:Concept), (t2:Term)<-[:SYN]-(o2:Code {SAB:"HGNC"})<-[:CODE]-(c2:Concept)
RETURN distinct o2.CODE as HGNC_ID, gds.alpha.linkprediction.preferntialAttachment(c1, c2) AS PA_score
//Common Neighbors Algorithm
MATCH (o1:Code {CODE:"HP:0001636"})<-[:CODE]-(c1:Concept), (t2:Term)<-[:SYN]-(o2:Code {SAB:"HGNC"})<-[:CODE]-(c2:Concept)
RETURN distinct o2.CODE as HGNC_ID, gds.alpha.linkprediction.commonNeighbors(c1, c2) AS PA_score
```

##### Figure 14.
Validation with Use Case 2. Querying possible drug-tissue interactions for rofecoxib using CMAP, LINCS L1000 and GTEX_EXP datasets. 
```
//Drug-Gene-Tissues
WITH 'rofecoxib' AS COMPOUND_NAME, 5 AS MIN_EXP
MATCH (ChEBITerm:Term {name:COMPOUND_NAME})<-[:PT]-(ChEBICode:Code {SAB:'CHEBI'})<-[:CODE]-(ChEBIconcept:Concept)-[r1{SAB:"LINCS"}]-(hgncConcept:Concept)-[:expresses {SAB:'GTEXEXP'}]->(gtexexp_concept:Concept)<-[:expresses {SAB:'GTEXEXP'}]-(tissue_concept:Concept)-[:PREF_TERM]-(tissue_term:Term)<-[]-(:Code {SAB:'UBERON'}),(gtexexp_concept:Concept)-[:has_expression {SAB:'GTEXEXP'}]->(exp_concept:Concept)-[:CODE]-(exp_code:Code),(hgncConcept)-[:CODE]->(hgncCode:Code{SAB:'HGNC'})-[:SYN]-(hgncTerm:Term) WHERE exp_code.lowerbound > MIN_EXP
RETURN DISTINCT ChEBITerm.name AS Compound, hgncTerm.name AS GENE, tissue_term.name AS Tissue, exp_code.CODE AS Expression_Level
```

##### Figure 15.
Validation through shortest path analysis. Analysis of connections between HPO terms in a Petagraph subgraph between abnormal central nervous system (CNS) morphology and CNS neoplastic processes
```
//Shortest Path Between HPO Groups
LOAD CSV WITH HEADERS FROM 'file:///CNS_NP.csv' AS PH UNWIND PH.V1 AS CNSO UNWIND PH.V2 AS NPO WITH COLLECT(DISTINCT CNSO) AS O1, COLLECT(DISTINCT NPO) AS O2 MATCH (o1:Code)<-[:CODE]-(c1:Concept), (o2:Code)<-[:CODE]-(c2:Concept), p = shortestPath((c1)-[*]->(c2)) WHERE o1.CodeID IN O1 and o2.CodeID IN O2 return o1.CodeID as start_hpo, o2.CodeID as end_hpo, length(p) as p_length,[x in nodes(p)|x.CUI]
```


##### Figure 16.
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




