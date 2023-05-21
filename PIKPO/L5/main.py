# Подключаем приложение Flask из пакета labapp (см. модуль инициализации __init__.py)
from labapp import app
from labapp.Processor.dataprocessor_service import DataProcessorService

"""
    Этот модуль запускает web-приложение
"""

if __name__ == '__main__':
    DataProcessorService(datasource="central_bank_discount_rate_annual_percent.csv",
                         db_connection_url="sqlite:///C:\\Users\\user\\Documents\\GitHub\\Labs_PIKPO\\PIKPO\\L5\\DB.db").push_years_and_contries_tables()
    app.run(host='0.0.0.0', port=8000)
