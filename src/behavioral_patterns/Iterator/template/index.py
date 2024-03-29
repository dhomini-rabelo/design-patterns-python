from typing import Tuple


from collections.abc import Iterable, Iterator


class PaginatorIterator(Iterator):
    def __init__(self, paginator: 'Paginator'):
        self.__paginator = paginator
        self.__position = 1

    def __next__(self):
        try:
            value = self.__getitem__(self.__position)
            self.__position += 1
        except IndexError:
            raise StopIteration()

        return value

    def __getitem__(self, input_page: int) -> Tuple[int, int]:
        page = input_page - 1
        start = (page * self.__paginator._step) + 1
        end = (page + 1) * self.__paginator._step
        length = self.__paginator._length
        if input_page <= 0:
            raise IndexError('The pagination starts with 1')
        elif end < length:
            return (start, end)
        elif start < length:
            return (start, length)
        else:
            raise IndexError(f'{length} was surpassed')


class Paginator(Iterable):
    def __init__(self, step: int, length: int) -> None:
        self._step = step
        self._length = length

    def __iter__(self) -> PaginatorIterator:
        return PaginatorIterator(self)

    def __getitem__(self, page: int):
        return PaginatorIterator(self).__getitem__(page)


paginator = Paginator(7, 20)

for index, (start, end) in enumerate(paginator):
    print(f'page: {index+1:>2}; start: {start:>2}; end: {end:>2}')

print(f'page 2: {paginator[2]}')
