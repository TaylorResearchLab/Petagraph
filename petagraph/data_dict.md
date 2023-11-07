
# Petagraph Data Source Descriptions and Schema Reference

Each section contains the following information,

- Title
- Source and Description of the dataset/ontology
- Description of how the dataset/ontology was preprocessed
- Schema figure
- Schema figure description
- Cypher query to produce the schema figure

    
For clarity, all schema figures in this document follow this color format:
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_key.png" alt="drawing" width="800"/>
  

[Genotype-Tissue Expression (GTEx) Portal]()  
[Human-Mouse Orthologs (HGNCHCOP)]()  
[Human gene-phenotype (HGNCHPO)]()  
[Mouse gene-phenotype (HCOPMP)]()  
[Human Phenotype Ontology (HPO) to Mouse Phenotype (MP) mappings (HPOMP)]()  
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
  
  
## Genotype-Tissue Expression (GTEx) Portal
**Source**: We ingested two datasets from **[https://gtexportal.org/home/datasets](https://gtexportal.org/home/datasets):**
    - GTEx_Analysis_v8_eQTL (all files in this directory) -- only common eQTLs that were present in every tissue
    - GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct

**Preproccessing**: ...

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/gtex_exp.png" alt="drawing" width="800"/>
     
```cypher
// Cypher query to reproduce the schema figure
match (gtex_exp:Concept)-[:CODE]-(gtex_exp_code:Code {SAB:'GTEXEXP' })
match (gtex_exp)-[r1:expressed_in {SAB:'GTEXEXP'}]->(hgnc_concept:Concept)-[r2:CODE]-(hgnc_code:Code {SAB:'HGNC'}), (hgnc_concept)-[pt:PREF_TERM]-(t:Term)
match (gtex_exp)-[r3:expressed_in {SAB:"GTEXEXP"}]-(ub_concept:Concept)-[r4:CODE]-(ub_code:Code {SAB:'UBERON'}), (ub_concept)-[pt2:PREF_TERM]-(t2:Term)
match (gtex_exp)-[r5:has_expression]->(exp_concept:Concept)-[r6:CODE]-(exp_code:Code {SAB: 'EXPBINS' })
return * limit 1
```
  

  
--- 
## GTEXEQTL

**Source**: ... 
  

**Preproccessing**: ...
  

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/gtex_eqtl.png" alt="drawing" width="800"/>


An UBERON Concept, Code and Term (top left), an HGNC Concept and preferred Term (top right) and GTEx eQTL Concept, Code and Terms (center). The GTEx Terms shown here represent a binned  p-value and variant ID for the eQTL.

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
## GTEXCOEXP
**Source**:
- Co-expression of genes were computed using Pearson’s correlation > 0.9 in 37 human tissues according to the GTEx expression data:
- GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct
- Relationship Name: `coexpressed_with`
- Tissue where the co-expression is detected is in the SAB of the relationship  “coexpressed_with”

**Preproccessing**:

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/gtexcoexp.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code)-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
where type(r1) starts with 'coexpressed_with'
return * limit 1
```


---
## Human-Mouse Orthologs (HGNCHCOP)

**Source**:
- Orthologs from HGNC Comparisons of Orthology Predictions (**HCOP**) [https://www.genenames.org/tools/hcop/](https://www.genenames.org/tools/hcop/) (scroll to the bottom, under Bulk Downloads. Select Human - Mouse ortholog data)

**Preproccessing**:
-  were obtained in April 2023 from the HGNC Comparisons of Orthology Predictions (HCOP) tool at https://www.genenames.org/tools/hcop/. We created new mouse gene Concepts and mapped them using the HCOP data to their corresponding human ortholog. Each orthologous pair share reciprocal relationships, ('has_human_ortholog', 'has_mouse_ortholog') and out of the 41,638 HGNC Codes in the UMLS, the HCOP tool found at least one mouse ortholog for 20,715 HGNC Codes. 

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HGNCHCOP.png" alt="drawing" width="800"/>

HGNC Concept (blue), Code (purple) and Term (green) from HGNC on the left and its corresponding Mouse gene Concept and code on the right  


```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HCOP'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Human gene-phenotype (HGNCHPO)

