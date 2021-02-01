from datetime import datetime
from python_graphql_client.graphql_client import GraphqlClient
from common import GRAPH_QL_ENDPOINT
from collections import defaultdict

DELIMITER_STRING = "#" * 100

EMPTY_CONDITION_QUERY = {'reklamaByReklama': {'kolor': {}, 'rozpoznane_teksty': {}, 'szerokosc': {}, 'wysokosc': {}},
                         'internautum': {'dochod': {}, 'lat': {}, 'lon': {}, 'plec': {}, 'rok_urodzenia': {}}}

queryQL = ''' 
query  my_query($conditions : wyswietlenie_bool_exp){
  wyswietlenie_aggregate(where: $conditions) {
    aggregate {
      count
    }
  }
}
'''

root = None


def pprint_cond(cond, current_cond, _prefix=""):
    label_name = "AKTUALNIE MODYFIKOWANY " if current_cond == cond else ""
    print(_prefix, label_name, condition_to_string(cond), sep='')

    if '_or' in cond:
        print(_prefix, "OR:", sep='')
        for c in cond['_or']:
            pprint_cond(c, current_cond, _prefix + (4 * ""))

    if '_and' in cond:
        print(_prefix, "AND:", sep='')
        for c in cond['_and']:
            pprint_cond(c, current_cond, f"{_prefix}    ")


def condition_to_string(cond):
    cond_for_print = dict((k, dict(v)) for k, v in cond.items() if k not in ['timestamp', '_or', '_and'])
    return str(cond_for_print)


def init_condition(start_time=None, end_time=None):
    result = defaultdict(lambda: defaultdict(dict))

    if start_time is not None:
        result['timestamp']['_gte'] = start_time.strftime("%Y-%m-%d %H:%M:%S")
    if end_time is not None:
        result['timestamp']['_lt'] = end_time.strftime("%Y-%m-%d %H:%M:%S")

    return result


def query_datetime(printed_info):
    auxiliary_info = "W formacie yyyy-mm-dd HH:MM:SS, przykładowo 2020-01-31 13:00:00"

    while True:
        datetime_str = input(f"{DELIMITER_STRING} \n {printed_info} \n {auxiliary_info}")
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            print(f"Błąd:{e}")


def parse_action_number(action_str, max_number_of_actions):
    action_nr = int(action_str)
    if action_nr not in list(range(1, max_number_of_actions + 1)):
        raise ValueError("Nieprawidlowy numer akcji")
    return action_nr


def modify_condition_with_input(condition, key, name):
    value = input(f"Podaj wartość {name}")
    condition[key] = value


def add_categorical_condition(categorical_condition, name):
    while True:
        menu_str = f''' {DELIMITER_STRING}
                             Modyfikowany warunek na {name}: {categorical_condition}
                             Wybierz typ dodawanego warunku:
                             1.  = 
                             2.  !=
                             3. Zatwierdz
        '''
        action_str = input(menu_str)
        try:
            action_nr = parse_action_number(action_str, 3)

            if action_nr == 1:
                modify_condition_with_input(categorical_condition, '_eq', name)
            elif action_nr == 2:
                modify_condition_with_input(categorical_condition, '_neq', name)
            else:
                return
        except ValueError as error:
            print(error.args)


def add_numeric_condition(numeric_condition, name):
    while True:
        menu_str = f''' {DELIMITER_STRING}
                             Modyfikowany warunek na {name}: {numeric_condition}
                             Wybierz typ dodawanego warunku:
                             1.  = 
                             2.  >=
                             3.  <=
                             4.  >
                             5.  <
                             6.  !=
                             7. Zatwierdz
        '''

        action_str = input(menu_str)
        try:
            action_nr = parse_action_number(action_str, 7)

            if action_nr == 1:
                modify_condition_with_input(numeric_condition, '_eq', name)
            elif action_nr == 2:
                modify_condition_with_input(numeric_condition, '_gte', name)
            elif action_nr == 3:
                modify_condition_with_input(numeric_condition, '_lte', name)
            elif action_nr == 4:
                modify_condition_with_input(numeric_condition, '_gt', name)
            elif action_nr == 5:
                modify_condition_with_input(numeric_condition, '_lt', name)
            elif action_nr == 6:
                modify_condition_with_input(numeric_condition, '_neq', name)
            else:
                return
        except ValueError as error:
            print(error.args)


