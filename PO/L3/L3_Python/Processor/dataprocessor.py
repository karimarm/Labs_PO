from abc import ABC, abstractmethod     # подключаем инструменты для создания абстрактных классов
from typing import List

import pandas   # пакет для работы с датасетами

"""
    В данном модуле реализуются классы обработчиков для 
    применения алгоритма обработки к различным типам файлов (csv или txt).
"""


class DataProcessor(ABC):
    """ Родительский класс для обработчиков файлов """

    def __init__(self, datasource: str):
        # общие атрибуты для классов обработчиков данных
        self._datasource = datasource   # путь к источнику данных
        self._dataset = None            # входной набор данных
        self.result = None              # выходной набор данных (результат обработки)


    # Все методы, помеченные декоратором @abstractmethod, ОБЯЗАТЕЛЬНЫ для переопределения в классах-потомках
    @abstractmethod
    def read(self) -> bool:
        """ Метод, инициализирующий источник данных """
        pass

    def run(self) -> None:
        """ Метод, запускающий обработку данных """

        choise = int(input("1) Отфильтровать по годам и странам\n2) Отсортировать по крадитным ставкам\n3) Отфильтровать кредитные ставки\nВведите команду: "))
        if choise == 1:
            self.result = self.filter_by_years_and_countries()
        elif choise == 2:
            self.result = self.sort_by_credit_rates()
        elif choise == 3:
            self.result = self.filter_credit_rates()

    """
        Ниже представлены примеры различных методов для обработки набора данных
    """

    def sort_data_by_col(self, df: pandas.DataFrame, colname: str, asc: bool) -> pandas.DataFrame:
        """
            Метод sort_data_by_col просто сортирует входной датасет по наименованию
            заданной колонки (аргумент colname) и устанвливает тип сортировки:
            ascending = True - по возрастанию, ascending = False - по убыванию
        """
        return df.sort_values(by=[colname], ascending=asc)

    def remove_col_by_name(self, df: pandas.DataFrame, col_name: List[str]):
        """
            Метод remove_col_by_name принимает входной набор данных и список имён колонок для удаления.
            Возвращает набор данных с удалёнными колонками.
        """
        return df.drop(col_name, axis=1)

    def get_mean_value_by_filter(self, df: pandas.DataFrame, filter_expr: str) -> pandas.DataFrame:
        """
            Метод get_mean_value_by_filter выбирает из входного набора данных строки с заданным условием
            (фильтр), используя инструкцию DataFrame.query(), применяет к получившимся значением функцию
            mean (считает среднее значения в колонках) и возвращает результат в виде нового DataFrame.
        """
        result = df.query(filter_expr)
        return result.mean(axis=0, skipna=True).to_frame().T



    def filter_by_years_and_countries(self) -> pandas.DataFrame:
        """
             Фильтрует входного набора данных по заданным строкам и столбцам
        """

        result_dt = self._dataset
        countries = ["country/year"]
        years = ["country/year"]

        """ Ввод стран """
        n = int(input("Введите количество стран: "))
        """ Если введён 0,то будут выбраны все страны """
        if n != 0:
            print("Введите страны:")
            for _ in range(n):
                countries.append(input())
            result_dt = self._dataset[self._dataset["country/year"].isin(countries)]

        """ Ввод годов """
        n = int(input("Введите количество годов: "))
        """ Если введён 0,то будут выбраны все годы """
        if n != 0:
            print("Введите годы:")
            for _ in range(n):
                years.append(input())
            result_dt = result_dt[years]
        return result_dt



    def sort_by_credit_rates(self) -> pandas.DataFrame:
        """
            Сортирует кредитные ставки за выбранный год
        """

        years = ["country/year"]
        year = input("Введите год: ")
        years.append(year)
        result_dt = self._dataset[years]
        result_dt = self.sort_data_by_col(result_dt, year, False)
        return result_dt



    def filter_credit_rates(self) -> pandas.DataFrame:
        """
            Фильтрует кредитные ставки по выбранному диапазону за выбранный год
        """

        years = ["country/year"]
        rates = []
        year = input("Введите год: ")
        years.append(year)
        result_dt = self._dataset[years]
        min_credit_rates = int(input("Введите минимальную кредитную ставку: "))
        max_credit_rates = int(input("Введите максимальную кредитную ставку: "))
        for i in range(min_credit_rates, max_credit_rates):
            rates.append(i)
        result_dt = result_dt[result_dt[year].isin(rates)]
        return result_dt


    @abstractmethod
    def print_result(self) -> None:
        """ Абстрактный метод для вывода результата на экран """
        pass


class CsvDataProcessor(DataProcessor):
    """ Реализация класса-обработчика csv-файлов """

    def __init__(self, datasource: str):
        # Переопределяем конструктор родительского класса
        DataProcessor.__init__(self, datasource)    # инициализируем конструктор родительского класса для получения общих атрибутов
        self.separators = [';', ',', '|']        # список допустимых разделителей

    """
        Переопределяем метод инициализации источника данных.
        Т.к. данный класс предназначен для чтения CSV-файлов, то используем метод read_csv
        из библиотеки pandas
    """
    def read(self):
        try:
            # Пытаемся преобразовать данные файла в pandas.DataFrame, используя различные разделители
            for separator in self.separators:
                self._dataset = pandas.read_csv(self._datasource, sep=separator, header='infer', names=None, encoding="utf-8")
                # Читаем имена колонок из файла данных
                col_names = self._dataset.columns
                # Если количество считанных колонок > 1 возвращаем True
                if len(col_names) > 1:
                    print(f'Columns read: {col_names} using separator {separator}')
                    return True
        except Exception as e:
            print(e)
        return False

    def print_result(self):
        print(f'Running CSV-file processor!\n', self.result)


class TxtDataProcessor(DataProcessor):
    """ Реализация класса-обработчика txt-файлов """

    def read(self):
        """ Реализация метода для чтения TXT-файла (разедитель колонок - табуляция) """
        try:
            self._dataset = pandas.read_table(self._datasource, sep='\t', engine='python')
            col_names = self._dataset.columns
            if len(col_names) < 2:
                return False
            return True
        except Exception as e:
            print(str(e))
            return False

    def print_result(self):
        print(f'Running TXT-file processor!\n', self.result)
