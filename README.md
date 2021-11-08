# Cassandra

Cassandra is a key-value store database. It has 2 basic compoents, client and server. The server is a long run Java process, working as the database (DB).
The client is a temporary Java process, used to submit DB request.

Before start reading this script, change `131.x.x.201` into your Cassandra server's IP address.

# Requirements
- Java (1.8 and higher. Cassandra 4.0 works with Java 11 and 12)
- And (1.8 and higer)
- Python (2.7 and higher)

# Build

```bash
cd Cassandra_dir
sudo yum install ant ant-junit java-11-openjdk-devel
```

add following lines to ~/.bashrc:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export JRE_HOME=/usr/lib/jvm/java-11-openjdk/jre
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
```

Restart shell to apply changes.

Build Cassandras

```bash
cd cassandra
ant -Duse.jdk11=true
```

reference: [Support for Java 11](https://cassandra.staged.apache.org/doc/latest/cassandra/new/java11.html)

# Configuration

`cd cassandra/conf`

## IP of Cassandra server

Assuming using ip 131.x.x.201 as server, change the following arguments in `cassandra.yaml`:

```conf
# 1. seeds
seeds: "131.x.x.201:7000"

# 2. listen_address
listen_address: 131.x.x.201

# 3. rpc_address
rpc_address: 131.x.x.201
```

## Java Options

When using JDK11 or above, config java options in `jvm11-server.options`.

For Mako or Shenandoah GC, a template configuration is provided in `jvm11-server-shenandoah.options`.

`diff jvm11-server.options jvm11-server-shenandoah.options` for changes.

To modify GC log options, search `JVM_OPTS="$JVM_OPTS -Xlog:gc=info,heap*=trace,age*=debug,safepoint=info,promotion*=trace:file=${CASSANDRA_LOG_DIR}/gc.log:time,uptime,pid,tid,level:filecount=10,filesize=10485760"` and modify in `cassandra-env.sh`.

## bash variables config

add following lines to ~/.bashrc (Replace `jdk_home_directory` and `cassandra_home_directory`):

```bash
export JAVA_HOME=`jdk_home_directory`
export JAVA=`jdk_home_directory`/bin/java
export PATH=$PATH:$JAVA_HOME/bin
# cassandra
export PATH=$PATH:`cassandra_home_directory`/bin
```

Restart shell to apply changes.

# Basic operations

## Launch the DB server

(maybe not necessary) add this line at the start of `cassandra`

```bash
# It is recommended to launch the server in a tmux session.
# To ensure server is using the intended JVM, `echo $JAVA_HOME` to check before running
# You may need to modify ~/.bash_profile to apply changes in `~/.bashrc` to tmux shell
# ref: [New tmux sessions do not source bashrc file](https://unix.stackexchange.com/questions/320465/new-tmux-sessions-do-not-source-bashrc-file)
cassandra
```

## Operations

And then we can insert/delete/search data via DB command line.
Assume the server ip is 131.x.x.201
```bash
cqlsh 131.x.x.201
```

## Stop the DB server

```bash
stop-server
```

## Delete all database data

```bash
rm -rf ~/cassandra/data
```

# Run with YCSB
Yahoo! Cloud Serving Benchmark (YCSB) is a testcase for database. We can use it to submit lots of DB requests to test the throughput of the Cassandra.

## Server end

Launch the Cassandra server on the CPU server.

### Use a script to set up

```bash
cd ${HOME}
# ask Shi for permission
git clone https://github.com/FereX98/scripts-repo.git
cqlsh 131.x.x.201 9042 --file $HOME/scripts-repo/cassandra/ycsb.cql
```

### Setting up manually

#### Create keyspace for YCSB

```js
  # Connect to Cassandra
  # Assume the Cassandra server runs on 131.x.x.201
  cqlsh 131.x.x.201 9042

  # Create a keyspace with name ycsb
  create keyspace ycsb WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 3 };
```

#### Create an in-memory usertable for YCSB

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
  # Assume the Cassandra server runs on 131.x.x.201
  # We are going to use the workload defined in workloads/workloada
  bin/ycsb load cassandra-cql -p hosts="131.x.x.201" -s -P workloads/workloada
```

