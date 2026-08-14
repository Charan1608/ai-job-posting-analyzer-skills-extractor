import pandas as pd
import re
from pathlib import Path


def load_role_taxonomy():

    taxonomy_path = Path("taxonomy/role_taxonomy.csv")

    taxonomy = pd.read_csv(taxonomy_path)

    taxonomy["Include"] = taxonomy["Include"].astype(bool)

    taxonomy = taxonomy[taxonomy["Include"] == True]

    return taxonomy


def classify_role(job_title, taxonomy):

    title = str(job_title).lower()

    for _, row in taxonomy.iterrows():

        pattern = row["Regex_Pattern"]

        if re.search(pattern, title):
            return row["Role_Family"]

    return "Other"