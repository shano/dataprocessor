# Data Processor

Multi-process script that takes in a folder of csv files, a glob query and database connection.

## Dependencies

### If using mysql on ubuntu

```bash
sudo apt-get install python3-pip python3-dev libmysqlclient-dev
```

Sorry about needing the -dev requirements, wanted to dockerise it...

## Usage

```bash
export SRC_DATA_FOLDER='/path/to/data'
export SRC_FILE_NAME='certificates.csv'
export DEST_SQL='mysql://user:pass@localhost/db' # SQLALCHEMY COMPATIBLE postgsql://user:pass@localhost/db
export DEST_TABLE='table_name'

virtualenv -p /path/to/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Then run with:

```bash
python index.py
```

## Testing

```bash
python -m unittest discover test
```


## Assumptions

* Assuming pandas automated interpretation of datatypes in csv is sufficient
* No requirements around how the database is to be used as a result:
  * Target DB already exists
  * Target table doesn't exist
  * No indexing is required
  * Rather than potentially complicate/slow down data persistence, I've put a comment in to say where lng/lat queue message might go to trigger that process independently.
* Data is only updated quarterly, imaging this could be a quickly spun up/built docker image run infequently:
  * As a result, prioriting a docker image we could potentially spin up an ephemeral server, then build/run docker

## Requirements

### What tools/resources you would use

* Pandas
* SQLAlchemy
* Docker
* Python multi-processor functionality

### How would you treat/manage the import as part of your operational workload

That would depend on requirements for this data, where is it used in the system?

Is the database the source for others systems? If using AWS, perhaps an SNS notification could be fired on completion for further systems to ingest data from the database(eg say elasticsearch indexes needing an update).

### How you would scale the import if it grew massively in size? Say from 8Gb to 100Gb

If we wanted to scale out insertion horizontally, rather than use multicore processing. We could initially start with by:

1. A script to download the zip, extract it, then push to s3.
2. On pushing each csv to s3 an SQS(or SNS if other metrics/data source).
3. Have a Lambda job to recieve the CSV filename then:
    1. Pull from s3
    2. Process data into the database

Upsides:

* Very little on-going cost as lambda/sqs/sns charge on-demand.
* Scales horizontally so should be very quick to process large amounts of data.

Downside:

* Complicates things
* End to end testing is more difficult
* With python's multiprocess functionality we are limited by the number of processes supplied to the pool. Depending on your account setup, Lambda can run 1000s of concurrent workers, this could flood your database connection limit easily(and Lambda has limited controls around concurrency limits at the moment)

Another potential solution is to use something like Hadoop's Mapreduce to do batch processing.

### How often would you run the import? What is an acceptable completion time?

* If the data is only updated quarterly I don't see any reason to run it anymore often that that.
* An acceptable completion time would depend on the requirements of the business. Once the data is published what would be considered acceptable.

### How would you know when the import has failed?

* It'd throw an error to stderr but nothing is capturing or doing anything with that for multiprocessor

## TODO

* Finish dockerfile(Basic structure is in place but needs to be tested/support env variables etc)
* Better checks around database/table existences
* Better logging
* Specify logstash as logger to leverage ELK
* Write a potential downloader for automatically grabbing/unzipping source data
* Rewrite processfiles to not use pool.map as it's messed up the abstraction layer I was going for
* Refactor ProcessFiles
* Add testing against the ProcessFiles.py this was tough, again due to time shortages and the limitations of multiprocessing
  * This means injecting say mock dependencies was a challenge.