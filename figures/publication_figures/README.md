






```cypher
match (m:Concept)-[:CODE]-(l:Code {SAB:'HPO'})
match (m)-[r:is_approximately_equivalent_to]-(n:Concept)-[:CODE]-(mp:Code {SAB:'MP'})
match (n)-[r2]-(o:Concept)-[:CODE]-(hcop_code:Code {SAB:'HCOP'})
match (o)-[r3]-(p:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})
match (p)-[r4]-(q:Concept)-[:CODE]-(eqtl:Code {SAB:'GTEXEQTL'})
RETURN * LIMIT 1
```
