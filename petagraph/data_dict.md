

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
match (gtex_exp)-[r1:located_in]-(hgnc_concept:Concept)-[r2]-(hgnc_code:Code) where hgnc_code.SAB = 'HGNC'
match (gtex_exp)-[r3:located_in]-(ub_concept:Concept)-[r4]-(ub_code:Code) where ub_code.SAB = 'UBERON'
match (gtex_exp)-[r5:p_value]-(exp_concept:Concept)-[r6]-(exp_code:Code) where exp_code.SAB = 'PVALUEBINS'  
return * limit 1
```
