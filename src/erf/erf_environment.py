import os
from datetime import datetime


class ERFEnvironment:
    """
    The environment stores values and configurations
    used during the compilation of the ERF (embedded referencing format) files.
    """

    def __init__(self):
        """
        Initialize the environment with the current working directory
        and a default set of environment variables.
        """
        self.file_root = os.getcwd()
        self.env_vars = {}
        self.initialize_env_vars()

    def initialize_env_vars(self):
        """
        Initialize the environment with same default environment variables e.g., current time and date.
        """
        current_datetime = datetime.now()
        self.env_vars['DATE'] = current_datetime.strftime('%Y-%m-%d')
        self.env_vars['TIME'] = current_datetime.strftime('%H:%M')
