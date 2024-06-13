from uagents import Model


class UserRawData(Model):
    """
    Model for users raw data.

    Attributes:
        raw_data (str): The raw data.
        reply_to (str): The address to reply to.
    """
    raw_data: str
    reply_to: str


class PensionSchemeData(Model):
    """
    Model for pension scheme data.

    Attributes:
        raw_pension_scheme_data (str): The pension scheme data.
        reply_to (str): The address to reply to.
    """
    raw_pension_scheme_data: str
    reply_to: str


class DataForRecommendation(Model):
    """
    Model for data to be used for recommendation.

    Attributes:
        processed_user_data (str): The processed user data.
        processed_scheme (str): The processed pension scheme data.
        reply_to (str): The address to reply to.
    """
    processed_user_data: str
    processed_scheme: str
    reply_to: str
