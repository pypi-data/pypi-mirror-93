from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.schema import MetaData

metadata = MetaData(schema="pl_docdb_generic_menu")
DeclarativeBase = declarative_base(metadata=metadata)


def loadStorageTuples():

    """ Load Storage Tables

    This method should be called from the "load()" method of the agent, server, worker
    and client entry hook classes.

    This will register the ORM classes as tuples, allowing them to be serialised and
    deserialized by the vortex.

    """
    from . import DocDbGenericMenuTuple
    DocDbGenericMenuTuple.__unused = False

    from . import Setting
    Setting.__unused = False
