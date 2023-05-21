# Подключаем объект приложения Flask из __init__.py
from labapp import app
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, jsonify, redirect
from .Processor.dataprocessor_service import DataProcessorService

import labapp.webservice as webservice   # подключаем модуль с реализацией бизнес-логики обработки запросов

"""
    Модуль регистрации обработчиков маршрутов, т.е. здесь реализуется обработка запросов
    при переходе пользователя на определенные адреса веб-приложения
"""


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    years_list = webservice.get_years_list()
    countries_list = webservice.get_countries_list()

    if request.method == 'POST':
        DataProcessorService(datasource="central_bank_discount_rate_annual_percent.csv",
                             db_connection_url="sqlite:///C:\\Users\\user\\Documents\\GitHub\\Labs_PIKPO\\PIKPO\\L5\\DB.db"
                             ).run_service(request.form['select_year'], request.form.getlist('select_countries[]'), request.form['check_sort'],
                                           request.form['min_credit_rate'], request.form['max_credit_rate'])
        processed_files = webservice.get_source_files_list()
        return redirect(f'/data/{processed_files[0][0]}', code=302)
    return render_template('index.html',
                           title='Labs PIKPO',
                           page_name='HOME',
                           navmenu=webservice.navmenu,
                           years=years_list,
                           countries=countries_list)


@app.route('/history', methods=['GET'])
def history():
    """ Обработка запроса к индексной странице """
    # Пример вызова метода с выборкой данных из БД и вставка полученных данных в html-шаблон
    processed_files = webservice.get_source_files_list()
    # "рендеринг" (т.е. вставка динамически изменяемых данных) в шаблон history.html и возвращение готовой страницы
    return render_template('history.html',
                           title='MY BEST WEBSERVICE!!!',
                           page_name='HISTORY',
                           navmenu=webservice.navmenu,
                           processed_files=processed_files)


@app.route('/contact', methods=['GET'])
def contact():
    """ Обработка запроса к странице contact.html """
    return render_template('contact.html',
                           title='Labs PIKPO',
                           page_name='CONTACT US',
                           navmenu=webservice.navmenu)


@app.route('/data/<int:source_file_id>', methods=['GET'])
def get_data(source_file_id: int):
    """
        Вывод данных по идентификатору обработанного файла.
        Функция также пытается получить значение GET-параметра pageNum
        из запроса типа: http://127.0.0.1:8000/data/16?pageNum=2
    """
    processed_data = []
    pageNum = request.args.get('pageNum')
    if pageNum is not None:
        processed_data = webservice.get_processed_data(source_file=source_file_id, page_num=int(pageNum))
    else:
        processed_data = webservice.get_processed_data(source_file=source_file_id)
    return render_template('data.html',
                           title='Labs PIKPO',
                           page_name=f'DATA_FILE_{source_file_id}',
                           navmenu=webservice.navmenu,
                           processed_data=processed_data)


@app.route('/api/contactrequest', methods=['POST'])
def post_contact():
    """ Пример обработки POST-запроса для демонстрации подхода AJAX (см. formsend.js и ЛР№5 АВСиКС) """
    request_data = request.json     # получаeм json-данные из запроса
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в этом объекте, например, не заполнено обязательное поле 'firstname'
    if not request_data or request_data['firstname'] == '':
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе отправляем json-ответ с сообщением об успешном получении запроса
    else:
        msg = request_data['firstname'] + ", ваш запрос получен !"
        return jsonify({'message': msg})


@app.route('/notfound', methods=['GET'])
def not_found_html():
    """ Возврат html-страницы с кодом 404 (Не найдено) """
    return render_template('404.html', title='404', err={'error': 'Not found', 'code': 404})


def bad_request():
    """ Формирование json-ответа с ошибкой 400 протокола HTTP (Неверный запрос) """
    return make_response(jsonify({'message': 'Bad request !'}), 400)
