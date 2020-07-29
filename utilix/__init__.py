try:
    from utilix.rundb import DB

    # instantiate here so we just do it once
    db = DB()

except:
    print("Error initializing RunDB. Maybe no ~/.xenon_config file?")
