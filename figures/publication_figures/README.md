






```cypher
match (m:Concept)-[:CODE]-(l:Code {SAB:'HPO'})
match (m)-[r:is_approximately_equivalent_to]-(n:Concept)-[:CODE]-(mp:Code {SAB:'MP'})
match (n)-[r2]-(o:Concept)-[:CODE]-(hcop_code:Code {SAB:'HCOP'})
match (o)-[r3]-(p:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})
match (p)-[r4]-(q:Concept)-[:CODE]-(eqtl:Code {SAB:'GTEXEQTL'})
RETURN * LIMIT 1
```


## remake of figure 10 (w/o) RO codes as edge names
## whats up w/ the cl-log2fcbins relationship?
```cypher
match (asd:Concept)-[:CODE]-(asd_code:Code {SAB:'MP'})//,CodeID:'MP:0010403'})
match (asd)-[:isa]-(opsd:Concept)-[:CODE]-(opsd_code:Code {SAB:'HPO'})//CodeID:'MP:0010404'})//-[r0]-(pt:Term) where pt.name contains 'Flna'
match (opsd)-[:involved_in]-(hcop:Concept)-[:CODE]-(hcop_code:Code {SAB:'HCOP'})
match (hcop)-[r]-(hgnc:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})//-[]-(T:Term)
match (hgnc)-[r1 {SAB:'HMAZ'}]-(cl:Concept)-[:CODE]-(cl_code:Code {SAB:'CL'})
 match (cl)-[r2]-(c:Concept)-[:CODE]-(cc:Code {SAB:'LOG2FCBINS'})
RETURN * LIMIT 1
```
