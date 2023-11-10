
# Petagraph Data Source Descriptions and Schema Reference

Each section in this document represents a dataset/ontology that the Petagraph team has ingested into the graph. The title of each section are named in the following format: `Name (SAB)`, were `Name` is the name of the dataset/ontology and `SAB` is the main Source Abbreviation of the dataset/ontology. SABs are properties on Code nodes and edges that allow a user to identify what dataset/ontology a Code or relationship came from.

Each section contains the following information,

- Title
- Source and Description of the dataset/ontology
- Description of how the dataset/ontology was preprocessed
- Schema figure
- Schema figure description
- Cypher query to produce the schema figure

    
For clarity, all schema figures in this document follow this color format:
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_key.png" alt="drawing" width="800"/>
  
[Genotype-Tissue Expression Portal, Expression data (GTEXEXP)]()  
[Genotype-Tissue Expression Portal, eQTL data (GTEXEQTL)]()  
[Genotype-Tissue Expression Portal, Coexpression data (GTEXCOEXP)]()  
[Human-Mouse Orthologs (HGNCHCOP)]()  
[Human gene-phenotype (HGNCHPO)]()  
[Mouse gene-phenotype (HCOPMP)]()  
[Human Phenotype Ontology to Mouse Phenotype mappings (HPOMP)]()  
[Human-Rat ENSEMBL orthology (RATHCOP)]()  
[GENCODE-HSCLO mappings (GENCODEHSCLO)]()  
[LINCS L1000 Gene-Perturbagen Associations (LINCS)]()  
[Connectivity Map (CMAP)]()  
[Homo Sapiens Chromosomal Ontology (HSCLO)]()  
[Molecular Signatures Database (MSIGDB)]()  
[ClinVar (CLINVAR)]()  
[Azimuth (AZ)]()  
[Protein - Protein Interactions (STRING)]()  
[Single Cell Fetal Heart expression data (ASP2019)]()  
[GlyGen: Computational and Informatics Resources for Glycoscience (GLYGEN)]()  
[Gabriella Miller Kids First (KF)]()  
[4D Nucleome Program (4DN)]()  
  
  
## Genotype-Tissue Expression Portal, Expression data (GTEXEXP) 
**Source**: Median transcript per million (TPM) expression levels were ingested from the file `GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct` located on the GTEx Portal website at **[https://gtexportal.org/home/datasets](https://gtexportal.org/home/datasets)**.
**Preproccessing**: No preprocessing was done on the median TPM dataset. We only filtered for median TPM expression levels that corresponded to an ENSEMBL gene id that could be mapped back to an HGNC Code.

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
##  Genotype-Tissue Expression Portal, eQTL data (GTEXEQTL) 
**Source**: The GTEx eQTL data we ingested comes from the file `GTEx_Analysis_v8_eQTL.tar` located on the GTEx Portal website at **[https://gtexportal.org/home/datasets](https://gtexportal.org/home/datasets)**.
**Preproccessing**: For this first ingestion of GTEx's eQTL data, we only included eQTLs that were present in every tissue. This reduced the number of eQTLs in the dataset from 71 million to 2.1 million. Furthermore, we did not include any eQTLs that were not mapped to genes with a valid HGNC Code. This criteria dropped about 14% of the eQTLs. We then created eQTL nodes and attached them to their respective gene (HGNC), tissue (UBERON), genomic location ([HSCLO](),see section below) and p-value (PVALUEBINS) nodes. The following list of numbers was used to create the p-value bins: `[0,1e-12,1e-11,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,.005,.01,.02,.03,.04,.05,.06]`
  
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
##  Genotype-Tissue Expression Portal, Coexpression data (GTEXCOEXP)
**Source**: The source of this data is the `GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct` from the GTEx Expression dataset above.
**Preproccessing**:  Co-expression of genes was computed using Pearson’s correlation. Gene pairs were included if the Pearson correlation coefficient was greater than 0.99. Computing co-expression pairs for all genes in all tissues resulted in many pairs even after filtering for pairs with a score above 0.99. To reduce the size of the data we included only gene co-expression pairs that are highly co-expressed in at least 5 tissues.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/gtexcoexp.png" alt="drawing" width="800"/>

**Schema Description**: Two HGNC Concepts are shown along with their Codes and preferred Terms. They're connected by a `coexpressed_with` relationship. There is an `evidence_class` property on the relationship that specifies how many tissues the two genes are highly co-expressed in.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code)-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
where type(r1) starts with 'coexpressed_with'
return * limit 1
```

---
## Human-Mouse Orthologs (HGNCHCOP)
**Source**: Mouse genes were downloaded from HGNC Comparisons of Orthology Predictions (HCOP) [https://www.genenames.org/tools/hcop/](https://www.genenames.org/tools/hcop/) (scroll to the bottom, under Bulk Downloads. Select Human - Mouse ortholog data)
The human to mouse orthology mapping data were also obtained in April 2023 from the HGNC HCOP tool. 
**Preproccessing**: We created new mouse gene Concepts and mapped them using the HCOP data to their corresponding human ortholog. Each orthologous pair share reciprocal relationships. Out of the 41,638 HGNC Codes in the UMLS, the HCOP tool found at least one mouse ortholog for 20,715 of them. 

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HGNCHCOP.png" alt="drawing" width="800"/>

**Schema Description**: HGNC Concept (blue), Code (yellow) and Term (brown) from HGNC on the left and its corresponding Mouse gene Concept and Code (SAB = `HCOP`) on the right. The SAB for this mapping dataset is `HGNCHCOP` and is located on the SAB property of the `in_1_to_1_relationship_with` and `inverse_in_1_to_1_relationship_with` relationships.


```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HCOP'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Human gene-phenotype (HGNCHPO)
**Source**:
We use the Human Phenotype (HPO) Ontology mappings for `genes_to_phenotype.txt` and `phenotype_to_genes.txt`. The HPO annotations can be found here: [https://hpo.jax.org/app/data/annotations](https://hpo.jax.org/app/data/annotations). 
These data are generated by the HPO group to use OMIM disease-gene associations to map all HPO phenotypes to genes with those phenotypes associated with diseases.  Therefore, a gene can be associated with several phenotypes, and a phenotype can be associated with several genes.
**Preproccessing**: This data did not need any preprocessing.


<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HGNCHPO.png" alt="drawing" width="800"/>

**Schema Description**: On the left hand side, an HGNC Concept (blue), Code (yellow) and Term (brown) nodes are connected to an HPO Concept node through an `associated_with` relationship. The SAB for this mapping dataset is HGNCHPO and it is located on the SAB property of the `associated_with` and `inverse_associated_with` relationships. In this example we can see that the ODAD2 gene is associated with Atelectasis.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HGNC'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HPO'})
return * limit 1
```

---
## Mouse gene-phenotype (HCOPMP)
**Source**: Mouse gene-to-phenotype (HCOPMP) data were obtained in January 2021 from multiple datasets from two separate databases. The first set of datasets were obtained from the international mouse phenotyping consortium (IMPC), which includes data from KOMP2, and can be found at http://ftp.ebi.ac.uk/pub/databases/impc/all-data-releases/latest/results/. We used the `genotype-phenotype-assertions-ALL.csv.gz` and the `statistical-results-ALL.csv.gz datasets` from this database. Both datasets contain, among other data, phenotype to gene mappings in the mouse. The second set of datasets were obtained from the mouse genome informatics (MGI) database and can be found at http://www.informatics.jax.org/downloads/reports/index.html#pheno. We used the `MGI_PhenoGenoMP.rpt (Table 5)`,  `MGI_GenePheno.rpt (Table 9)` and `MGI_Geno_DiseaseDO.rpt (Table 10)` datasets. All 3 datasets contain, among other data, mouse phenotype-to-gene mappings. 
**Preproccessing**: The datasets from IMPC and MGI were combined to create a master gene-to-phenotype mapping dataset. This master dataset contains 10,380 mammalian phenotype (MP) terms that are mapped to at least one mouse gene and 17,936 mouse genes that are mapped to at least one MP term.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HCOPMP.png" alt="drawing" width="800"/>

**Schema Description**: On the left hand side, an MP Concept (blue), Code (yellow) and Term (brown) nodes are connected to an HCOP Concept node through an `involved_in` relationship. The HCOP Code nodes represent mouse genes. The SAB for this mapping dataset is HCOPMP and it is located on the SAB property of the `involved_in` and `inverse_involved_in` relationships. 

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HCOP'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MP'})
return * limit 1
```

---
## Human Phenotype Ontology to Mouse Phenotype mappings (HPOMP)
**Source**:  Mappings between the HPO and MP were generated using the PheKnowLator tool,  [https://github.com/callahantiff/PheKnowLator](https://github.com/callahantiff/PheKnowLator) in December 2020.
**Preproccessing**: The mappings that PheKnowLator generated were then checked and edited manually for accuracy. We kept only the highest quality mappings which left us with ~1000 mappings. No other preprocessing was done on this data.
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HPOMP.png" alt="drawing" width="800"/>

**Schema Description**: A Concept (blue), Code (yellow) and Term (brown) from MP on the left and its corresponding HPO Concept, Code and Term on the right. They are connected through an `is_approximately_equivalent_to` relationship. The SAB for this mappings, HPOMP, can be found on the SAB property on the bidirectional relationships.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HPO'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MP'})
return * limit 1
```

---
## Human-Rat ENSEMBL orthology (RATHCOP)
**Source**: The source of the human ENSEMBL to rat ENSEMBL orthologs is the HGNC Comparisons of Orthology Predictions tool. Go to https://www.genenames.org/tools/hcop/, scroll to the Bulk Downloads section at bottom of the page, select `Rat` in the first drop down menu and `15 columns` and download the data.
**Preproccessing**: No preprocessing was needed on these mappings, we simply selected the `human_ensembl_gene` and `rat_ensembl_gene` columns.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/RATHCOP.png" alt="drawing" width="800"/>

**Schema Description**: ...

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'ENSEMBL'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'ENSEMBL'})
where a.CODE contains 'ENSR'
return * limit 1
```

