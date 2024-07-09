# Instructions on how to build a Graph-RAG application using an LLM and Petagraph.

### We will use Pythons Langchain library for this application pipeline.

### The pipeline will consist of the following steps


1. First, aqcuire Petagraph and instantiate it on the cluster. The reformatting of the entire graph requires too much RAM to done on a local computer

2. Then, transform Petagraph by pushing relevant properties to the Concept nodes and then change the labels of any relevant nodes you need for your use case using Cypher. For example, if you want genes and phenotypes as part of your use case, you will need to set gene nodes to be type :Gene and phenotype nodes to be type :Phenotype.

3.  (a) Create a subgraph (should contain only Concept nodes) and then (b) Export this as a dump and then (c) Create a new neo4j database using this dump.

3a. Create a subgraph  


3b. Export subgraph as a dump  


3c. Create a new neo4j database using this dump  


4.  Install Ollama, which will power our LLM application.

5.  Start the Neo4j database and set constraints and indices via the `cypher-shell` or through a Python Neo4j API.
6.  Execute the rest of the code in the llm-integration jupyter notebook to set up a Graph-RAG application using the subgraph.

.......  
   


