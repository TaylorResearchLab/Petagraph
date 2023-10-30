

## figure 7a
```cypher
match (asd:Concept)-[:CODE]-(asd_code:Code{SAB:'MP'} ) // {CodeID:'MP:0010403'}
match (asd)-[:involved_in]-(hcop:Concept)-[:CODE]-(hcop_code:Code {SAB:'HCOP'}) // {CodeID:'HCOP:Crebbp'}
match (hcop)-[r]-(hgnc:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})
match (hgnc)-[:located_in]-(gtexeqtl:Concept)-[:CODE]-(eqtl_code:Code {SAB:'GTEXEQTL'})
match (gtexeqtl)-[:p_value]-(pvalue:Concept)-[:CODE]-(pval_code:Code {SAB:'PVALUEBINS'})
RETURN * LIMIT 1
```



## fig?
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
first part
```cypher
match (asd:Concept)-[:CODE]-(asd_code:Code {CodeID:'MP:0010403'})
match (asd)-[:isa]-(opsd:Concept)-[:CODE]-(opsd_code:Code {CodeID:'MP:0010404'})
match (opsd)-[:involved_in]-(hcop:Concept)-[:CODE]-(hcop_code:Code {SAB:'HCOP'})
match (hcop)-[r]-(hgnc:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})-[:MTH_ACR]-(T:Term {name:'FLNC gene'})
RETURN * LIMIT 1
```
