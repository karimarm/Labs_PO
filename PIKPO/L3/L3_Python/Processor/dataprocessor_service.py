from .dataprocessor_factory import DataProcessorFactory

"""
    В данном модуле реализуется класс с основной бизнес-логикой приложения. 
    Обычно такие модули / классы имеют в названии слово "Service".
"""


class DataProcessorService:

    def __init__(self, datasource: str):
        self.datasource = datasource
        # Инициализируем в конструкторе фабрику DataProcessor
        self.processor_fabric = DataProcessorFactory()

    def run_service(self) -> None:
        """ Метод, который запускает сервис обработки данных  """
        processor = self.processor_fabric.get_processor(self.datasource)        # Инициализируем обработчик
        if processor is not None:
            processor.run()
            processor.print_result()
        else:
            print('Nothing to run')