def add_array_condition(array_condition, name):
    while True:
        color_menu_str = f''' {DELIMITER_STRING}
                             Modyfikowany warunek na {name}: {array_condition}
                             1.  Wartość znajduje się w tablicy
                             2.  Zatwierdz 
        '''
        action_str = input(color_menu_str)
        try:
            action_nr = parse_action_number(action_str, 2)

            if action_nr == 1:
                modify_condition_with_input(array_condition, '_contains', name)
            else:
                return
        except ValueError as error:
            print(error.args)


def condition_menu(cond_argument):
    while True:
        pprint_cond(root, cond_argument)
        menu_string = f'''{DELIMITER_STRING}
                            Warunek nakładany na:
                            1. Kolor reklamy
                            2. Rozpoznany tekst w tresci reklamy
                            3. Szerokosc reklamy
                            4. Wysokość reklamy
                            5. Dochód internauty
                            6. Długość geograficzną pozycji internauty
                            7. Szerokość geograficzną pozycji internauty
                            8. Płeć internauty
                            9. Rok urodzenia
                            10. Dodaj warunek AND
                            11. Dodaj warunek OR
                            12. Zatwierdz
        '''
        action_str = input(menu_string)
        try:
            action_nr = parse_action_number(action_str, 12)

            if action_nr == 1:
                add_categorical_condition(cond_argument['reklamaByReklama']['kolor'], 'kolor')
                pass
            elif action_nr == 2:
                add_array_condition(cond_argument['reklamaByReklama']['rozpoznane_teksty'], 'rozpoznane teksty')
            elif action_nr == 3:
                add_numeric_condition(cond_argument['reklamaByReklama']['szerokosc'], 'szerokosc reklamy')
            elif action_nr == 4:
                add_numeric_condition(cond_argument['reklamaByReklama']['wysokosc'], 'wysokosc reklamy')
            elif action_nr == 5:
                add_numeric_condition(cond_argument['internautum']['dochod'], 'dochód internauty')
            elif action_nr == 6:
                add_numeric_condition(cond_argument['internautum']['lon'],
                                      'długość geograficzną pozycji internauty')
            elif action_nr == 7:
                add_numeric_condition(cond_argument['internautum']['lat'],
                                      'długość geograficzną pozycji internauty')
            elif action_nr == 8:
                add_categorical_condition(cond_argument['internautum']['plec'], 'płeć internauty')
            elif action_nr == 9:
                add_numeric_condition(cond_argument['internautum']['rok_urodzenia'], 'rok urodzenia internauty')
            elif action_nr == 10:
                if '_and' not in cond_argument:
                    cond_argument['_and'] = []
                child_cond = init_condition()
                cond_argument['_and'].append(child_cond)
                condition_menu(child_cond)
            elif action_nr == 11:
                if '_or' not in cond_argument:
                    cond_argument['_or'] = []
                child_cond = init_condition()
                cond_argument['_or'].append(child_cond)
                condition_menu(child_cond)
            else:
                return
        except ValueError as error:
            print(error.args)


if __name__ == "__main__":
    # start_datetime = query_datetime("Proszę podać początek okresu")
    # end_datetime = query_datetime("Proszę podać koniec okresu")
    start_datetime = datetime(1970, 1, 1)
    end_datetime = datetime(2030, 1, 1)
    cond = init_condition(start_datetime, end_datetime)
    root = cond

    condition_menu(cond)
    client = GraphqlClient(endpoint=GRAPH_QL_ENDPOINT)

    res = client.execute(query=queryQL, variables={"conditions": cond})
    print("Spełniających te kryteria wyświetleń jest", res['data']['wyswietlenie_aggregate']['aggregate']['count'])