**Source**:
We use the Human Phenotype (HP) Ontology mappings for gene-to-phenotype and phenotype-to-genes. The HP annotations can be found here: [https://hpo.jax.org/app/data/annotations](https://hpo.jax.org/app/data/annotations). 
These data are generated by the HP group to use OMIM disease-gene associations to map all HP phenotypes to genes with those phenotypes associated with diseases.  Therefore, a gene can be associated with several phenotypes, and a phenotype can be associated with several genes.
- OMIM and Orphanet are combined together in the HPO database. 

**Preproccessing**:

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HGNCHPO.png" alt="drawing" width="800"/>

A Concept (blue), Code (purple) and Term (green) node from HPO (left side) and HGNC (right side) and the bidirectional relationships between the two Concept nodes.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HGNC'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HPO'})
return * limit 1
```

---
## Mouse gene-phenotype (HCOPMP)

**Source**:
- We ingested two datasets from the International Mouse Phenotype Consortium (**IMPC**) which contains data from the Knockout Mouse Phenotyping Program (**KOMP2**) at [http://ftp.ebi.ac.uk/pub/databases/impc/all-data-releases/latest/results/](http://ftp.ebi.ac.uk/pub/databases/impc/all-data-releases/latest/results/)
    - genotype-phenotype-assertions-ALL.csv
    - statistical-results-ALL.csv
- And three datasets from Mouse Genome Informatics (**MGI**) at [http://www.informatics.jax.org/downloads/reports/index.html#pheno](http://www.informatics.jax.org/downloads/reports/index.html#pheno)
    - MGI_PhenoGenoMP.rpt
    - MGI_GenePheno.rpt
    - MGI_Geno_DiseaseDO.rpt

**Preproccessing**:
Mouse genotype-to-phenotype (HCOPMP) data were obtained in January 2021 from multiple datasets from two separate databases. The first set of datasets were obtained from the international mouse phenotyping consortium (IMPC), which includes data from KOMP2, and can be found at http://ftp.ebi.ac.uk/pub/databases/impc/all-data-releases/latest/results/. We used the genotype-phenotype-assertions-ALL.csv.gz and the statistical-results-ALL.csv.gz datasets from this database. Both datasets contain, among other data, phenotype to gene mappings in the mouse. The second set of datasets were obtained from the mouse genome informatics (MGI) database and can be found at http://www.informatics.jax.org/downloads/reports/index.html#pheno. We used the MGI_PhenoGenoMP.rpt (Table 5),  MGI_GenePheno.rpt (Table 9) and MGI_Geno_DiseaseDO.rpt (Table 10) datasets. All 3 datasets contain, among other data, phenotype-to-gene mappings. The datasets from IMPC and MGI were combined to create a master genotype-to-phenotype dataset. This master dataset contains 10,380 MP terms that are mapped to at least one gene and 17,936 genes that are mapped to at least one MP term.
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HCOPMP.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HCOP'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MP'})
return * limit 1
```

---
## Human Phenotype Ontology (HPO) to Mouse Phenotype (MP) mappings (HPOMP)

**Source**:  The PheKnowLator tool,  [https://github.com/callahantiff/PheKnowLator](https://github.com/callahantiff/PheKnowLator) was used to map HPO terms to MP terms using semantic matching.


**Preproccessing**:  Matches were then manually curated.
data that connects HPO terms to MP terms was generated using the PheKnowLator tool in December 2020 [PheKnowLator citation.] Here we only map mouse to human phenotypes that are present in the Gabriella Miller Kids First (GMKF) datasets in this instance of Petagraph, to support the use cases in this study, but other mappings could be included at a later date. The mappings that PheKnowLator generated were then checked and edited manually for accuracy. We kept only the highest quality mappings which left us with ~1000 mappings. Mapping all HPO to MP terms is an ongoing project by the MONDO and uPheno projects [CITE]. 
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/HPOMP.png" alt="drawing" width="800"/>

A Concept (blue), Code (purple) and Term (green) from HPO on the left and its corresponding MP Concept, Code and Term on the right.

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HPO'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MP'})
return * limit 1
```

---
## Human-Rat ENSEMBL orthology (RATHCOP)

**Source**:

**Preproccessing**:

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/RATHCOP.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'ENSEMBL'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'ENSEMBL'})
where a.CODE contains 'ENSR'
return * limit 1
```

