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
