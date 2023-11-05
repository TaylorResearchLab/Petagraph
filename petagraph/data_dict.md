

### Kids First
```cypher
match (c0:Code {SAB:'KFCOHORT'})-[r0:CODE]-(cui1:Concept)-[r1:belongs_to_cohort]-(cui2:Concept )-[r2:CODE]-(c1:Code {SAB:'KFPT'})
match (cui2)-[r3:has_phenotype]-(cui3:Concept)-[r4:CODE]-(c2:Code {SAB:'HPO'})
match (cui1)-[r5:belongs_to_cohort]-(cui4:Concept)-[r6:CODE]-(c3:Code {SAB:'KFGENEBIN'})
match (cui4)-[r7:gene_has_variants]-(cui5:Concept)-[r8:CODE]-(c4:Code {SAB:'HGNC'})
return * LIMIT 1
```


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
match (gtex_exp:Concept)-[r0]-(gtex_exp_code:Code) where gtex_exp_code.SAB = 'GTEXEQTL' 
match (gtex_exp)-[r1]-(hgnc_concept:Concept)-[r2]-(hgnc_code:Code {CodeID:'HGNC:52402'}) where hgnc_code.SAB = 'HGNC'
match (gtex_exp)-[r3:located_in]-(ub_concept:Concept)-[r4]-(ub_code:Code) where ub_code.SAB = 'UBERON'
match (gtex_exp)-[r5:p_value]-(exp_concept:Concept)-[r6]-(exp_code:Code) where exp_code.SAB = 'PVALUEBINS'  
match  (gtex_exp)-[r7]-(hsclo_concept:Concept)-[r8]-(hsclo_code:Code) where hsclo_code.SAB = 'HSCLO'  
return * limit 1
```


### GTEXCOEXP
```cyphermatch (hgnc1:Code)-[r0:CODE]-(hgnc_concept1:Concept)-[r1]-(hgnc_concept2:Concept)-[r2:CODE]-(hgnc2:Code {SAB:'HGNC'})
where type(r1) starts with 'coexpressed_with'
return * limit 1
```


### Human-Mouse Orthologs (HGNCHCOP)
```cypher
match (hgnc1:Code {SAB:'HCOP'})-[r0:CODE]-(hgnc_concept1:Concept)-[r1]-(hgnc_concept2:Concept)-[r2:CODE]-(hgnc2:Code {SAB:'HGNC'})
return * limit 1
```
### Human gene-phenotype (HGNCHPO)
```cypher
match (hgnc1:Code {SAB:'HGNC'})-[r0:CODE]-(hgnc_concept1:Concept)-[r1]-(hgnc_concept2:Concept)-[r2:CODE]-(hgnc2:Code {SAB:'HPO'})
return * limit 1
```

### Mouse gene-phenotype (HCOPMP)

```cypher
match (hgnc1:Code {SAB:'HCOP'})-[r0:CODE]-(hgnc_concept1:Concept)-[r1]-(hgnc_concept2:Concept)-[r2:CODE]-(hgnc2:Code {SAB:'MP'})
return * limit 1
```

### Human-Mouse Phenotype mappings (HPOMP)
```cypher
match (hgnc1:Code {SAB:'HPO'})-[r0:CODE]-(hgnc_concept1:Concept)-[r1]-(hgnc_concept2:Concept)-[r2:CODE]-(hgnc2:Code {SAB:'MP'})
return * limit 1
```


### Human-Rat ENSEMBL orthology (RATHCOP)

```cypher
match (hgnc1:Code {SAB:'ENSEMBL'})-[r0:CODE]-(hgnc_concept1:Concept)-[r1]-(hgnc_concept2:Concept)-[r2:CODE]-(hgnc2:Code {SAB:'ENSEMBL'})
where hgnc1.CODE contains 'ENSR'
return * limit 1
```


