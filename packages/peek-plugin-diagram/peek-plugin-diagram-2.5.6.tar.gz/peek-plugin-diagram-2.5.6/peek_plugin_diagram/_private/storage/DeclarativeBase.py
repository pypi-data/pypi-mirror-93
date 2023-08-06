from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.schema import MetaData
from txhttputil.util.ModuleUtil import filterModules

from peek_plugin_diagram._private.storage import branch

metadata = MetaData(schema="pl_diagram")
DeclarativeBase = declarative_base(metadata=metadata)


# noinspection PyUnresolvedReferences
def loadStorageTuples():

    """ Load Storage Tables

    This method should be called from the "load()" method of the agent, server, worker
    and client entry hook classes.

    This will register the ORM classes as tuples, allowing them to be serialised and
    deserialized by the vortex.

    """
    # Import the disp links first for the SQLA Mapper
    from . import LiveDbDispLink

    for mod in filterModules(__package__, __file__):
        if mod.startswith("Declarative"):
            continue
        __import__(mod, locals(), globals())

    for mod in filterModules(branch.__package__, branch.__file__):
        __import__(mod, locals(), globals())
