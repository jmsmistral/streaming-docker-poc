import json
import logging

from faker import Faker
import numpy as np
from numpy.random import RandomState as mrs
import pandas as pd


logger = logging.getLogger("Generator")

# Init faker
fake = Faker()


class sample_generator():
    def __init__(self, config):
        self._dataset = self._generate_data(config)

    def _get_date(self, config):
        start_date = config["start_date"]
        end_date = config["end_date"]
        dates = mrs().choice(
            pd.date_range(start_date, end_date, freq="S"), config["n"],
        )
        date_df = pd.DataFrame({"Datetime": dates})
        # Convert to string as Datetime is not JSON serializable
        date_df["Datetime"] = date_df["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
        return date_df

    def _get_name_and_email(self, config):
        n = config["n"]
        name_df = pd.DataFrame({"Name": [fake.name() for i in range(n)]})
        name_df["Email"] = (name_df["Name"] + "@example.com").str.replace(" ", "_").str.lower()
        return name_df

    def _get_location(self, config):
        location_sample = config["locations"]
        locations = mrs().choice(location_sample, config["n"])
        location_df = pd.DataFrame({"Location": locations})
        return location_df

    def _generate_data(self, config):
        config = config["test_data"]
        logger.info(config)

        name_df = self._get_name_and_email(config)
        date_df = self._get_date(config)
        location_df = self._get_location(config)

        df = pd.concat((name_df, date_df, location_df), axis=1)

        return df

    def get_message(self):
        select_index = mrs().choice(self._dataset.index)
        sample = self._dataset.loc[select_index]
        message = {
            "Name": sample["Name"],
            "Email": sample["Email"],
            "Datetime": sample["Datetime"],
            "Location": sample["Location"]
        }
        return json.dumps(message)
        