---
## GENCODE-HSCLO mappings (GENCODEHSCLO)

**Source**:
**Preproccessing**:
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/GENCODEHSCLO.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'GENCODE'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HSCLO'})
return * limit 1
```

---
### LINCS L1000 Gene-Perturbagen Associations (LINCS)

**Source**:
- LINCS L1000 Connectivity Map dataset was obtained from the Ma’ayan Lab Harmonizome portal:
- [https://maayanlab.cloud/Harmonizome/search?t=all&q=l1000](https://maayanlab.cloud/Harmonizome/search?t=all&q=l1000)
- Relationship SAB: `LINCS L1000`
- Relationship Name: `positively_correlated_with_chemical_or_drug`, `positively_correlated_with_gene`, `negatively_correlated_with_chemical_or_drug`, `negatively_correlated_with_gene`
    
**Preproccessing**:
We introduced gene-small molecule perturbagen relationships to the KG based on the LINCS L1000 [iii] edge list available on the Harmonizome database: https://maayanlab.cloud, (Duan et al. 2014; Rouillard et al. 2016) . These relationships were summarized from LINCS L1000 CMAP Signatures of Differentially Expressed Genes for Small Molecules dataset. This was done by first finding the corresponding CHEBI Concept nodes for the L1000 small molecules and then establishing the relationship of such nodes to the KG HGNC nodes according to the edge list mentioned above. For that purpose, the relationships were collapsed to exclude the cell line, dosage, and treatment time information but the effect directions were retained in relationship types. This led to 3,198,094 relationships (bidirectional) with “LINCS” as the SAB and types of “negatively_correlated_with_gene”, “positively_correlated_with_gene”, “inverse_negatively_correlated_with_gene” and “inverse_positively_correlated_with_gene”.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/LINCS.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'CHEBI'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'LINCS'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Connectivity Map (CMAP)

**Source**:
- Signature perturbations of gene expression profiles as induced by chemical (small molecule) were obtained from the Ma’ayan Lab Harmonizome portal:
- [https://maayanlab.cloud/Harmonizome/dataset/CMAP+Signatures+of+Differentially+Expressed+Genes+for+Small+Molecules](https://maayanlab.cloud/Harmonizome/dataset/CMAP+Signatures+of+Differentially+Expressed+Genes+for+Small+Molecules)
- Relationship SAB: `CMAP`
- Relationship Name: `positively_correlated_with_chemical_or_drug`, `positively_correlated_with_gene`, `negatively_correlated_with_chemical_or_drug`, `negatively_correlated_with_gene`
  
**Preproccessing**:  
In a similar manner to L1000 data integration discussed above, we obtained the edge lists of the CMAP Signatures of Differentially Expressed Genes for Small Molecules dataset from the Harmonizome database :https://maayanlab.cloud, (Lamb et al. 2006; Rouillard et al. 2016). The data was computed based on an earlier study (Lamb et al. 2006; Rouillard et al. 2016). The dataset added 2,625,336 new relationships (including reverse relationships) connecting the KG CHEBI and HGNC nodes with types types of “negatively_correlated_with_gene”, “positively_correlated_with_gene”, “inverse_negatively_correlated_with_gene” and “inverse_positively_correlated_with_gene” and SAB of “CMAP”.

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/CMAP.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'CHEBI'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'CMAP'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Homo Sapiens Chromosomal Ontology (HSCLO)

**Source**: The HSCLO was created by Taha Ahooyi Mohseni.

**Preproccessing**:  
Homo Sapiens Chromosomal Location Ontology (HSCLO) was primarily created to connect 4DN loop coordinates to the rest of the graph through the mapping between HSCLO and GENCODE. HSCLO was later utilized to connect GTEXEQTL locations in the graph as searchable nodes at 1 kbp resolution (same as 4DN). The dataset relationships as well as nodes use HSCLO as their SAB. HSCLO nodes are defined at 5 resolution levels; chromosomes, 1 Mbp, 100 kbp, 10 kbp and 1kbp with each level connects to lower level with above_(resolution level)_band (e.g. "above_1Mbp_band", "above 1_kbp_band") and nodes at the same resolution level are connected through prcedes_(resolution level)_band (e.g. "precedes_10kbp_band"). The dataset contains 3,431,155 nodes and 6,862,195 relationships (13,724,390 including reverse).

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HSCLO'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code)
MATCH (b)-[r3]-(c:Concept)-[:CODE]-(e:Code {SAB:'4DNL'})
MATCH  (b)-[r4]-(c2:Concept)-[:CODE]-(f:Code {SAB:'GTEXEQTL'})
MATCH  (b)-[r5]-(c3:Concept)-[:CODE]-(g:Code {SAB:'ENSEMBL'})
return * limit 1
```

