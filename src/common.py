import pandas as pd
import sys
from ast import literal_eval

GRAPH_QL_ENDPOINT = 'https://gentle-reindeer-95.hasura.app/v1/graphql'
ID_COLUMN_NAME = 'id'


def filter_not_unique_ids(df, keep='last'):
    number_of_uniques_ids = len(df.id.unique())
    if number_of_uniques_ids != len(df):
        print(f"Non unique_ids find in data, filter keeping {keep}")
        df.drop_duplicates(subset=ID_COLUMN_NAME, keep=keep, inplace=True)


def string_to_array(row, ident):
    if ident in row:
        row[ident] = literal_eval(row[ident])
    return row


def filter_nans(row):
    return dict((k, v) for k, v in row.items() if not pd.isnull(v))


def handle_result(res, query_name):
    if 'errors' in res:
        for error in res['errors']:
            print("ERROR:", error['message'])
            sys.exit(1)
    else:
        print(f"SUCCESSFULY UPDATE/INSERT: {res['data'][query_name]['affected_rows']} rows")


def get_data_path(parser):
    parser.add_argument('data_path', type=str, help='Path to csv.file')
    args = parser.parse_args()
    return args.data_path
