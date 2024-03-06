# Instructions on how to launch and query Petagraph on the Taylor server


#### (Optional) Prerequisites
a.) Set up ssh keys for password free login
b.) Install pip on server
c.) Use virtualenv to create a virtural environment and install python3.11


Install packages: jupyter, graphdatascience, neo4j, 


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

#### 5. Activate virtual environment so you can use a newer version of Python in jupyter lab
The default Python is python3.6, but neo4js python graph data science plugin `graphdatascience==1.8` needs a newer version of python.
To use a newer version of Python follow these steps:  
5a. Use method 2 from https://tecadmin.net/how-to-install-python-3-11-on-ubuntu/ to d/l Python and PIP...
```
sudo wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz;
sudo tar xzf Python-3.11.3.tgz;
cd Python-3.11.3 ;
sudo ./configure --enable-optimizations;
sudo make altinstall ;
python3.11 -V ;
```

```
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11;
pip3.11 -V
```

5b. Create venv to create new kernel https://saturncloud.io/blog/how-to-add-a-python-3-kernel-to-jupyter-ipython/#step-3-install-the-ipython-kernel-package  
5c.
#export PATH="/usr/local/lib/python3.11:$PATH"  
#export PATH="/usr/local/lib/python3.11/site-packages:$PATH"  
sudo python3.11 -m pip show graphdatascience  
