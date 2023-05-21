from .dataprocessor_factory import DataProcessorFactory
from Repository.connectorfactory import SQLStoreConnectorFactory       # подключаем фабрику коннекторов БД
from Repository.sql_api import *                                       # подключаем API для работы с БД

"""
    В данном модуле реализуется класс с основной бизнес-логикой приложения. 
    Обычно такие модули / классы имеют в названии слово "Service".
"""


class DataProcessorService:

    def __init__(self, datasource: str, db_connection_url: str):
        self.datasource = datasource
        self.db_connection_url = db_connection_url
        self.database = None
        # Инициализируем в конструкторе фабрику DataProcessor
        self.processor_fabric = DataProcessorFactory()

    def run_service(self) -> None:
        """ Метод, который запускает сервис обработки данных  """
        processor = self.processor_fabric.get_processor(self.datasource)        # Инициализируем обработчик
        if processor is not None:
            processor.run()
            processor.print_result()
            self.database = processor.getDatabase()
        else:
            print('Nothing to run')
        self.save_to_database(processor.result)


    def save_to_database(self, result: DataFrame) -> None:
        """ Сохранение данных в БД """
        db_connector = None
        if result is not None:
            try:
                db_connector = SQLStoreConnectorFactory().get_connector(self.db_connection_url)  # инициализируем соединение
                db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)

                """
                    Обновление таблиц годов и стран
                    update(db_connector, self.database)
                """

                insert_into_source_files(db_connector, self.datasource)  # сохраняем в БД информацию о новом файле с набором данных
                print(select_all_from_source_files(db_connector))  # вывод списка всех обработанных файлов
                insert_rows_into_processed_data(db_connector, result)  # записываем в БД результат обработки набора данных
            except Exception as e:
                print(e)
            finally:
                if db_connector is not None:
                    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
                    db_connector.close()            # Завершаем работу с БД
