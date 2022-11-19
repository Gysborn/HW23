from typing import Iterable, Iterator, Set, Union, List, Generator, Any, Sequence

from flask import abort, Response
import re


def regex_query(param: str, data: Iterable[str]) -> Iterator[str]:
    return filter(lambda x: re.findall(param, x), data)


def file_iter(file_name: str) -> Generator:
    """

    :param file_name: Имя файла
    :return: Возвращает построчно файл
    """
    try:
        with open(file_name) as f:
            for row in f:
                yield row
    except FileNotFoundError:
        abort(Response('File Not found', 400))


def filter_query(param: str, data: Iterable[str]) -> Iterator[str]:
    return filter(lambda x: param in x, data)


def map_query(param: int, data: Iterable[str]) -> Iterator[str]:
    try:
        param = int(param)
    except ValueError:
        abort(Response(f'Некорректный параметр {param}'))

    return map(lambda x: x.split(' ')[param], data)


def unique_query(*args, data: Iterable[str]) -> Set[str]:
    return set(data)


def sort_query(param: str, data: Iterable[str]) -> Iterable[str]:
    if param != 'desc':
        return sorted(data, reverse=True)
    else:
        return sorted(data, reverse=False)


def limit_query(param: int, data: Sequence) -> Sequence:
    try:
        param = int(param)
    except ValueError:
        abort(Response(f'Некорректный параметр {param}'))
    return data[:param]


class Validator:
    def __init__(self, query1, query2):
        self.query1 = list(filter(lambda x: x is not None, query1))  # Удаляем пустые поля запроса
        self.query2 = list(filter(lambda x: x is not None, query2))
        self.CMD = ['filter', 'map', 'limit', 'unique', 'sorted', 'regex']

    def _empty_valid(self, value: Union[str, int]) -> bool:  # Проверка налиячия запроса
        if not value:
            return False
        return True

    def _not_complete(self, value: list) -> bool:  # Проверка целостности запроса (команда/значение)
        if len(value) != 2:
            return False
        return True

    def _validation(self, value: Union[Any]) -> Union[Any]:  # Проверка на существование комманд
        if not self._empty_valid(value):
            return False
        elif not self._not_complete(value):
            abort(Response('Некорректный запрос', 400))
        elif value[0] in self.CMD:
            return value
        else:
            abort(Response('Некорректный запрос', 400))

    def complete(self) -> List[Any]:  # Итоговая проверка и вывод листа запросов
        """

        :return: Возвращает лист проверенных запросов
        """
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
