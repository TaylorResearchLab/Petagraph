

# Data Dictionary

### GTEXEXP
```cypher
match (gtex_exp:Concept)-[:CODE]-(gtex_exp_code:Code {SAB:'GTEXEXP' })
match (gtex_exp)-[r1:expressed_in {SAB:'GTEXEXP'}]->(hgnc_concept:Concept)-[r2:CODE]-(hgnc_code:Code {SAB:'HGNC'}), (hgnc_concept)-[pt:PREF_TERM]-(t:Term)
match (gtex_exp)-[r3:expressed_in {SAB:"GTEXEXP"}]-(ub_concept:Concept)-[r4:CODE]-(ub_code:Code {SAB:'UBERON'}), (ub_concept)-[pt2:PREF_TERM]-(t2:Term)
match (gtex_exp)-[r5:has_expression]->(exp_concept:Concept)-[r6:CODE]-(exp_code:Code {SAB: 'EXPBINS' })
return * limit 1
```

### GTEXEQTL
```cypher
match (gtex_eqtl:Concept)-[r0]-(gtex_eqtl_code:Code) where gtex_eqtl_code.SAB = 'GTEXEQTL' 
match (gtex_eqtl)-[r1]-(hgnc_concept:Concept)-[r2]-(hgnc_code:Code {CodeID:'HGNC:52402'}) where hgnc_code.SAB = 'HGNC'
match (gtex_eqtl)-[r3:located_in]-(ub_concept:Concept)-[r4]-(ub_code:Code) where ub_code.SAB = 'UBERON'
match (gtex_eqtl)-[r5:p_value]-(exp_concept:Concept)-[r6]-(exp_code:Code) where exp_code.SAB = 'PVALUEBINS'  
match  (gtex_eqtl)-[r7]-(hsclo_concept:Concept)-[r8]-(hsclo_code:Code) where hsclo_code.SAB = 'HSCLO'  
return * limit 1
```


### GTEXCOEXP
```cypher
match (a:Code)-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
where type(r1) starts with 'coexpressed_with'
return * limit 1
```


### Human-Mouse Orthologs (HGNCHCOP)
```cypher
match (a:Code {SAB:'HCOP'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```
### Human gene-phenotype (HGNCHPO)
```cypher
match (a:Code {SAB:'HGNC'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HPO'})
return * limit 1
```

### Mouse gene-phenotype (HCOPMP)

```cypher
match (a:Code {SAB:'HCOP'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MP'})
return * limit 1
```

### Human-Mouse Phenotype mappings (HPOMP)
```cypher
match (a:Code {SAB:'HPO'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MP'})
return * limit 1
```


### Human-Rat ENSEMBL orthology (RATHCOP)
```cypher
match (a:Code {SAB:'ENSEMBL'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'ENSEMBL'})
where a.CODE contains 'ENSR'
return * limit 1
```

### GENCODE-HSCLO
```cypher
match (a:Code {SAB:'GENCODE'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HSCLO'})
return * limit 1
```

### LINCS
```cypher
match (a:Code {SAB:'CHEBI'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'LINCS'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

### CMAP
```cypher
match (a:Code {SAB:'CHEBI'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'CMAP'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```


### HSCLO
```cypher
match (a:Code {SAB:'HSCLO'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code)
MATCH (b)-[r3]-(c:Concept)-[:CODE]-(e:Code {SAB:'4DNL'})
MATCH  (b)-[r4]-(c2:Concept)-[:CODE]-(f:Code {SAB:'GTEXEQTL'})
MATCH  (b)-[r5]-(c3:Concept)-[:CODE]-(g:Code {SAB:'ENSEMBL'})
return * limit 1
```

### MSIGDB
```cypher
match (a:Code {SAB:'HGNC'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'MSIGDB'})
return * limit 1
```

### CLINVAR
```cypher
match (a:Code {SAB:'UBERON'})-[r0:CODE]-(b:Concept)-[r1 {SAB:'CLINVAR'}]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```
### AZ
```cypher
match (a:Code {SAB:'AZ'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
return * limit 1
```

### STRING 
```cypher
match (a:Code {SAB:'UNIPROTKB'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'UNIPROTKB'})
return * limit 1
```

### Single Cell Heart expression data
```cypher
match (a:Code {SAB:'ASP2019'})-[r0:CODE]-(b:Concept)-[r1:expressed_in]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'HGNC'})
match (b)-[:expressed_in]-(e:Concept)-[:CODE]-(f:Code {SAB:'ASP2019CLUSTER'})
match (b)-[:log2FC]-(g:Concept)-[:CODE]-(h:Code {SAB:'LOG2FCBINS'})
return * limit 1
```

### GLYGEN (selected datasets)
```cypher
match (a:Code {SAB:'GLY.TYPE.SITE'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'GLYTOUCAN'})
match (b)-[r3]-(e:Concept)-[:CODE]-(f:Code {SAB:'UNIPROTKB.ISOFORM'})
return * limit 1
```

### Kids First
```cypher
match (c0:Code {SAB:'KFCOHORT'})-[r0:CODE]-(cui1:Concept)-[r1:belongs_to_cohort]-(cui2:Concept )-[r2:CODE]-(c1:Code {SAB:'KFPT'})
match (cui2)-[r3:has_phenotype]-(cui3:Concept)-[r4:CODE]-(c2:Code {SAB:'HPO'})
match (cui1)-[r5:belongs_to_cohort]-(cui4:Concept)-[r6:CODE]-(c3:Code {SAB:'KFGENEBIN'})
match (cui4)-[r7:gene_has_variants]-(cui5:Concept)-[r8:CODE]-(c4:Code {SAB:'HGNC'})
return * LIMIT 1
```

### 4DN
```cypher
match (a:Code {SAB:'4DNF'})-[r0:CODE]-(b:Concept)-[r1]-(c:Concept)-[r2:CODE]-(d:Code {SAB:'4DNL'})
match (b)-[r3]-(e:Concept)-[:CODE]-(f:Code {SAB:'4DND'})
match (c)-[:loop_ds_end]-(g:Concept)-[:CODE]-(h:Code {SAB:'HSCLO'})
match (c)-[r4]-(i:Concept)-[:CODE]-(j:Code {SAB:'4DNQ'})
//match (j)-[r5]-(k:Concept)-[:CODE]-(l:Code {SAB:'UBERON'})
return * limit 1
```

