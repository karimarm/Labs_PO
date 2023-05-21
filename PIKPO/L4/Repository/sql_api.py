from typing import List

from .connector import StoreConnector
from pandas import DataFrame, Series
from datetime import datetime

"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
"""


def select_all_from_source_files(connector: StoreConnector) -> List[tuple]:
    """ Вывод списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING) """
    query = f'SELECT * FROM source_files ORDER BY processed DESC'
    result = connector.execute(query).fetchall()
    return result


def insert_into_source_files(connector: StoreConnector, filename: str):
    """ Вставка в таблицу обработанных файлов """
    now = datetime.now()        # текущая дата и время
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")   # преобразуем дату в формат SQL, например, '2022-11-15 22:03:16'
    query = f'INSERT INTO source_files (filename, processed) VALUES (\'{filename}\', \'{date_time}\')'
    result = connector.execute(query)
    return result


def insert_rows_into_processed_data(connector: StoreConnector, dataframe: DataFrame):
    """ Вставка строк из DataFrame в БД с привязкой данных к последнему обработанному файлу (по дате) """
    dataframe.columns = ['country', 'credit_rate']
    rows = dataframe.to_dict('records')
    files_list = select_all_from_source_files(connector)
    last_file_id = files_list[0][0]
    if len(files_list) > 0:
        for row in rows:
            connector.execute(f'INSERT INTO processed_data (country, credit_rate, source_file) VALUES (\'{row["country"]}\','
                              f'\'{row["credit_rate"]}\', {last_file_id})')
        print('Data was inserted successfully')
    else:
        print('File records not found. Data inserting was canceled.')


def update(connector: StoreConnector, dataframe: DataFrame):
    col = dataframe.columns.tolist()
    col.pop(0)
    row = dataframe['country/year']

    if len(col) > 0:
        connector.execute(f'DELETE FROM years')
        for i in col:
            #print(i)
            connector.execute(f'INSERT INTO years (year) VALUES (\"{i}\")')
        print('update was inserted successfully')
    else:
        print('File records not found. update inserting was canceled.')

    if len(row) > 0:
        connector.execute(f'DELETE FROM countries')
        for i in row:
            #print(i)
            connector.execute(f'INSERT INTO countries (country) VALUES (\"{i}\")')
        print('update was inserted successfully')
    else:
        print('File records not found. update inserting was canceled.')
