from App import Generator
from pathlib import Path



SAVE_PATH: str = Path.home()
BUFFER:    int = 10

App = Generator(SAVE_PATH, BUFFER)


userList, v_min, v_max = App.getArguments()

arr:   list = App.getArrayValues(userList)
total: int  = App.calculateGeneratedSize(arr, v_min, v_max)

App.msg(f'Total elements: {total:_}', 'i')
App.msg('Do you want to continue? (y/n)', 'i')
ans = input()

if ans != 'y':
    App.msg('Terminating...', 'i', True)


App.generateNumbers(arr, v_min, v_max)
