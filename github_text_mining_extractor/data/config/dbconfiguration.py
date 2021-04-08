""" Database Configuration class module.
"""


class DBConfiguration():

    def get_engine_str():
        return "sqlite+pysqlite:///:memory:"  # "sqlite:////tmp/database.db"
