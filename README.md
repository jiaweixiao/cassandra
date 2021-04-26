# Cassandra 
Cassandra is a key-value store database. It has 2 basic compoents, client and server. The server is a long run Java process, working as the database (DB). 
The client is a temporary Java process, used to submit DB request.

# Requirements
- Java (1.8 and higher. Cassandra 4.0 works with Java 11 and 12)
- And (1.8 and higer)
- Python (2.7 and higher)

# Build
cd Cassandra_dir

ant -Duse.jdk11=true

# Configuration
cd Cassandra_dir/conf
- cassandra-env.sh Configure the environments.
- cassandra.yaml Basic Cassandra configurations.
- jvm11-server.options Java options, for Java 11 and higer.

# Basic operations

/bin/cqlsh server_ip \
And then we can insert/delete/search data via DB command line.


# Run with YCSB
Yahoo! Cloud Serving Benchmark (YCSB) is a testcase for database. We can use it to submit lots of DB requests to test the throughput of the Cassandra.

## Server end

Launch the Cassandra server on the CPU server.

### Create keyspace for YCSB

```js
  # Connect to Cassandra
  # Assume the Cassandra server runs on 131.179.96.201
  cqlsh 131.179.96.201 9042
  
  # Create a keyspace with name ycsb
  create keyspace ycsb WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 3 };
```

### Create an in-memory usertable for YCSB

```js
cqlsh> USE ycsb;

cqlsh:ycsb> create table usertable ( y_id varchar primary key, field0 varchar, field1 varchar,field2 varchar,field3 varchar,field4 varchar,field5 varchar,field6 varchar,field7 varchar,field8 varchar,field9 varchar);

# Check the created usertable
cqlsh:ycsb> SELECT * FROM usertable;

 y_id | field0 | field1 | field2 | field3 | field4 | field5 | field6 | field7 | field8 | field9
------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------

```

## Client end

Run the request on another server. e.g., paso.
Download the binary version ycsb on client. 

### Load data for YCSB
Choose a workload from YCSB/workloads to run. The workload defines the DB commandlines, e.g., read/update/insert/delete. 
For memliner, we have some pre-defined workloads in repo, Benchmark/Cassandra/YCSB/workloads/.
Please use the pre-built SH in repo ShellScript/Memliner/Cassandra/.

```js
  # Assume the Cassandra server runs on 131.179.96.201
  # We are going to use the workload defiend in workloads/workloada
  bin/ycsb load cassandra-cql -p hosts="131.179.96.201" -s -P workloads/workloada
```

### Run YCSB

Do operations on the loaded data.
Please use the pre-built SH in repo ShellScript/Memliner/Cassandra/.

```js
  bin/ycsb run cassandra-cql -p hosts="131.179.96.201" -s -P workloads/workloada
```

# More details

## Add the Cassandra server into cgroup
Modify the sh

```js
# 1) Modify the start sh to add the server into a cgroup
cassandra/bin/cassandra

#############
# MemLiner control
############
ADD_INTO_CGROUP="cgexec  --sticky -g memory:memctl"

# 2) Set the $ADD_INTO_CGROUP to null to remove the cassandra server from cgroup


```






