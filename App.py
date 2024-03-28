from string import ascii_lowercase, ascii_uppercase
from sys import argv
from os import stat
from itertools import product
from timeit import default_timer
from time import process_time


class Generator():
    def __init__(self, savePath: str, buffer: int = 10):
        self._generatedCombos = []
        self._generatedSize   = 0
        self._buffer          = buffer
        self._savePath        = savePath


    def _appendToFile(self, file_path: str, currentNum: int) -> None:
        with open(file_path, 'a') as file:
            file.write('\n'.join(self._generatedCombos) + '\n')

        self.msg(f'{currentNum} / {self._generatedSize}', 'w')
        self._generatedCombos.clear()

    def _getFileSize(self, file_path: str) -> str:
        total_bytes: int = stat(file_path).st_size
        MiB:         int = 2**20

        if total_bytes >= MiB:
            return f'{round(total_bytes / MiB)}MiB'

        return f'{round(total_bytes / 2**10)}KiB' 




    def msg(self, string: str, itype: str = 'e', terminate: bool = False) -> None:
        match(itype):
            case 'i':     itype = 'INFO'
            case 'w':     itype = 'WRITING'
            case 'e' | _: itype = 'ERROR'

        print(f'[{itype}] {string}')

        if terminate or itype == 'ERROR':
            exit(1)


    def getArguments(self) -> list[any, int, int]:
        if len(argv) != 4:
            self.msg('Usage: python3 index.py <arr> <min> <max>')

        _, arr, v_min, v_max = argv

        try:
            v_min = int(v_min)
            v_max = int(v_max)

        except (AttributeError, ValueError):
            self.msg('<min> and/or <max> are not numeric values')


        if (
            v_min <= 0 or 
            v_max <= 0 or
            v_max < v_min
        ):
            self.msg('<min> and/or <max> are incorrect')


        return [arr, v_min, v_max]


    def calculateGeneratedSize(self, arr: list, minv: int, maxv: int) -> int:
        self._generatedSize = sum([ len(arr) ** x for x in range(minv, maxv + 1) ]) 

        return self._generatedSize


    def generateNumbers(self, arr: list, minv: int, maxv: int) -> None:
        self.msg('Saving data...', 'i')

        if not self._generatedSize:
            self.calculateGeneratedSize(arr, minv, maxv)

        wt: float = default_timer()
        ct: float = process_time() 

        self.msg(f'0 / {self._generatedSize}', 'w')

        currentNum: int = 0
        BUFF:       int = self._generatedSize // self._buffer
        filename:   str = f'wordlist_{self._generatedSize}.txt'
        FULL_PATH:  str = f'{self._savePath}/{filename}'

        for current_it in range(minv, maxv + 1):
            for combo in product(arr, repeat=current_it):
                self._generatedCombos.append(''.join(combo))

                if len(self._generatedCombos) >= BUFF:
                    currentNum += BUFF
                    self._appendToFile(FULL_PATH, currentNum)

        if len(self._generatedCombos):
            self._appendToFile(FULL_PATH, self._generatedSize)


        total_value: str = self._getFileSize(FULL_PATH)

        self.msg(f'Finished generating "{filename}". Total file size: {total_value}', 'i')
        self.msg(f'Execution time: {round(default_timer() - wt, 4)}s', 'i')
        self.msg(f'CPU time: {round(process_time() - ct, 4)}s', 'i')


    def getArrayValues(self, userList: str) -> list:
        match userList:
            case 'num':
                return [num for num in range(0, 10)]

            case 'alphalower':
                return ascii_lowercase

            case 'alphaupper':
                return ascii_uppercase
                
            case _:
                s = userList.split(',')

                if any(len(val) != 1 for val in s):
                    self.msg(f'Incorrect array value (got: {userList})')

                return s