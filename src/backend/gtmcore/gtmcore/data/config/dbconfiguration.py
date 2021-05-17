""" Database Configuration class module.
"""


class DBConfiguration():
    """ Definition of database configuration aspects.
    """

    @staticmethod
    def get_engine_str() -> str:
        """ Gets the engine connection string.

        Returns:
            str: The engine connection string.
        """
        return "sqlite:////tmp/gtm_database.db"
