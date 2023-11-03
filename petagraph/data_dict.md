

### Kids First
```cypher
match (c0:Code {SAB:'KFCOHORT'})-[r0:CODE]-(cui1:Concept)-[r1:belongs_to_cohort]-(cui2:Concept )-[r2:CODE]-(c1:Code {SAB:'KFPT'})
match (cui2)-[r3:has_phenotype]-(cui3:Concept)-[r4:CODE]-(c2:Code {SAB:'HPO'})
match (cui1)-[r5:belongs_to_cohort]-(cui4:Concept)-[r6:CODE]-(c3:Code {SAB:'KFGENEBIN'})
match (cui4)-[r7:gene_has_variants]-(cui5:Concept)-[r8:CODE]-(c4:Code {SAB:'HGNC'})
return * LIMIT 1
```
