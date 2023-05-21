from Processor.dataprocessor_service import DataProcessorService


"""
    Main-модуль, т.е. модуль запуска приложений ("точка входа" приложения)
"""

if __name__ == '__main__':
    # Без указания полного пути, программа будет читать файл из своей корневой папки
    DataProcessorService("central_bank_discount_rate_annual_percent.csv").run_service()