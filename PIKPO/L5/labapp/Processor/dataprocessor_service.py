from .dataprocessor_factory import DataProcessorFactory
from ..repository.connectorfactory import SQLStoreConnectorFactory       # подключаем фабрику коннекторов БД
from ..repository.sql_api import *                                       # подключаем API для работы с БД
from ..repository.connector import StoreConnector
from pandas import DataFrame
from typing import List

"""
    В данном модуле реализуется класс с основной бизнес-логикой приложения. 
    Обычно такие модули / классы имеют в названии слово "Service".
"""


class DataProcessorService:

    def __init__(self, datasource: str, db_connection_url: str):
        self.datasource = datasource
        self.db_connection_url = db_connection_url
        self.processor = None
        # Инициализируем в конструкторе фабрику DataProcessor
        self.processor_fabric = DataProcessorFactory()


    def push_years_and_contries_tables(self):
        self.processor = self.processor_fabric.get_processor(self.datasource)  # Инициализируем обработчик
        dataset = self.processor.get_dataset()
        db_connector = None

        if dataset is not None:
            try:
                db_connector = SQLStoreConnectorFactory().get_connector(self.db_connection_url)  # инициализируем соединение
                db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)

                fl_countries_empty = db_connector.execute(f"SELECT COUNT(*) FROM countries").fetchone()
                fl_years_empty = db_connector.execute(f"SELECT COUNT(*) FROM years;").fetchone()
                # Обновление таблиц годов и стран
                if fl_countries_empty[0] == 0 or fl_years_empty[0] == 0:
                    update(db_connector, dataset)
            except Exception as e:
                print(e)
            finally:
                if db_connector is not None:
                    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
                    db_connector.close()  # Завершаем работу с БД


    def run_service(self, select_year: str, select_countries: list, check_sort: str, min_credit_rate: str, max_credit_rate: str) -> None:
        """ Метод, который запускает сервис обработки данных  """
        self.processor = self.processor_fabric.get_processor(self.datasource)        # Инициализируем обработчик
        if self.processor is not None:
            self.processor.run(select_year, select_countries, check_sort, min_credit_rate, max_credit_rate)
            self.processor.print_result()
        else:
            print('Nothing to run')
        self.save_to_database(self.processor.result)


    def save_to_database(self, result: DataFrame) -> None:
        """ Сохранение данных в БД """
        db_connector = None
        if result is not None:
            try:
                db_connector = SQLStoreConnectorFactory().get_connector(self.db_connection_url)  # инициализируем соединение
                db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
                insert_into_source_files(db_connector, self.datasource)  # сохраняем в БД информацию о новом файле с набором данных
                print(select_all_from_source_files(db_connector))  # вывод списка всех обработанных файлов
                insert_rows_into_processed_data(db_connector, result)  # записываем в БД результат обработки набора данных
            except Exception as e:
                print(e)
            finally:
                if db_connector is not None:
                    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
                    db_connector.close()            # Завершаем работу с БД
