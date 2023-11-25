
# Petagraph Data Source Descriptions and Schema Reference

Each section in this document represents a dataset/ontology that the Petagraph team has ingested into the graph. The title of each section are named in the following format: `Name (SAB)`, were `Name` is the name of the dataset/ontology and `SAB` is the main Source Abbreviation of the dataset/ontology. SABs are properties on Code nodes and edges that allow a user to identify what dataset/ontology a Code or relationship came from.

Each section contains the following information,

- Title
- Source and Description of the dataset/ontology
- Description of how the dataset/ontology was preprocessed
- Schema figure
- Schema figure description
- Cypher query to produce the schema figure

    
For clarity, all schema figures in this document follow this node color format:
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_key.png" alt="drawing" width="800"/>

[4D Nucleome Program (4DN)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#4d-nucleome-program-4dn)  
[Azimuth mappings (AZ)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#azimuth-mappings-az)  
[ClinVar (CLINVAR)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#clinvar-clinvar)  
[Connectivity Map (CMAP)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#connectivity-map-cmap)  
[Gabriella Miller Kids First data (KF)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#gabriella-miller-kids-first-data-kf)  
[GTEx, Expression data (GTEXEXP)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#gtex-expression-data-gtexexp
)  
[GTEx, eQTL data (GTEXEQTL)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#gtex-eqtl-data-gtexeqtl)  
[GTEx Coexpression data (GTEXCOEXP)]()  
[GlyGen (GLYGEN)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#glygen-computational-and-informatics-resources-for-glycoscience-glygen)  
[Homo Sapiens Chromosomal Location Ontology (HSCLO)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#homo-sapiens-chromosomal-location-ontology-hsclo)  
[Human gene-phenotype mappings (HGNCHPO)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#human-gene-phenotype-hgnchpo) 
[Human-Mouse Orthologs (HGNCHCOP)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#human-mouse-orthologs-hgnchcop)  
[Mouse gene-phenotype (HCOPMP)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#mouse-gene-phenotype-hcopmp)  
[Human Phenotype Ontology to Mouse Phenotype mappings (HPOMP)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#human-phenotype-ontology-to-mouse-phenotype-mappings-hpomp)  
[Human-Rat ENSEMBL orthologs (RATHCOP)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#human-rat-ensembl-orthology-rathcop)  

[LINCS L1000 Gene-Perturbagen Associations (LINCS)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#lincs-l1000-gene-perturbagen-associations-lincs)  

[Molecular Signatures Database (MSIGDB)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#molecular-signatures-database-msigdb)  

[Protein - Protein Interactions (STRING)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#protein---protein-interactions-string)  
[Single Cell Fetal Heart expression data (ASP2019)](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#single-cell-fetal-heart-expression-data-asp2019)  



## 4D Nucleome Program (4DN)

**Source**: 23 loop files stored in dot call format were obtained from the 4D nucleome project website https://www.4dnucleome.org. 

**Preproccessing**: The loop files were processed for ingestion by first creating dataset nodes (SAB: `4DND`) with the respective terms containing the dataset information (assay type, lab and cell type involved), file nodes (SAB: `4DNF`) with the respective terms containing the file information, loop nodes (SAB: `4DNL`) attached to `HSCLO` nodes at 1kpb resolution level corresponding to upstream start and end and downstream start and end nodes of the characteristic anchor of the loop and q-value nodes (SAB: `4DNQ`) corresponding to donut q-value of the loops. 

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/4DN_2.png" alt="drawing" width="800"/>

**Schema Description**: ...

```cypher
// Cypher query to reproduce the schema figure
MATCH (loop_concept:Concept)-[r2:loop_us_end {SAB:'4DN'}]->(us_end_concept:Concept)-[:CODE]->(us_end_code:Code)
MATCH (loop_concept:Concept)-[r3:loop_ds_start {SAB:'4DN'}]->(ds_start_concept:Concept)-[:CODE]->(ds_start_code:Code)
MATCH (loop_concept:Concept)-[r4:loop_ds_end {SAB:'4DN'}]->(ds_end_concept:Concept)-[:CODE]->(ds_end_code:Code)
MATCH (loop_code:Code {SAB:'4DNL'})<-[:CODE]-(loop_concept:Concept)-[r5:loop_has_qvalue_bin {SAB:'4DN'}
]->(qvalue_bin_concept:Concept)-[:CODE]->(qvalue_bin_code:Code {SAB:'4DNQ'})
MATCH (file_code:Code {SAB:'4DNF'})<-[:CODE]-(file_concept:Concept)-[r6:file_has_loop {SAB:'4DN'}]->(loop_concept:Concept)
MATCH (dataset_code:Code {SAB:'4DND'})<-[:CODE]-(dataset_concept:Concept)-[r7:dataset_has_file {SAB:'4DN'}]->(file_concept:Concept)
MATCH (dataset_concept:Concept)-[r8:dataset_involves_cell_type {SAB:'4DN'}]->(cell_type_concept:Concept)-[:PREF_TERM]->(cell_type_term:Term )
RETURN * LIMIT 1
```

---
## Azimuth mappings (AZ)  

**Source**: Marker genes per cell type mappings were downloaded from the [Azimuth](https://azimuth.hubmapconsortium.org) website which is part of the larger Human Biomolecular Atlas Project [HuBMAP](https://commonfund.nih.gov/HuBMAP)

**Preproccessing**: The data for human heart (evidence class: I2), kidney (evidence class: I2) and liver (evidence class: I2) were processed to establish relationships between AZ nodes and HGNC genes.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/AZ.png" alt="drawing" width="800"/>

**Schema Description**: An `AZ` Concept and Code are shown on the left and an `HGNC` Concept and Code are shown on the right. The two Concepts are connected through a `has_marker_gene_{TISSUE}` relationship, in this example, it is `has_marker_gene_kidney`. Currently, there are marker gene to cell type mappings from kidney, heart and liver.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'AZ'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1

match (a:Code {SAB:'AZ'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
match (b)-[r3 {SAB:'AZ'}]-(e:Concept)-[:CODE]-(f:Code)
return distinct f.SAB
```

## ClinVar (CLINVAR)
**Source**: Human genetic variant-disease associations were obtained from: [https://www.ncbi.nlm.nih.gov/clinvar/](https://www.ncbi.nlm.nih.gov/clinvar/). Only associations with Pathogenic or Likely Pathogenic consequence scores were included in the graph. We also did not include variants that affect a subset of genes (where there was no one-to-one relationship between a gene and phenotype/disease).  

**Preproccessing**: The ClinVar human genetic variants-phenotype submission summary dataset (2023-01-05) was utilized to define relationships between human genes and phenotypes (Landrum et al. 2018). To retrieve the target phenotype/disease we used MEDGEN IDs listed in the ClinVar dataset (also already present in Petagraph). The `CLINVAR` variant-disease mappings gave rise to 214,040 new relationships (with the following characteristics [Type: `gene_associated_with_disease_or_phenotype`, SAB: `CLINVAR`] and [type: `inverse_gene_associated_with_disease_or_phenotype`, SAB: `CLINVAR`] connecting `HGNC` and `MEDGEN`, `MONDO`, `HPO`, `EFO` and `MESH` Concept nodes. 

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/CLINVAR_2.png" alt="drawing" width="800"/>

**Schema Description**: An HGNC Concept, Code and Term node are shown on the left, connected to an HPO Concept, Code and Term node on the right through the `gene_associated_with_disease_or_phenotype` relationship. The SAB for this mapping dataset, `CLINVAR` is found on the SAB property of the relationship.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HPO'})<-[r0:CODE]-(b:Concept)-[r1 {SAB:'CLINVAR'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
where id(r1) = 29001875
match (a:Code {SAB:'HPO'})-[r0:CODE]-(b:Concept)-[r3 {SAB:'CLINVAR'}]->(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
where id(r3) = 52494094
return * limit 1
```

---
## Connectivity Map (CMAP)
**Source**: Signature perturbations of gene expression profiles as induced by chemical (small molecule) were obtained from the Ma’ayan Lab Harmonizome portal at [https://maayanlab.cloud/Harmonizome/dataset/CMAP+Signatures+of+Differentially+Expressed+Genes+for+Small+Molecules](https://maayanlab.cloud/Harmonizome/dataset/CMAP+Signatures+of+Differentially+Expressed+Genes+for+Small+Molecules)

**Preproccessing**:  In a similar manner to L1000 data integration discussed above, we obtained the edge lists of the CMAP Signatures of Differentially Expressed Genes for Small Molecules dataset from the Harmonizome database :https://maayanlab.cloud, (Lamb et al. 2006; Rouillard et al. 2016). The data was computed based on an earlier study (Lamb et al. 2006; Rouillard et al. 2016). The dataset added 2,625,336 new relationships (including reverse relationships) connecting the Petagraph `CHEBI` and `HGNC` nodes with types types of `negatively_correlated_with_gene`, `positively_correlated_with_gene`, `inverse_negatively_correlated_with_gene` and `inverse_positively_correlated_with_gene` all with a relationship SAB of `CMAP`.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/CMAP.png" alt="drawing" width="800"/>

**Schema Description**: A `CHEBI` Concept, Code node are shown on the left and an `HGNC` Concept and Code pair are shown on the right. The two Concepts are connected through a `positively_correlated_with_chemical_or_drug` relationship. There also exists a `negatively_correlated_with_chemical_or_drug` relationship.  The `CMAP` SAB can be found on the SAB property of the Concept-Concept relationships.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'CHEBI'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'CMAP'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Gabriella Miller Kids First data (KF)

**Source**: Patient-phenotype mappings were obtained from the Gabriella Miller Kids First (GMKF) data resource center. Variant per gene counts from the Congenital Heart Defects (CHD) Cohort from Gabriella Miller Kids First were also introduced into the graph. 

**Preproccessing**: We added phenotypes from 5,006 patients, modeled as Concept nodes with SAB of `KFPT`, for Kids First Patient, and connected them to their respective HPO Concepts in the graph. The variant per gene counts were generated based on VCF files of the patients in the Congenital Heart Defects Cohort. Only de novo variants and variants that received a VEP score of HIGH were included.
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/kf.png" alt="drawing" width="800"/>

**Schema Description**: The upper left Concept (blue) and Code (yellow) nodes represent a KF patient Concept and Code node, (SAB = `KFPT`). There are 5,006 KF Patient Concept and Code node pairs in Petagraph. The `KFPT` Concept node is connected to one or more Human Phenotype Ontology (`HPO`) Concepts. The `KFPT` Concept node is also connected to its corresponding KF Cohort Concept and Code node (SAB = KFCOHORT) through a `belongs_to_cohort` relationship type. There are 15 distinct KF cohorts the graph. On the right, the KF gene bin Concept and Code node pair (SAB = `KFGENEBIN`) connect to the `KFCOHORT` Concept and an HGNC Concept. The `KFGENEBIN` Code node has a 'value' property which is the number of high risk and de novo variants for that gene for all the patients in that cohort. 

```cypher
// Cypher query to reproduce the schema figure
match (c0:Code {SAB:'KFCOHORT'})-[r0:CODE]-(cui1:Concept)-[r1:belongs_to_cohort]-(cui2:Concept )-[r2:CODE]-(c1:Code {SAB:'KFPT'})
match (cui2)-[r3:has_phenotype]-(cui3:Concept)-[r4:CODE]-(c2:Code {SAB:'HPO'})
match (cui1)-[r5:belongs_to_cohort]-(cui4:Concept)-[r6:CODE]-(c3:Code {SAB:'KFGENEBIN'})
match (cui4)-[r7:gene_has_variants]-(cui5:Concept)-[r8:CODE]-(c4:Code {SAB:'HGNC'})
return * LIMIT 1
```
___

## GTEx, Expression data (GTEXEXP) 
**Source**: Median transcript per million (TPM) expression levels were ingested from the file `GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct` located on the GTEx Portal website at **[https://gtexportal.org/home/datasets](https://gtexportal.org/home/datasets)**. This gene expression dataset contains expression profiles 54 tissues and 56,200 transcripts.

**Preproccessing**: No preprocessing was done on the median TPM dataset. We only filtered for median TPM expression levels that corresponded to an ENSEMBL gene id that could be mapped back to an `HGNC` Code. The gene expression nodes are connected to their corresponding tissue node, gene node and expression bin node.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/gtex_exp.png" alt="drawing" width="800"/>

**Schema Description**: A tissue Concept and Code (SAB = `UBERON`) and a gene Concept and Code (SAB = `HGNC`) are connected via `expresses` relationships to a GTEx Expression Concept and Code (SAB = `GTEXEXP`). In this example, you can see that the ERCC6L gene has a median TPM between 1.0 and 2.0 in the venous blood. The `EXPBINS` Code node has `upperbound` and `lowerbound` properties which allow a user to filter genes based on the median TPM.
     
```cypher
// Cypher query to reproduce the schema figure
match (gtex_exp:Concept)-[:CODE]-(gtex_exp_code:Code {SAB:'GTEXEXP' })
match (gtex_exp)-[r1:expressed_in {SAB:'GTEXEXP'}]->(hgnc_concept:Concept)-[r2:CODE]-(hgnc_code:Code {SAB:'HGNC'}), (hgnc_concept)-[pt:PREF_TERM]-(t:Term)
match (gtex_exp)-[r3:expressed_in {SAB:"GTEXEXP"}]-(ub_concept:Concept)-[r4:CODE]-(ub_code:Code {SAB:'UBERON'}), (ub_concept)-[pt2:PREF_TERM]-(t2:Term)
match (gtex_exp)-[r5:has_expression]->(exp_concept:Concept)-[r6:CODE]-(exp_code:Code {SAB: 'EXPBINS' })
return * limit 1
```
  
--- 
##  GTEx, eQTL data (GTEXEQTL)
**Source**: The GTEx eQTL data we ingested comes from the file `GTEx_Analysis_v8_eQTL.tar` located on the GTEx Portal website at **[https://gtexportal.org/home/datasets](https://gtexportal.org/home/datasets)**. The eQTLs dataset contains over 71 million eQTLs from 49 tissues.

**Preproccessing**: For this first ingestion of GTEx's eQTL data, we only included eQTLs that were present in every tissue. This reduced the number of eQTLs in the dataset from 71 million to 2.1 million. Furthermore, we did not include any eQTLs that were not mapped to genes with a valid `HGNC` Code. This criteria dropped about 14% of the eQTLs. We then created eQTL nodes and attached them to their respective gene (`HGNC`), tissue (`UBERON`), genomic location ([HSCLO]([Homo Sapiens Chromosomal Ontology (HSCLO)]([https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#homo-sapiens-chromosomal-ontology-hsclo](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#homo-sapiens-chromosomal-location-ontology-hsclo))  ),see section below) and p-value (`PVALUEBINS`) nodes. The following list of numbers was used to create the p-value bins: `[0,1e-12,1e-11,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,.005,.01,.02,.03,.04,.05,.06]`
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/gtex_eqtl.png" alt="drawing" width="800"/>

**Schema Description**: A tissue Concept, Code (SAB = `UBERON`) and Term (top left), a gene Concept, Code (SAB = `HGNC`) and preferred Term (bottom left), a chromosomal location Concept and Code (SAB = `HSCLO`) and a p-value (SAB = `PVALUEBINS`) all connect to a GTEx eQTL Concept and Code (SAB = `GTEXEQTL`) in the center. The `PVALUEBINS` Code has `upperbound` and `lowerbound` properties on it, which bin the eQTLs p-value between them.

```cypher
// Cypher query to reproduce the schema figure
match (gtex_eqtl:Concept)-[r0]-(gtex_eqtl_code:Code) where gtex_eqtl_code.SAB = 'GTEXEQTL' 
match (gtex_eqtl)-[r1]-(hgnc_concept:Concept)-[r2]-(hgnc_code:Code {CodeID:'HGNC:52402'}) where hgnc_code.SAB = 'HGNC'
match (gtex_eqtl)-[r3:located_in]-(ub_concept:Concept)-[r4]-(ub_code:Code) where ub_code.SAB = 'UBERON'
match (gtex_eqtl)-[r5:p_value]-(exp_concept:Concept)-[r6]-(exp_code:Code) where exp_code.SAB = 'PVALUEBINS'  
match  (gtex_eqtl)-[r7]-(hsclo_concept:Concept)-[r8]-(hsclo_code:Code) where hsclo_code.SAB = 'HSCLO'  
return * limit 1
```

---
## GTEx Coexpression data (GTEXCOEXP)
**Source**: The source of this data is the `GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct` from the GTEx Expression dataset above.

**Preproccessing**:  Co-expression of genes was computed using Pearson’s correlation. Gene pairs were included if the Pearson correlation coefficient was greater than 0.99. Computing co-expression pairs for all genes in all tissues resulted in many pairs even after filtering for pairs with a score above 0.99. To reduce the size of the data we included only gene co-expression pairs that are highly co-expressed in at least 5 tissues.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/gtexcoexp.png" alt="drawing" width="800"/>

**Schema Description**: Two `HGNC` Concepts are shown along with their Codes and preferred Terms. They're connected by a `coexpressed_with` relationship. There is an `evidence_class` property on the relationship that specifies how many tissues the two genes are highly co-expressed in. The SAB for this dataset `GTEXCOEXP` is located on the `coexpressed_with` and the `inverse_coexpressed_with` 

```cypher
// Cypher query to reproduce the schema figure
match (a:Code)-[r0:CODE]-(b:Concept)-[r1:coexpressed_with {SAB:'GTEXCOEXP'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

## GlyGen (GLYGEN)

**Source**: Five datasets from the GlyGen website (https://data.glygen.org) (York et al. 2020)) were chosen based on their relevance to our preliminary use cases. The first two datasets were simply lists of genes that code for glycosyltransferase proteins in the human (https://data.glygen.org/GLY_000004) and mouse (https://data.glygen.org/GLY_000030). The other three datasets contain information on human proteoforms, such as the exact residue on a protein isoform which is glycosylated, the type of glycosylation and the glycans found to bind that amino acid. 
 
**Preproccessing**: The first two datasets which contain the names of genes that code for glycosyltransferase proteins  modeled by creating a human glycosyltransferase’ Concept node as well as a ‘mouse glycosyltransferase’ Concept node. Then, the Concept nodes for humanthe genes (`HGNC` nodes) and mouse genes (`HCOP` nodes) were connected to their respective glycosyltransferase nodes with a ‘is_glycotransferase’ relationship. To model the next three datasets, which contain data on protein isoform glycosylation, we created relationships between human proteins from UniProtKB (`UNIPROTKB` Concept nodes) (Boutet et al. 2016) and Glycans from the `CHEBI` resource (Hastings et al. 2016). More specifically, we introduced an intermediary ontology of gylcosylation sites derived from the information included in the mentioned dataset. This data added 38,344 protein isoform relationships (type: `has_isoform`, target node SAB: `UNIPROTKB.ISOFROM`), 38,344 gylcosylation_type_site relationships (type: “has_type_site”, target node SAB: `GLY.TYPE.SITE`), 38,344 gylcosylation_type_site relationships (type: `binds_site`, source node SAB: `GLYTOUCAN`), all with SAB: `GLYGEN`.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/GLYGEN_2.png" alt="drawing" width="800"/>

**Schema Description**: ... 

```cypher
// Cypher query to reproduce the schema figure
MATCH (o0)<-[:CODE]-(g:Concept)-[:has_gene_product]->(u:Concept)-[:has_isoform]-(i:Concept)-[:has_type_site]-(s:Concept)<-[:binds_site]-(l:Concept),(g)-[:PREF_TERM]->(t1:Term),(u)-[:CODE]->(o2:Code),(u)-[PREF_TERM]->(t2:Term),(s)-[:CODE]->(o3:Code), (l)-[:CODE]->(o4:Code),(i)-[:CODE]->(o5:Code) RETURN * LIMIT 1
```

---
## Homo Sapiens Chromosomal Location Ontology (HSCLO)
**Source**: The Homo Sapiens Chromosomal Location Ontology (HSCLO)  was created by Taha Ahooyi Mohseni of the Petagraph team. HSCLO was primarily created to connect 4DN loop coordinates to the rest of the graph through the mapping between HSCLO and GENCODE. HSCLO was later utilized to connect `GTEXEQTL` locations in the graph as searchable nodes at 1kbp resolution. 

**Preproccessing**: The dataset relationships as well as Code nodes use `HSCLO` as their SAB. `HSCLO` nodes are defined at 5 resolution levels; chromosomes, 1 Mbp, 100 kbp, 10 kbp and 1kbp with each level connecting to lower levels with `above_(resolution level)_band` (e.g. `above_1Mbp_band`, `above 1_kbp_band`) and nodes at the same resolution level are connected through `precedes_(resolution level)_band` (e.g. `precedes_10kbp_band`). The dataset contains 3,431,155 nodes and 6,862,195 relationships.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HSCLO_2.png" alt="drawing" width="800"/>

**Schema Description**: there are two types of connections (layers) between the `HSCLO` nodes; hierarchical, which relates nodes at different levels of resolution to their children nodes in a tree format, e.g. 1 Mbp nodes to 100 kbp nodes, and adjacency where nodes at the same level of resolution are linked together in a chain format. The layers of resolution include human genome, human chromosomes, 1 Mbp bands, 100 kbp bands, 10 kbp bands and 1 kbp bands.

```cypher
// Cypher query to reproduce the schema figure
MATCH (c1:Concept)-[:contains_chromosome{SAB:'HSCLO'}]->(c2:Concept)-[:above_1Mbp_band {SAB:'HSCLO'}]->(c3:Concept)-[:above_100kbp_band {SAB:'HSCLO'}]->(c4:Concept)-[:above_10kbp_band {SAB:'HSCLO'}]->(c5:Concept)-[:above_1kbp_band {SAB:'HSCLO'}]->(c6:Concept),
(c3:Concept)-[:precedes_1Mbp_band {SAB:'HSCLO'}]->(c7:Concept),
(c4:Concept)-[:precedes_100kbp_band {SAB:'HSCLO'}]->(c8:Concept),
(c5:Concept)-[:precedes_10kbp_band {SAB:'HSCLO'}]->(c9:Concept),
(c6:Concept)-[:precedes_1kbp_band {SAB:'HSCLO'}]->(c10:Concept),
(c1)-[:CODE]->(o1:Code),(c2)-[:CODE]->(o2:Code),(c3)-[:CODE]->(o3:Code),(c4)-[:CODE]->(o4:Code),(c5)-[:CODE]->(o5:Code),(c6)-[:CODE]->(o6:Code),(c7)-[:CODE]->(o7:Code),(c8)-[:CODE]->(o8:Code),(c9)-[:CODE]->(o9:Code),(c10)-[:CODE]->(o10:Code)
RETURN * LIMIT 1
```

---
## Human gene-phenotype mappings (HGNCHPO)
**Source**:
We use the Human Phenotype (HPO) Ontology mappings for `genes_to_phenotype.txt` and `phenotype_to_genes.txt`. The HPO annotations can be found here: [https://hpo.jax.org/app/data/annotations](https://hpo.jax.org/app/data/annotations). These data are generated by the HPO group using OMIM disease-gene associations to map HPO phenotypes to genes. These data contain 4,545 genes mapped to at least one phenotype and 10,896 phenotypes mapped to at least one gene

**Preproccessing**: This data did not need any preprocessing.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HGNCHPO.png" alt="drawing" width="800"/>

**Schema Description**: On the left hand side, an `HGNC` Concept (blue), Code (yellow) and Term (brown) nodes are connected to an `HPO` Concept node through an `associated_with` relationship. The SAB for this mapping dataset is `HGNCHPO` and it is located on the SAB property of the `associated_with` and `inverse_associated_with` relationships. In this example we can see that the ODAD2 gene is associated with Atelectasis.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HGNC'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HPO'})
return * limit 1
```

---
## Human-Mouse Ortholog mappings (HGNCHCOP)
**Source**: Mouse genes were downloaded from HGNC Comparisons of Orthology Predictions (HCOP) [https://www.genenames.org/tools/hcop/](https://www.genenames.org/tools/hcop/) (scroll to the bottom, under Bulk Downloads. Select Human - Mouse ortholog data)
The human to mouse orthology mapping data were also obtained in April 2023 from the HGNC HCOP tool. 

**Preproccessing**: We created new mouse gene Concepts and mapped them using the HCOP data to their corresponding human ortholog. Each orthologous pair share reciprocal relationships. Out of the 41,638 HGNC Codes in the UMLS, the HCOP tool found at least one mouse ortholog for 20,715 of them. 

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HGNCHCOP.png" alt="drawing" width="800"/>

**Schema Description**: An `HGNC` Concept (blue), Code (yellow) and Term (brown) on the left and its corresponding Mouse gene Concept and Code (SAB = `HCOP`) on the right. The SAB for this mapping dataset is `HGNCHCOP` and is located on the SAB property of the `in_1_to_1_relationship_with` and `inverse_in_1_to_1_relationship_with` relationships.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HCOP'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Human-to-mouse phenotype mapping (HPOMP)
**Source**:  Mappings between the HPO and MP were generated using the PheKnowLator tool,  [https://github.com/callahantiff/PheKnowLator](https://github.com/callahantiff/PheKnowLator) in December 2020.

**Preproccessing**: The mappings that PheKnowLator generated were then checked and edited manually for accuracy. We kept only the highest quality mappings which left us with ~1000 mappings. No other preprocessing was done on this data.
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HPOMP.png" alt="drawing" width="800"/>

**Schema Description**: A Concept (blue), Code (yellow) and Term (brown) from `MP` on the left and its corresponding `HPO` Concept, Code and Term on the right. They are connected through an `is_approximately_equivalent_to` relationship. The SAB for this mappings, `HPOMP`, can be found on the SAB property on the bidirectional relationships.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HPO'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MP'})
return * limit 1
```

---
## Human-Rat ENSEMBL orthologs (RATHCOP)
**Source**: The source of the human ENSEMBL to rat ENSEMBL orthologs is the HGNC Comparisons of Orthology Predictions tool. Go to https://www.genenames.org/tools/hcop/, scroll to the Bulk Downloads section at bottom of the page, select `Rat` in the first drop down menu and `15 columns` and download the data.

**Preproccessing**: No preprocessing was needed on these mappings, we simply selected the `human_ensembl_gene` and `rat_ensembl_gene` columns from the dataset.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/RATHCOP.png" alt="drawing" width="800"/>

**Schema Description**: A human ENSEMBL Concept and Code are shown on the left its orthologous rat ENSEMBL Concept and Code are shown on the right. The Concepts are connected by `has_human_ortholog` and `inverse_has_human_ortholog` relationships. The `RATHCOP` SAB is located on the SAB property of both Concept-Concept relationships.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'ENSEMBL'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'ENSEMBL'})
where a.CODE contains 'ENSR'
return * limit 1
```

---
### LINCS L1000 Gene-Perturbagen Associations (LINCS)
**Source**: The LINCS L1000 Connectivity Map dataset was obtained from the Ma’ayan Lab Harmonizome portal at [https://maayanlab.cloud/Harmonizome/search?t=all&q=l1000](https://maayanlab.cloud/Harmonizome/search?t=all&q=l1000) (Duan et al. 2014; Rouillard et al. 2016). We introduced gene-small molecule perturbagen relationships to Petagraph based on the LINCS L1000 edge list.

**Preproccessing**: These relationships were summarized from LINCS L1000 CMAP Signatures of Differentially Expressed Genes for Small Molecules dataset. This was done by first finding the corresponding CHEBI Concept nodes for the L1000 small molecules and then establishing the relationship of such nodes to the Petagraph HGNC nodes according to the edge list mentioned above. For that purpose, the relationships were collapsed to exclude the cell line, dosage, and treatment time information but the effect directions were retained in relationship types. This led to 3,198,094 relationships (bidirectional) with `LINCS` as the SAB and the following relationship types: `negatively_correlated_with_gene`, `positively_correlated_with_gene`, `inverse_negatively_correlated_with_gene` and `inverse_positively_correlated_with_gene`.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/LINCS.png" alt="drawing" width="800"/>

**Schema Description**: ...

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'CHEBI'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'LINCS'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Molecular Signatures Database (MSIGDB) 
**Sourcee**: MSigDB v7.4 datasets C1, C2, C3, C8 and H were obtained from the MSigDB molecular signature database. MSigDB is a collection of gene set resources, curated or collected from several different sources and can be accessed at [https://www.gsea-msigdb.org/gsea/msigdb/](https://www.gsea-msigdb.org/gsea/msigdb/). Five subsets of MSigDB v7.4 datasets were introduced as entity-gene relationships to the knowledge graph: C1 (positional gene sets), C2 (curated gene sets), C3 (regulatory target gene sets), C8 (cell type signature gene sets) and H (hallmark gene sets).

**Preproccessing**:  With these five datasets, we created `MSIGDB` Concept nodes for 31,516 MSigDB systematic names. The relationships between these Concept nodes and HGNC nodes were established considering the information available in each of the mentioned 5 subsets where the subset information was included in the relationship SABs as `MSIGDB`. The Term names were also compiled according to the MSigDB generic entity names. Collectively, the five `MSIGDB` datasets added 2,598,060 Concept-Concept relationships to Petagraph. The relationship types used to map MSigDB Concept nodes to `HGNC` Concept nodes are: `MSigDB C1`, `MSigDB C2`, `MSigDB C3`, `MSigDB C8`, `MSigDB H`.
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/MSIGDB.png" alt="drawing" width="800"/>

**Schema Description**: An `HGNC` Concept, Code and Term node are connected to an `HGNC` Concept, Code and Term node on the right. The `MSIGDB` SAB is located on the SAB property for both sets of relationships.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HGNC'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MSIGDB'})
return * limit 1
```

---
## Mouse gene-phenotype (HCOPMP)
**Source**: Mouse gene-to-phenotype (HCOPMP) data were obtained in January 2021 from multiple datasets from two separate databases. The first set of datasets were obtained from the international mouse phenotyping consortium (IMPC), which includes data from KOMP2, and can be found at http://ftp.ebi.ac.uk/pub/databases/impc/all-data-releases/latest/results/. We used the `genotype-phenotype-assertions-ALL.csv.gz` and the `statistical-results-ALL.csv.gz datasets` from this database. Both datasets contain, among other data, phenotype to gene mappings in the mouse. The second set of datasets were obtained from the mouse genome informatics (MGI) database and can be found at http://www.informatics.jax.org/downloads/reports/index.html#pheno. We used the `MGI_PhenoGenoMP.rpt (Table 5)`,  `MGI_GenePheno.rpt (Table 9)` and `MGI_Geno_DiseaseDO.rpt (Table 10)` datasets. All 3 datasets contain, among other data, mouse phenotype-to-gene mappings. 

**Preproccessing**: The datasets from IMPC and MGI were combined to create a master gene-to-phenotype mapping dataset. This master dataset contains 10,380 mammalian phenotype (MP) terms that are mapped to at least one mouse gene and 17,936 mouse genes that are mapped to at least one MP term.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HCOPMP.png" alt="drawing" width="800"/>

**Schema Description**: On the left hand side, an `MP` Concept (blue), Code (yellow) and Term (brown) nodes are connected to an `HCOP` Concept node through an `involved_in` relationship. The `HCOP` Code nodes represent mouse genes. The SAB for this mapping dataset is HCOPMP and it is located on the SAB property of the `involved_in` and `inverse_involved_in` relationships. 

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HCOP'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MP'})
return * limit 1
```

---
## Single Cell Fetal Heart expression data (ASP2019)

**Source**: Single cell RNAseq data from human fetal heart tissue was obtained from the Asp et al. 2019 publication "A Spatiotemporal Organ-Wide Gene Expression and Cell Atlas of the Developing Human Heart", which can be found at https://pubmed.ncbi.nlm.nih.gov/31835037/. 

**Preproccessing**: Average gene expression of each cluster was calculated and used to represent each gene within a cell type cluster. Single cell fetal heart concept nodes were created and connections to cell type nodes from the Cell Ontology (CL) and HGNC nodes connections were made. There were also quite a few cell types defined in the Asp et al. paper that do not currently exist in the CL. We created our own cell type Concept nodes for these cell types with an SAB of ‘ASP2019CLUSTER’. The Single cell heart Code nodes have an SAB of `ASP2019`.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/SCHEART.png" alt="drawing" width="800"/>

**Schema Description**: An `ASP2019CLUSTER` Code (yellow) and its Concept are shown in the upper left hand of the figure and an `HGNC` Concept node and its Code and Term nodes are shown on the upper right. Both of these Concepts are connected tp the `ASP2019` Concept in the center of the figure. The `ASP2019` Concept, which represents the expression of a gene in the fetal heart is connected to a `LOG2FCBINS` Concept node. The `LOG2FCBINS` Code node has `lowerbound` and `upperbound` properties which can be used to filter the log2 fold-change expression values of the genes as reported in the Asp study.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'ASP2019'})-[r0:CODE]-(b:Concept)-[r1:expressed_in]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
match (b)-[:expressed_in]-(e:Concept)-[:CODE]-(f:Code {SAB:'ASP2019CLUSTER'})
match (b)-[:log2FC]-(g:Concept)-[:CODE]-(h:Code {SAB:'LOG2FCBINS'})
return * limit 1
```

---

## STRING

**Source**:  We ingested human protein to protein interaction data from the STRING website. To download the file, navigate to the STRING download page [here](https://string-db.org/cgi/download?sessionId=bhAGIM6ZbBmX) and select Homo Sapiens in the drop down box. Then download the 9606.protein.links.full.v12.0 file.

**Preproccessing**: We converted human ENSEMBL protein IDs to UNIPROTKB IDs and filtered the dataset for the top 10% of the combined score. The refined dataset contains 459,701 relationships (919,402 including reverse ones) that connect `UNIPROTKB` nodes with the relationship types `interacts_with` and `inverse_interacts_with`. The SAB `STRING`  and `evidence_class` which denotes the combined score for the relationship, are both found on these Concept-Concept relationships.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/STRING.png" alt="drawing" width="800"/>

**Schema Description**: A `UNIPROTKB` Concept, Code and Term node are connected to another set of `UNIPROTKB` Concept, Code and Term nodes on the right through an `interacts_with` relationship. The SAB property on the edge of this relationship is `STRING`.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'UNIPROTKB'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'UNIPROTKB'})
return * limit 1
```
---


# [BACK TO TOP](https://github.com/TaylorResearchLab/Petagraph/blob/main/petagraph/data_dict.md#petagraph-data-source-descriptions-and-schema-reference)


