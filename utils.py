from flask import abort, Response


def file_iter(file_name):
    try:
        with open(file_name) as f:
            for row in f:
                yield row
    except:
        abort(Response('File Not found', 400))


def filter_query(param: str, data):
    return filter(lambda x: param in x, data)


def map_query(param: str, data):
    try:
        param = int(param)
    except:
        abort(Response(f'Некорректный параметр {param}'))

    return map(lambda x: x.split(' ')[param], data)


def unique_query(*args, data):
    return set(data)


def sort_query(param: str, data):
    if param == 'desc':
        param = False
    else:
        param = True
    return sorted(data, reverse=param)


def limit_query(param: str, data): #
    try:
        param = int(param)
    except:
        abort(Response(f'Некорректный параметр {param}'))
    return data[:param]


class Validator:
    def __init__(self, query1, query2):
        self.query1 = list(filter(lambda x: x is not None, query1)) # Удаляем пустые поля запроса
        self.query2 = list(filter(lambda x: x is not None, query2))
        self.CMD = ['filter', 'map', 'limit', 'unique', 'sorted']

    def _empty_valid(self, value): # Проверка налиячия запроса
        if not value:
            return False
        return True

    def _not_complete(self, value): # Проверка целостности запроса (команда/значение)
        if len(value) != 2:
            return False
        return True

    def _validation(self, value): # Проверка на существование комманд
        if not self._empty_valid(value):
            return False
        elif not self._not_complete(value):
            abort(Response('Некорректный запрос', 400))
        elif value[0] in self.CMD:
            return value
        else:
            return abort(Response('Некорректный запрос', 400))

    def complete(self): # Итоговая проверка и вывод листа запросов
        result = []
        res1 = self._validation(self.query1)
        res2 = self._validation(self.query2)
        if res1:
            result.append(res1)
        if res2:
            result.append(res2)
        if not len(result):
            abort(Response('Пустой запрос', 400))
        return result
