from Processor.dataprocessor_service import DataProcessorService

"""
    Main-модуль, т.е. модуль запуска приложений ("точка входа" приложения)
"""

if __name__ == '__main__':
    # Без указания полного пути, программа будет читать файл из своей корневой папки
    DataProcessorService(datasource="central_bank_discount_rate_annual_percent.csv", db_connection_url="sqlite:///DB.db").run_service()