---
## Molecular Signatures Database (MSIGDB) 

**Sourcee**: 
- MSigDB v7.4 datasets C1, C2, C3, C8 and H were obtained and ingested from the MSigDB molecular signature database:
- [https://www.gsea-msigdb.org/gsea/msigdb/](https://www.gsea-msigdb.org/gsea/msigdb/)
- Relationship SAB: `MSigDB C1`, `MSigDB C2`, `MSigDB C3`, `MSigDB C8`, `MSigDB H`
- Code SAB: `MSigDB_Systematic_Name`
- 
**Preproccessing**:  
MSigDB is a collection of gene set resources, curated or collected from several different sources (Subramanian et al. 2005; Liberzon et al. 2015). Five subsets of MSigDB v7.4 datasets were introduced as entity-gene relationships to the knowledge graph: C1 (positional gene sets), C2 (curated gene sets), C3 (regulatory target gene sets), C8 (cell type signature gene sets) and H (hallmark gene sets ). With this subset, we created MSIGDB Concept nodes for 31,516 MSigDB systematic names (used as Codes) through base64 encoding (Code SAB: MSIGDB). The relationships between these Concept nodes and HGNC nodes were established considering the information available in each of the mentioned 5 subsets where the subset information was included in the relationship SABs as “MSIGDB”. The Term names and SUIs were also compiled according to the MSigDB generic entity names and base64 conversion of such names, respectively. Collectively, MSigDB ingestion added 2,598,060 CUI-CUI relationships (including reverse relationships) to the KG. Table S2 summarizes the bidirectional relationship information for the MSigDB dataset integration. 
  
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/MSIGDB.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'HGNC'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MSIGDB'})
return * limit 1
```

---
## ClinVar (CLINVAR)

**Source**:
- ClinVar human genetic variant-disease associations were obtained from: [https://www.ncbi.nlm.nih.gov/clinvar/](https://www.ncbi.nlm.nih.gov/clinvar/)
- Only associations with Pathogenic and/or Likely Pathogenic consequence which met assertion criteria were included in the graph.
- Future versions of the KG will have the rest of the consequence levels.
- Relationship SAB: `CLINVAR`
- Relationship Name: `gene_associated_with_disease_or_phenotype`, `disease_or_phenotype_associated_with_gene`
**Preproccessing**:
The ClinVar human genetic variants-phenotype submission summary dataset (2023-01-05) was utilized to define relationships between human genes and phenotypes (Landrum et al. 2018). For that purpose Wwe only  considered included genes with pathogenic, likely pathogenic and pathogenic/likely pathogenic variants, and associations with no assertion criteria met were excluded. We also did not include variants that affect a subset of genes (where there was no one-to-one relationship between a gene and phenotype/disease). To retrieve the target phenotype/disease we used MEDGEN IDs listed in the ClinVar dataset (also already present in the KG). As a result, ClinVar gave rise to 214,040 new relationships (including reverse relationships) with the following characteristics [Type: “gene_associated_with_disease_or_phenotype”, SAB: “CLINVAR”] and [type: inverse_gene_associated_with_disease_or_phenotype, SAB: “CLINVAR”] connecting HGNC and MEDGEN, MONDO, HPO, EFO and MESH Concept nodes. The ClinVar website is hosted at https://www.ncbi.nlm.nih.gov/clinvar/. 
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/CLINVAR.png" alt="drawing" width="800"/>

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

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'AZ'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

---
## Protein - Protein Interactions (STRING)

**Source**: 
We used 9606.protein.links.full.v12.0 assertions obtained from STRING database and converted ENSP entries to UNIPROTKB and filtered the dataset for the top 10% of the combined score. The refined dataset contains 459,701 relationships (919,402 including reverse ones) that connects UNIPROTKB nodes with the relationship type: “interacts_with” and “inverse_interacts_with”, SAB: “STRING” and evidence_class denotes the combined score for the relationship.
**Preproccessing**: human only
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/STRING.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'UNIPROTKB'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'UNIPROTKB'})
return * limit 1
```

---
## Single Cell Fetal Heart expression data (ASP2019)

**Source**: 
Single cell Fetal heart data was obtained from Asp et al. 2019 https://pubmed.ncbi.nlm.nih.gov/31835037/ Average gene expression of each cluster was calculated and used to represent each gene within a cell type cluster. Single cell fetal heart concept nodes were created and connections to cell type nodes (author defined cell types, as many Cell Ontology concepts defined in paper are not currently part of the Cell Ontology) and HGNC nodes connections were made
**Preproccessing**: 
<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/SCHEART.png" alt="drawing" width="800"/>

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
**Preproccessing**: 

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/GLYGEN.png" alt="drawing" width="800"/>

```cypher
// Cypher query to reproduce the schema figure
match (a:Code {SAB:'GLY.TYPE.SITE'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'GLYTOUCAN'})
match (b)-[r3]-(e:Concept)-[:CODE]-(f:Code {SAB:'UNIPROTKB.ISOFORM'})
return * limit 1
```

---
## Gabriella Miller Kids First (KF) -- phenotypes and variants per gene

**Source**: 
Kids First phenotypes were added because we are specifically interested in evaluating patients in the Kids First database. We added phenotypes from 5,006 subjects, modeled as Concept nodes, and connected them to their respective HPO Concepts in the graph. As of 2022, we had access to phenotypes over 5,006 subject IDs. KFPheno_June2022_forKG.xlsx, represents 5,006 patient IDs

Data containing mappings from human genes to human phenotypes (HGNC-HPO) were obtained from https://ci.monarchinitiative.org/view/hpo/job/hpo.annotations/lastSuccessfulBuild/artifact/rare-diseases/util/annotation/phenotype_to_genes.txt. These data contain 4,545 genes mapped to at least one phenotype and 10,896 phenotypes mapped to at least one gene

Variant per Gene binning data

**Preproccessing**:   DONT FORGET ABOUT HIGH RISK VARIANTS

<img src="https://github.com/TaylorResearchLab/Petagraph/blob/main/figures/publication_figures/schema_figures/kf.png" alt="drawing" width="800"/>

The upper left Concept (blue) and Code (yellow) nodes represent a KF patient Concept and Code node, (SAB = KFPT). There are 5,329 KF Patient Concept and Code node pairs in  Petagraph. The KFPT Concept node is connected to one or more Human Phenotype Ontology (HPO) Concepts. The KFPT Concept node is also connected to its corresponding KF Cohort Concept and Code node (SAB = KFCOHORT) through a `belongs_to_cohort` relationship type. There are 15 distinct KF cohorts the graph. On the right, the KF gene bin Concept and Code node pair (SAB = KFGENEBIN) connect to the KFCOHORT Concept and an HGNC Concept. The KFGENEBIN Code node has a 'value' property which is the number of high risk and de novo variants for that gene for the patients in that cohort. 

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


