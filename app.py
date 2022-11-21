import os
from typing import Mapping, Callable

from flask import Flask, request, jsonify


from utils import file_iter, filter_query, map_query, limit_query, unique_query, sort_query, Validator, regex_query

FILE_NAME = 'data/apache_logs.txt'


CMD_OF_FUNC: Mapping[str, Callable] = {
    'filter': filter_query,
    'map': map_query,
    'limit': limit_query,
    'unique': unique_query,
    'sorted': sort_query,
    'regex': regex_query
}

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def query_compiler(qwe: list) -> list: # Обработчик/компановщик запросов
    it = file_iter(FILE_NAME)
    cmd1 = qwe[0]
    it = CMD_OF_FUNC[cmd1[0]](cmd1[1], data=it) # Словарь в котором значениями являются объекты функций вызываемые по ключу
    if len(qwe) == 2: # Проверка на кол. запросов
        cmd2 = qwe[1]
        it = CMD_OF_FUNC[cmd2[0]](cmd2[1], data=it)
    res = list(it)
    return res


@app.route("/perform_query", methods=['POST'])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    query1 = [request.args.get('cmd1'), request.args.get('value1')]
    query2 = [request.args.get('cmd2'), request.args.get('value2')]
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    validator = Validator(query1, query2)
    res = query_compiler(validator.complete())

    return jsonify(res)


if __name__ == "__main__":
    app.run()
