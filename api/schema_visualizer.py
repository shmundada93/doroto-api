from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

# Database
host = 'localhost:3306'
engine = 'mysql'
database = 'doroto'
username = 'doroto'
password = 'doroto'

# General
data_types = True
indexes = False

# Generation
dsn = engine + '://' + username + ':' + password + '@' + host + '/' + database

graph = create_schema_graph(
        metadata=MetaData(dsn),
        show_datatypes=data_types,
        show_indexes=indexes
)

graph.write_png('schema.png')