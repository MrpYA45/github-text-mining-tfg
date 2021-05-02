""" Database Configuration class module.
"""


class DBConfiguration():

    @staticmethod
    def get_engine_str():
        return "sqlite:///github_text_mining.db"
