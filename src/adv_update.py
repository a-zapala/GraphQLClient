import pandas as pd
import argparse
from python_graphql_client import GraphqlClient

from common import GRAPH_QL_ENDPOINT, string_to_array, ID_COLUMN_NAME, filter_nans, handle_result, \
    get_data_path

COLUMN_NAMES_FOR_MODIFICATION = ['szerokosc', 'wysokosc', 'rozpoznane_teksty', 'kolor']
COLUMN_NAMES = COLUMN_NAMES_FOR_MODIFICATION + [ID_COLUMN_NAME]

query_adv = '''
mutation update_reklama($objects: [reklama_insert_input!]!, $colnames: [reklama_update_column!]!) {
    insert_reklama(objects: $objects
      on_conflict: {
        constraint: reklama_pkey,
        update_columns: $colnames
      }
  ) {
    affected_rows
  }
}
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script updates or inserts advertisement info in database')
    data_path = get_data_path(parser)

    client = GraphqlClient(endpoint=GRAPH_QL_ENDPOINT)

    df = pd.read_csv(data_path)
    df = df[[col for col in df.columns if col in COLUMN_NAMES]]
    rows = df.to_dict('records')
    rows = [string_to_array(filter_nans(row), 'rozpoznane_teksty') for row in rows]

    col_names = [col for col in df.columns if col in COLUMN_NAMES_FOR_MODIFICATION]

    res = client.execute(query=query_adv, variables={"objects": rows, "colnames": col_names})
    handle_result(res, 'insert_reklama')