import pandas as pd
import argparse
from python_graphql_client import GraphqlClient

from common import filter_not_unique_ids, GRAPH_QL_ENDPOINT, string_to_array, filter_nans, handle_result, \
    get_data_path, ID_COLUMN_NAME

COLUMN_NAMES_FOR_MODIFICATION = ['lat', 'lon', 'plec', 'rok_urodzenia', 'dochod', 'zainteresowania']
COLUMN_NAMES = COLUMN_NAMES_FOR_MODIFICATION + [ID_COLUMN_NAME]

query_users = '''
mutation update_internauta($objects: [internauta_insert_input!]!, $colnames: [internauta_update_column!]!) {
    insert_internauta(objects: $objects
      on_conflict: {
        constraint: internauta_pkey,
        update_columns: $colnames
      }
  ) {
    affected_rows
  }
}
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script updates or inserts users info in database')
    data_path = get_data_path(parser)

    client = GraphqlClient(endpoint=GRAPH_QL_ENDPOINT)

    df = pd.read_csv(data_path)
    df = df[[col for col in df.columns if col in COLUMN_NAMES]]
    filter_not_unique_ids(df)

    rows = df.to_dict('records')
    rows = [string_to_array(filter_nans(row), 'zainteresowania') for row in rows]

    col_names = [col for col in df.columns if col in COLUMN_NAMES_FOR_MODIFICATION]

    res = client.execute(query=query_users, variables={"objects": rows, "colnames": col_names})

    handle_result(res, 'insert_internauta')
