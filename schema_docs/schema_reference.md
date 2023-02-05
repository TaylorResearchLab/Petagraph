# Data Source Descriptions and Schema Reference

### ****Genotype-Tissue Expression (GTEx) Portal****

- We ingested two datasets from ****[https://gtexportal.org/home/datasets](https://gtexportal.org/home/datasets):**
    - GTEx_Analysis_v8_eQTL (all files in this directory)
    - GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct
    
    Code SABs: Gene (HGNC), Tissue (UBERON). The GTEx gene expression SABs are currently just [GTEx - Gene - Tissue - Expression] (SABs for GTEx gene expression names will be changed in the next version to just gene-tissue-GTEx_version)
    
    Expression schema:
    
    ![Human gene concept  (HGNC code), linked by expression to the GTEX expression value (green term) linked to the tissue (Uberon code)](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/GTEx_expression.png)
    
    Human gene concept  (HGNC code), linked by expression to the GTEX expression value (green term) linked to the tissue (Uberon code)
    

eQTL schema:

![An UBERON Concept, Code and Term (top left), an HGNC Concept and preferred Term (top right) and GTEx eQTL Concept, Code and Terms (center). The GTEx Terms shown here represent a binned  p-value and variant ID for the eQTL](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/GTEx_eQTL.png)

An UBERON Concept, Code and Term (top left), an HGNC Concept and preferred Term (top right) and GTEx eQTL Concept, Code and Terms (center). The GTEx Terms shown here represent a binned  p-value and variant ID for the eQTL

### Human BioMolecular Atlas Program (HuBMAP)

- We ingested 61 10X V3 single-cell/nuclei RNAseq datasets which can be found at [https://portal.hubmapconsortium.org/search?mapped_data_types[0]=snRNA-seq (10x Genomics v3)&mapped_data_types[1]=scRNA-seq (10x Genomics v3)&entity_type[0]=Dataset](https://portal.hubmapconsortium.org/search?mapped_data_types%5B0%5D=snRNA-seq%20%2810x%20Genomics%20v3%29&mapped_data_types%5B1%5D=scRNA-seq%20%2810x%20Genomics%20v3%29&entity_type%5B0%5D=Dataset)

HuBMAP data schema example:

![From left to right (Concepts are orange): A tissue Concept (could be UBERON, FMA or SNOMED) , HuBMAP dataset Concept, HuBMAP cluster Concept (most datasets have between 10 and 20 clusters), HuBMAP expression Concept and a HGNC Concept.](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/hubmap.png)

From left to right (Concepts are orange): A tissue Concept (could be UBERON, FMA or SNOMED) , HuBMAP dataset Concept, HuBMAP cluster Concept (most datasets have between 10 and 20 clusters), HuBMAP expression Concept and a HGNC Concept.

### Human-Mouse gene Orthologs

- Orthologs from HGNC Comparisons of Orthology Predictions (**HCOP**) [https://www.genenames.org/tools/hcop/](https://www.genenames.org/tools/hcop/) (scroll to the bottom, under Bulk Downloads. Select Human - Mouse ortholog data)

Schema and query example for HGNC-HCOP mouse

![HGNC Concept (blue), Code (purple) and Term (green) from HGNC on the left and its corresponding Mouse gene Concept and code on the right  ](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/HGNC_HCOP.png)

HGNC Concept (blue), Code (purple) and Term (green) from HGNC on the left and its corresponding Mouse gene Concept and code on the right  

### ****Mammalian Phenotype Ontology (MP)****

- We ingested the latest release of MP which can be found at [https://bioportal.bioontology.org/ontologies/MP](https://bioportal.bioontology.org/ontologies/MP)

See schema below for MP-HPO mappings for more.

### Mouse Gene - Phenotype mappings

- We ingested two datasets from the International Mouse Phenotype Consortium (**IMPC**) which contains data from the Knockout Mouse Phenotyping Program (**KOMP2**) at [http://ftp.ebi.ac.uk/pub/databases/impc/all-data-releases/latest/results/](http://ftp.ebi.ac.uk/pub/databases/impc/all-data-releases/latest/results/)
    - genotype-phenotype-assertions-ALL.csv
    - statistical-results-ALL.csv
- And three datasets from Mouse Genome Informatics (**MGI**) at [http://www.informatics.jax.org/downloads/reports/index.html#pheno](http://www.informatics.jax.org/downloads/reports/index.html#pheno)
    - MGI_PhenoGenoMP.rpt
    - MGI_GenePheno.rpt
    - MGI_Geno_DiseaseDO.rpt
    
    (Same schema as Human Gene-Phenotype mappings below)
    

### Human Gene - Phenotype mappings

- OMIM and Orphanet are combined together. In the future we will be separating out HPO-to-gene sources.

![A Concept (blue), Code (purple) and Term (green) node from HPO (left side) and HGNC (right side) and the bidirectional relationships between the two Concept nodes.](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/HPO_HGNC.png)

A Concept (blue), Code (purple) and Term (green) node from HPO (left side) and HGNC (right side) and the bidirectional relationships between the two Concept nodes.

### HPO - MP mapping

- The PheKnowLator tool,  [https://github.com/callahantiff/PheKnowLator](https://github.com/callahantiff/PheKnowLator) was used to map HPO terms to MP terms using semantic matching. Matches were then manually curated.
- Schema for MP← → HPO mappings:

![A Concept (blue), Code (purple) and Term (green) from HPO on the left and its corresponding MP Concept, Code and Term on the right.](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/HPO_MP.png)

A Concept (blue), Code (purple) and Term (green) from HPO on the left and its corresponding MP Concept, Code and Term on the right.

### HGNC annotation data

- ****[http://genome.ucsc.edu/cgi-bin/hgTables](http://genome.ucsc.edu/cgi-bin/hgTables) (exact dataset will be available in the future)**

### ClinVar

- ClinVar human genetic variant-disease associations were obtained from: [https://www.ncbi.nlm.nih.gov/clinvar/](https://www.ncbi.nlm.nih.gov/clinvar/)
- Only associations with Pathogenic and/or Likely Pathogenic consequence which met assertion criteria were included in the graph.
- Future versions of the KG will have the rest of the consequence levels.
- Relationship SAB: **ClinVar**
- Relationship Name: **gene_associated_with_disease_or_phenotype, disease_or_phenotype_associated_with_gene**

![graph-5.png](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/graph-5.png)

### Connectivity Map (CMAP)

- Signature perturbations of gene expression profiles as induced by chemical (small molecule) were obtained from the Ma’ayan Lab Harmonizome portal:
- [https://maayanlab.cloud/Harmonizome/dataset/CMAP+Signatures+of+Differentially+Expressed+Genes+for+Small+Molecules](https://maayanlab.cloud/Harmonizome/dataset/CMAP+Signatures+of+Differentially+Expressed+Genes+for+Small+Molecules)
- Relationship SAB: **CMAP**
- Relationship Name: **positively_correlated_with_chemical_or_drug, positively_correlated_with_gene, negatively_correlated_with_chemical_or_drug, negatively_correlated_with_gene**

![graph-3.png](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/graph-3.png)

### LINCS L1000 Gene-Perturbagen Associations

- LINCS L1000 Connectivity Map dataset was obtained from the Ma’ayan Lab Harmonizome portal:
- [https://maayanlab.cloud/Harmonizome/search?t=all&q=l1000](https://maayanlab.cloud/Harmonizome/search?t=all&q=l1000)
- Relationship SAB: **LINCS L1000**
- Relationship Name: **positively_correlated_with_chemical_or_drug, positively_correlated_with_gene, negatively_correlated_with_chemical_or_drug, negatively_correlated_with_gene**
    
    ![graph-4.png](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/graph-4.png)
    

### UniProtKB Gene-Protein Associations

- The ingested human gene-protein associations data was obtained from the Glygen project portal:
- [https://data.glygen.org/GLY_000001](https://data.glygen.org/GLY_000001)

Schema is included with the Glygen schema on left side of diagram.

### Protein Glycosylation

- Information on human protein glycosylation types/sites and the associated glycans were obtained and ingested from the Glygen project portal:
- [https://data.glygen.org](https://data.glygen.org/)

![Untitled](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/Untitled.png)

### GTEx Gene Co-Expression

- Co-expression of genes were computed using Pearson’s correlation > 0.9 in 37 human tissues according to the GTEx expression data:
- GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct
- Relationship Name: **coexpressed_with**
- Tissue where the co-expression is detected is in the SAB of the relationship  “coexpressed_with”
    
    ![graph-2.png](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/graph-2.png)
    

### MSigDB

- MSigDB v7.4 datasets C1, C2, C3, C8 and H were obtained and ingested from the MSigDB molecular signature database:
- [https://www.gsea-msigdb.org/gsea/msigdb/](https://www.gsea-msigdb.org/gsea/msigdb/)
- Relationship SAB: **MSigDB C1, MSigDB C2, MSigDB C3, MSigDB C8, MSigDB H**
- Code SAB: **MSigDB_Systematic_Name**

![graph.png](https://github.com/TaylorResearchLab/CFDIKG/blob/master/Tutorials/CFDE_Hackathons/schema_images/graph.png)