---
## GENCODE-HSCLO mappings (GENCODEHSCLO)
**Source**: ... 
**Preproccessing**: ... 

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/GENCODEHSCLO.png" alt="drawing" width="800"/>

**Schema Description**: ...

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'GENCODE'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HSCLO'})
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
## Connectivity Map (CMAP)
**Source**: Signature perturbations of gene expression profiles as induced by chemical (small molecule) were obtained from the Ma’ayan Lab Harmonizome portal at [https://maayanlab.cloud/Harmonizome/dataset/CMAP+Signatures+of+Differentially+Expressed+Genes+for+Small+Molecules](https://maayanlab.cloud/Harmonizome/dataset/CMAP+Signatures+of+Differentially+Expressed+Genes+for+Small+Molecules)
**Preproccessing**:  In a similar manner to L1000 data integration discussed above, we obtained the edge lists of the CMAP Signatures of Differentially Expressed Genes for Small Molecules dataset from the Harmonizome database :https://maayanlab.cloud, (Lamb et al. 2006; Rouillard et al. 2016). The data was computed based on an earlier study (Lamb et al. 2006; Rouillard et al. 2016). The dataset added 2,625,336 new relationships (including reverse relationships) connecting the Petagraph `CHEBI` and `HGNC` nodes with types types of “negatively_correlated_with_gene”, “positively_correlated_with_gene”, “inverse_negatively_correlated_with_gene” and “inverse_positively_correlated_with_gene” and SAB of “CMAP”.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/CMAP.png" alt="drawing" width="800"/>

**Schema Description**: ...

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'CHEBI'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'CMAP'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Homo Sapiens Chromosomal Ontology (HSCLO)
**Source**: The Homo Sapiens Chromosomal Location Ontology (HSCLO)  was created by Taha Ahooyi Mohseni of the Petagraph team. HSCLO was primarily created to connect 4DN loop coordinates to the rest of the graph through the mapping between HSCLO and GENCODE. HSCLO was later utilized to connect GTEXEQTL locations in the graph as searchable nodes at 1kbp resolution. 
**Preproccessing**: The dataset relationships as well as nodes use HSCLO as their SAB. HSCLO nodes are defined at 5 resolution levels; chromosomes, 1 Mbp, 100 kbp, 10 kbp and 1kbp with each level connecting to lower levels with `above_(resolution level)_band` (e.g. "above_1Mbp_band", "above 1_kbp_band") and nodes at the same resolution level are connected through `precedes_(resolution level)_band` (e.g. "precedes_10kbp_band"). The dataset contains 3,431,155 nodes and 6,862,195 relationships.


### NEED BETTER HSCLO FIGURE
<img src=

"https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HSCLO.png" alt="drawing" width="800"/>

**Schema Description**: 

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HSCLO'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code)
MATCH (b)-[r3:loop_ds_end]-(c:Concept)-[:CODE]-(e:Code {SAB:'4DNL'})
MATCH  (b)-[r4:located_in]-(c2:Concept)-[:CODE]-(f:Code {SAB:'GTEXEQTL'})
return * limit 1
```

---
## Molecular Signatures Database (MSIGDB) 
**Sourcee**: MSigDB v7.4 datasets C1, C2, C3, C8 and H were obtained from the MSigDB molecular signature database. MSigDB is a collection of gene set resources, curated or collected from several different sources and can be accessed at [https://www.gsea-msigdb.org/gsea/msigdb/](https://www.gsea-msigdb.org/gsea/msigdb/). Five subsets of MSigDB v7.4 datasets were introduced as entity-gene relationships to the knowledge graph: C1 (positional gene sets), C2 (curated gene sets), C3 (regulatory target gene sets), C8 (cell type signature gene sets) and H (hallmark gene sets).
**Preproccessing**:  With these five datasets, we created MSIGDB Concept nodes for 31,516 MSigDB systematic names. The relationships between these Concept nodes and HGNC nodes were established considering the information available in each of the mentioned 5 subsets where the subset information was included in the relationship SABs as “MSIGDB”. The Term names were also compiled according to the MSigDB generic entity names. Collectively, the five MSIGDB datasets added 2,598,060 Concept-Concept relationships to Petagraph. The relationship types used to map MSigDB Concept nodes to HGNC Concept nodes are: `MSigDB C1`, `MSigDB C2`, `MSigDB C3`, `MSigDB C8`, `MSigDB H`. The MSIGDB Codes SAB property is: `MSigDB_Systematic_Name`.
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/MSIGDB.png" alt="drawing" width="800"/>

**Schema Description**: 

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HGNC'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MSIGDB'})
return * limit 1
```

---
## ClinVar (CLINVAR)
**Source**: Human genetic variant-disease associations were obtained from: [https://www.ncbi.nlm.nih.gov/clinvar/](https://www.ncbi.nlm.nih.gov/clinvar/). Only associations with Pathogenic or Likely Pathogenic consequence scores were included in the graph. We also did not include variants that affect a subset of genes (where there was no one-to-one relationship between a gene and phenotype/disease).
**Preproccessing**: The ClinVar human genetic variants-phenotype submission summary dataset (2023-01-05) was utilized to define relationships between human genes and phenotypes (Landrum et al. 2018). To retrieve the target phenotype/disease we used MEDGEN IDs listed in the ClinVar dataset (also already present in Petagraph). The `CLINVAR` variant-disease mappings gave rise to 214,040 new relationships (with the following characteristics [Type: “gene_associated_with_disease_or_phenotype”, SAB: “CLINVAR”] and [type: inverse_gene_associated_with_disease_or_phenotype, SAB: “CLINVAR”] connecting HGNC and MEDGEN, MONDO, HPO, EFO and MESH Concept nodes. 

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/CLINVAR.png" alt="drawing" width="800"/>

**Schema Description**: ...

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'UBERON'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'CLINVAR'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Azimuth (AZ)  


**Source**:  ...


**Preproccessing**: ...


<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/AZ.png" alt="drawing" width="800"/>

**Schema Description**: ...

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'AZ'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Protein - Protein Interactions (STRING)

**Source**: 
We used 9606.protein.links.full.v12.0 assertions obtained from STRING database and ...

**Preproccessing**: We converted ENSP entries to UNIPROTKB and filtered the dataset for the top 10% of the combined score. The refined dataset contains 459,701 relationships (919,402 including reverse ones) that connects UNIPROTKB nodes with the relationship type: “interacts_with” and “inverse_interacts_with”, SAB: “STRING” and evidence_class denotes the combined score for the relationship.


mention human only data....

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/STRING.png" alt="drawing" width="800"/>

**Schema Description**: ... 

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'UNIPROTKB'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'UNIPROTKB'})
return * limit 1
```

---
## Single Cell Fetal Heart expression data (ASP2019)

**Source**: 
Single cell Fetal heart data was obtained from the Asp et al. 2019 publication "A Spatiotemporal Organ-Wide Gene Expression and Cell Atlas of the Developing Human Heart", which can be found at https://pubmed.ncbi.nlm.nih.gov/31835037/. 

**Preproccessing**: Average gene expression of each cluster was calculated and used to represent each gene within a cell type cluster. Single cell heart concept nodes were created and connections to cell type nodes (author defined cell types, as many cell types  defined in the paper are not currently part of the Cell Ontology) and HGNC nodes connections were made. The Single cell heart Code nodes have an SAB of `ASP2019`  the cell types defined in the paper have an SAB of `ASP2019CLUSTER`.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/SCHEART.png" alt="drawing" width="800"/>

**Schema Description**: An `ASP2019CLUSTER` Code (yellow) and its Concept are shown in the upper left hand of the figure and an HGNC Concept node and its Code and Term nodes are shown on the upper right. Both of these Concepts are connected tp the `ASP2019` Concept in the center of the figure. The `ASP2019` Concept, which represents the expression of a gene in the fetal heart is connected to a `LOG2FCBINS` Concept node. The `LOG2FCBINS` Code node has `lowerbound` and `upperbound` properties which can be used to filter the log2 fold-change expression values of the genes as reported in the Asp study.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'ASP2019'})-[r0:CODE]-(b:Concept)-[r1:expressed_in]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
match (b)-[:expressed_in]-(e:Concept)-[:CODE]-(f:Code {SAB:'ASP2019CLUSTER'})
match (b)-[:log2FC]-(g:Concept)-[:CODE]-(h:Code {SAB:'LOG2FCBINS'})
return * limit 1
```

---
## GlyGen: Computational and Informatics Resources for Glycoscience (GLYGEN)

**Source**: 
Five datasets from the GlyGen website (https://data.glygen.org) (York et al. 2020)) were chosen based on their relevance to our preliminary use cases. The first two datasets were simply lists of genes that code for glycosyltransferase proteins in the human (https://data.glygen.org/GLY_000004) and mouse (https://data.glygen.org/GLY_000030). These datasets were modeled by creating a human glycosyltransferase’ Concept node as well as a ‘mouse glycosyltransferase’ Concept node. Then, the Concept nodes for humanthe genes (HGNC nodes) and mouse genes (HCOP nodes) were connected to their respective glycosyltransferase nodes with a ‘is_glycotransferase’ relationship. The next three datasets contain human O-linked and N-linked glycosylation information, namely O-GlcNac (human_proteoform_glycosylation_sites_o_glcnac_mcw.csv v1.12.3), Glyconnect (human_proteoform_glycosylation_sites_glyconnect.csv v1.12.3) and UniCarbKB (human_proteoform_glycosylation_sites_unicarbkb.csv v1.12.3) were obtained from GlyGen. These datasets contain information onof   human proteoforms, such asi.e. the exact residue on a protein isoform which is glycosylated, the type of glycosylation and the glycans found to bind that amino acid. To define relationships between human proteins from UniProtKB (UNIPROTKB concept nodes) (Boutet et al. 2016) and Glycans from the CHEBI resource (Hastings et al. 2016) (as included in CHEBI data) we introduced an intermediary ontology of gylcosylation sites derived from the information included in the mentioned dataset. In that process, we added 38,344 protein isoform relationships (type: “has_isoform”, target node SAB: “UNIPROTKB.ISOFROM”), 38,344 gylcosylation_type_site relationships (type: “has_type_site”, target node SAB: “GLY.TYPE.SITE”), 38,344 gylcosylation_type_site relationships (type: “binds_site”, source node SAB: “GLYTOUCAN”), all with SAB: “GLYGEN”.

**Preproccessing**: ...

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/GLYGEN.png" alt="drawing" width="800"/>

**Schema Description**: ... 

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'GLY.TYPE.SITE'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'GLYTOUCAN'})
match (b)-[r3]-(e:Concept)-[:CODE]-(f:Code {SAB:'UNIPROTKB.ISOFORM'})
return * limit 1
```

---
## Gabriella Miller Kids First (KF) -- phenotypes and variants per gene

**Source**: Patient-phenotype mappings were obtained from the Gabriella Miller Kids First (GMKF) data resource center. Variant per gene counts were also for the Congenital Heart Defects (CHD) Cohort from Gabriella Miller Kids First. 

**Preproccessing**: We added phenotypes from 5,006 patients, modeled as Concept nodes with SAB of KFPT, for Kids First Patient, and connected them to their respective HPO Concepts in the graph. The variant per gene counts were generated based on VCF files of the patients in the Congenital Heart Defects Cohort.
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/kf.png" alt="drawing" width="800"/>

**Schema Description**: The upper left Concept (blue) and Code (yellow) nodes represent a KF patient Concept and Code node, (SAB = KFPT). There are 5,006 KF Patient Concept and Code node pairs in Petagraph. The KFPT Concept node is connected to one or more Human Phenotype Ontology (HPO) Concepts. The KFPT Concept node is also connected to its corresponding KF Cohort Concept and Code node (SAB = KFCOHORT) through a `belongs_to_cohort` relationship type. There are 15 distinct KF cohorts the graph. On the right, the KF gene bin Concept and Code node pair (SAB = KFGENEBIN) connect to the KFCOHORT Concept and an HGNC Concept. The KFGENEBIN Code node has a 'value' property which is the number of high risk and de novo variants for that gene for the patients in that cohort. 

```cypher
// Cypher query to reproduce the schema figure
match (c0:Code {SAB:'KFCOHORT'})-[r0:CODE]-(cui1:Concept)-[r1:belongs_to_cohort]-(cui2:Concept )-[r2:CODE]-(c1:Code {SAB:'KFPT'})
match (cui2)-[r3:has_phenotype]-(cui3:Concept)-[r4:CODE]-(c2:Code {SAB:'HPO'})
match (cui1)-[r5:belongs_to_cohort]-(cui4:Concept)-[r6:CODE]-(c3:Code {SAB:'KFGENEBIN'})
match (cui4)-[r7:gene_has_variants]-(cui5:Concept)-[r8:CODE]-(c4:Code {SAB:'HGNC'})
return * LIMIT 1
```

---
## 4D Nucleome Program (4DN)

**Source**: 
23 loop files stored in dot call format were obtained from the 4D nucleome project website https://www.4dnucleome.org. The loop files were further processed for ingestion by first creating dataset nodes (SAB: “4DND”) with the respective terms containing the dataset information (assay type, lab and cell type involved), file nodes (SAB: “4DNF”) with the respective terms containing the file information, loop nodes (SAB: “4DNL”) attached to HSCLO nodes at 1kpb resolution level corresponding to upstream start and end and downstream start and end nodes of the characteristic anchor of the loop and q-value nodes (SAB: “4DNQ”) corresponding to donut q-value of the loops. 

**Preproccessing**: ...

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/4DN.png" alt="drawing" width="800"/>

**Schema Description**: ...

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'4DNF'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'4DNL'})
match (b)-[r3]-(e:Concept)-[:CODE]-(f:Code {SAB:'4DND'})
match (c)-[:loop_ds_end]-(g:Concept)-[:CODE]-(h:Code {SAB:'HSCLO'})
match (c)-[r4]-(i:Concept)-[:CODE]-(j:Code {SAB:'4DNQ'})
//match (j)-[r5]-(k:Concept)-[:CODE]-(l:Code {SAB:'UBERON'})
return * limit 1
```



# [BACK TO TOP]()


