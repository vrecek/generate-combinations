from string import ascii_lowercase, ascii_uppercase
from sys import argv
from os import stat
from itertools import product


class Generator():
    def __init__(self, savePath: str):
        self._generatedCombos = []
        self._generatedSize   = 0
        self._savePath        = savePath


    def _appendToFile(self, file_path: str, current: int) -> None:
        with open(file_path, 'a') as file:
            file.write('\n'.join(self._generatedCombos) + '\n')


        self.msg(f'{current} / {self._generatedSize}', 'w')
        self._generatedCombos.clear()



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


        self.msg(f'0 / {self._generatedSize}', 'w')

        currentNum: int = 0
        BUFF:       int = self._generatedSize // 10
        filename:   str = f'wordlist_{self._generatedSize}.txt'
        FULL_PATH:  str = f'{self._savePath}/{filename}'

        for current_it in range(minv, maxv + 1):
            for combo in product(arr, repeat=current_it):
                self._generatedCombos.append(''.join(combo))

                if len(self._generatedCombos) >= BUFF:
                    currentNum += BUFF
                    self._appendToFile(FULL_PATH, currentNum)


        if len(self._generatedCombos):
            currentNum = self._generatedSize
            self._appendToFile(FULL_PATH, currentNum)


        total_bytes: int = stat(FULL_PATH).st_size
        MiB:         int = 2**20

        if total_bytes >= MiB:
            total_value = f'{round(total_bytes / MiB)}MiB'
        else:
            total_value = f'{round(total_bytes / 2**10)}KiB' 


        self.msg(f'Finished generating "{filename}". Total file size: {total_value}', 'i')



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