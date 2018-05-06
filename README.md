# ResetTwitterDB

## Description
* The purpose of **main.py** is to reset the DataBase (DB) Tables process status. The Tables in this DB are used to keep
track of data collection feature status of Twitter accounts interacting with Verified Media Personalities (VMPs). These 
Tables are ued for scalability and tasks redundancy elimination. For example, if a process has for task collecting HMTL 
pages profiles of an unordered list containing thousands of Twitter accounts, then adding similar **_n_** processes will 
reduce task completion time. However, since these processes are independent of each other a communication convention 
must exist among them to eliminate work redundancy or **_inefficiency_**. 

* Using the same example above, a process will check into the Table **profiles** to select an account which has a "**Not 
processed**" status. Once an account has been selected for processing its status in the Table will change accordingly.
Similar action will be taken after the account was processed. Below is the convention used for the status in all 
processing Tables.

```angular2html
0 - Not processed
1 - In process
2 - Process completed

```
* Since a process may be interrupted during a "**In Process**" execution task, it is possible that a small number of
accounts may have an "**In Process**" _status_ after all tasks were completed. This is the reason for which resetting
a DB Table may be required. Some tasks require finding all accounts with a "**Not Processed**" _status_. This another 
scenario where resetting a DB Table is needed.  


## Installation 

```
$ git clone https://github.com/phvargas/ResetTwitterDB.git
```

## Pre-requisites

* Python3
* PostgreSQL DB MUST be available. If DB is not available run included script:
```
$ ./CreateDB.sh
```

## Running
```angular2html
./main.py path=path-to-conversations db=database-name user=database-user &lt;followers_path=path-to-followers-folder>
```

## Parameters
* **path**: path to the file where all capture conversations are stored. The conversations will be uploaded into memory.
           The uploaded object will contain the handles that interacted in the conversations. This is a MANDATORY
           parameter.
           
* **db**: name of database in use
    
* **user**: user which has access to database.

* **friends_path**: path of folder where interacting Twitter accounts\' friends will be stored. This is not a MANDATORY 
                   parameter.
    
* **followers_path**: path of folder where interacting Twitter accounts\' followers will be stored. This is not a 
                    MANDATORY parameter.
                    
* **tweets_path**: path of folder where interacting Twitter accounts\' tweets will be stored. This is not a 


* **NOTE**: Although _friends_path_, _followers_path_, _tweets_path_, and _profiles_path_ are not **MANDATORY** 
parameters, at least one of them must be used.