try:
    from utilix.rundb import DB

    # instantiate here so we just do it once
    db = DB()

except FileNotFoundError:
    print("Warning: no xenon_config file found!")