Use DB command line to check if the data is loaded into memtable correctly.

```js
# use cqlsh terminal
# 1. choose keyspace
use ycsb;

# 2. Show current tables
desc tables;

# 3. Check the number of rows of a table. Assume the table name is usrtable.
select count(*) from usertable;

# Results
# If the table is too large, this will run a while
 count
----------
 10000000

```


### Run YCSB

Do operations on the loaded data.
Please use the pre-built SH in repo ShellScript/Memliner/Cassandra/.

```js
  bin/ycsb run cassandra-cql -p hosts="131.x.x.201" -s -P workloads/workloada
```

Some arguments in the workload file, such as number of threads and number of records and operations can be overwritten by command options. Learn more in Chenxi's scripts:

The pre-defined workloads are in the repo, Benchmark/Cassandra/YCSB/workloads/

The pre-defiend shellscripts are in the repo, ShellScript/Memliner/Cassandra/

```bash
cd ~
# ask Chenxi for permissions
git clone https://github.com/wangchenxi7/Benchmark.git
git clone https://github.com/wangchenxi7/ShellScript.git

cp Benchmark/Cassandra/YCSB/workloads/workloadMemLiner* ycsb-0.17.0/workloads/
mkdir Logs

# edit arguments before running, mainly `host_ip`, `records`, `tag`, `workload`.
# It is racommended to change `records` to 1000000, for a faster test.
${HOME}/ShellScript/Memliner/Cassandra/optimal_ycsb_control.sh load
${HOME}/ShellScript/Memliner/Cassandra/optimal_ycsb_control.sh run
# When running with remote memory, do not forget to set cgroup ON SERVER
sudo cgcreate -t $USER -a $USER -g memory:/memctl
echo 9g > /sys/fs/cgroup/memory/memctl/memory.limit_in_bytes
```

### Run YCSB with Server Remote Control

It is possible to run several benchmarks autmatically by controlling Cassandra server via ssh on the client.

See Shi's script for more information:

```bash
# ask Shi for permission
git clone https://github.com/FereX98/scripts-repo.git
cd scripts-repo/cassandra
# There are problems about the start option in the script.
# Instead, please use the following commands on the server to start the server.
# ./manage_server.sh start
cassandra
# wait for the server to be ready, usually takes about 60 ~ 80 seconds
sleep 100
cqlsh 131.x.x.201 9042 --file ${HOME}/scripts-repo/cassandra/ycsb.cql

./manage_server.sh stop
./manage_server.sh limit 5g
# $tag is the prefix in the client-side log file, see ycsb_control.sh for more information
# $workload is the name of the workload files.
# For Mako, `workloadMemLinerInsertIntensive` and `workloadMemLinerUpdateInsert` are used for now.
./manage_server.sh load $tag $workload
./manage_server.sh run  $tag $workload
# e.g.
./manage_server.sh load 13-II workloadMemLinerInsertIntensive
./manage_server.sh run 13-UInsert workloadMemLinerUpdateInsert
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

## Cassandra disabled swapping by pretouching and pinning the Java heap in memory
We need to modify the source code of cassandra to disable the Java heap pinning mechanism. Check the commit for more details.

## Running several benchmarks with one server launch

Under the same Cassandra config and local ratio, running several benchmarks with one server launch and the order running them do not have a significant impact on the performance.

But impact of changing local cache ratio without restarting the server is untested. Every time the Cassandra config or local ratio is changed, it is recommended to stop the server, delete database data, restart the server and recreate the usertable, to ensure correct measurement of performance.

## GC pause calculation

To calcluate GC pause for each run of a benchmark, extract GC logs during the period of the benchmark run from the server log file: `${cassandra_home}/logs/gc.log`. Then use a script to add up all pause time.

The script to use depends on your GC and GC log option. For logs using the default Shenandoah GC log options (defined in `${cassandra_home}/conf/cassandra-env.sh`), you can use `${cassandra_home}/tools/pick_log.py` to extract GC log messages of a period of time; Use `${cassandra_home}/tools/pause.py` to calculate the GC pause time.
