# utilix
Package for XENON members to easily interface with RunDB, Midway batch queue, maybe Rucio (others?). 

## Configuration file

This tool expects a configuration file named `$HOME/.xenonnt.conf`. Note that
environment variables can be used in the form `$HOME`. Example:

    [RunDB]

    rundb_api_url = [ask Evan]
    rundb_api_user = [ask Evan]
    rundb_api_password = [ask Evan]

## Examples

### Query for runs by source

Note that the interface returns pages of 1,000 entries, with the first page being 1.

    db = rundb.DB()
    data = db.query_by_source('calibration', page_num=1)

### Get a full document

    db = rundb.DB()
    doc = db.get_doc_by_number(2000)

### Get only the data entry of a document

    db = rundb.DB()
    data = db.get_data_by_number(2000)

    
