try:
    from utilix.rundb import DB
    # instantiate here so we just do it once
    db = DB()

# if no utilix config exists, a RuntimeError is raised
except RuntimeError:
    print("Warning: no utilix configuration file found!")
