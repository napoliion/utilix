# utilix
Package for XENON members to easily interface with RunDB, Midway batch queue, maybe Rucio (others?). 

## Configuration file

This tool expects a configuration file named `$HOME/.xenon_config`. Note that
environment variables can be used in the form `$HOME`. Example:

    [RunDB]

    rundb_api_url = [ask Evan]
    rundb_api_user = [ask Evan]
    rundb_api_password = [ask Evan]


The idea is that analysts could use this single config for multiple purposes/analyses.
You just need to add a (unique) section for your own purpose and then you can use the `utilix.Config` 
easily. For example, if you made a new section called `WIMP` with `detected = yes` under it:

    from utilix.config import Config
    cfg = Config()
    value = cfg.get('WIMP', 'detected') # value = 'yes'
    
For more information, see the [ConfigParser](https://docs.python.org/3.6/library/configparser.html)
documentation, from which `utilix.config.Config` inherits.
## Examples

### Query for runs by source

Note that the interface returns pages of 1,000 entries, with the first page being 1.

    from utilix import db
    data = db.query_by_source('neutron_generator', page_num=1)

### Get a full document

You can also grab the full run document using the run number. A run name is also supported (from XENON1T days), 
but not going to be used for XENONnT

    doc = db.get_doc(7200)

### Get only the data entry of a document

    data = db.get_data(2000)
    
    

### TODO
We want to implement functionality for easy job submission to the Midway batch queue.
Eventually we want to do the same for OSG. 

It would be nice to port e.g. the admix database wrapper to utilix, which can then be used 
easily by all analysts. 

The rundb API likely needs to be updated slightly to handle nT schema.