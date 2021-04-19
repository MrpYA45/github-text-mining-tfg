""" Database Configuration class module.
"""


class DBConfiguration():

    @staticmethod
    def get_engine_str():
        return "sqlite+pysqlite:///:memory:"  # "sqlite:////tmp/database.db"

    def get_debug_state():
        return False
