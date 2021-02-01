import pandas as pd
import argparse
from python_graphql_client import GraphqlClient

from common import GRAPH_QL_ENDPOINT, handle_result, get_data_path

COLUMN_NAMES = ['internauta', 'reklama', 'timestamp']

query_imp = '''
mutation update_wyswietlenie($objects: [wyswietlenie_insert_input!]!) {
    insert_wyswietlenie(objects: $objects)
  {
    affected_rows
  }
}
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script add impressions into database')
    data_path = get_data_path(parser)

    client = GraphqlClient(endpoint=GRAPH_QL_ENDPOINT)

    df = pd.read_csv(data_path)
    df = df[[col for col in df.columns if col in COLUMN_NAMES]]
    rows = df.to_dict('records')
    res = client.execute(query=query_imp, variables={"objects": rows})

    handle_result(res, 'insert_wyswietlenie')