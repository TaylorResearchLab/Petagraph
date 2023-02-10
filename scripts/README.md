## Cypher queries to produce graph figures for "Petagraph: A large-scale unifying knowledge graph framework for integrating biomolecular and biomedical data"
#### Python and R Code to produce non-cypher Figures can be found [here](https://github.com/TaylorResearchLab/Petagraph/tree/main/scripts/code)

##### Figure 1. Example of the Concept-Code-Term schema
```
MATCH (c:Concept)-[:CODE]-(s:Code {CODE:'HGNC:11998'})-[r]-(t:Term)
RETURN * 
```

#### Figure 2. Petagraph Data Ingestion Workflow. 
- Figure 2 was made using an online workflow tool called [Canva](https://www.canva.com)


