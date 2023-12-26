# Instructions on how to launch and query Petagraph on the Taylor server


#### 1. ssh into the server: 
`$ ssh RESLNTAYLORD01.research.chop.edu`
#### 2. start the database:
This will start the database in the console. This allows you to see the status and updated logs of the running dataabase right in the terminal.
`$ neo4j-admin server console`
#### 3. open a new terminal and ssh into the server again, and show that the database is running:
`$ neo4j-admin server status`

output should look like this: `Neo4j is running at pid 2514457`.
You can now invoke the `cypher-shell` tool by doing `$ cypher-shell` and enter cypher statements in the terminal. 
Remember to end cypher statements with a semicolon. Type `:exit` to exit the `cypher-shell`.

#### 4. If you want to launch a jupyter notebook or r studio notebook you can just use regular port forwarding method by doing the following:
4a. Do `jupyter lab --no-browser --port=8890` on the Taylor server. Don't use port 7474 b/c thats the default for the neo4j database.  
4b. Do `ssh -N -f -L localhost:8890:localhost:8890 RESLNTAYLORD01.research.chop.edu` from a local terminal. If there are no errors it shoud've worked.  
4c. Copy the URL that the `jupyter lab --no-browser --port=8890` command gave and paste it into a browser window. It should open a jupyter lab page. Now you can use Python/R neo4j plugins to interact with the database  
In Python you can do:

```
NEO4J_URI='bolt://localhost:7687'
NEO4J_USER='neo4j'
NEO4J_PASSWORD='neo4j'
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
```
