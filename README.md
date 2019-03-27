# utilix
Package for XENON members to easily interface with RunDB, Midway batch queue, maybe Rucio (others?). 

## Configuration file

This tool expects a configuration file named `$HOME/.xenonnt.conf`. Note that
environment variables can be used in the form `$HOME`. Example:

    [RunDB]

    rundb_api_url = [ask Evan]
    rundb_api_user = [ask Evan]
    rundb_api_password = [ask Evan]
    
