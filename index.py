from App import Generator


SAVE_PATH: str = '/home/vrecek/Downloads'
App = Generator(SAVE_PATH)

userList, v_min, v_max = App.getArguments()

arr:   list = App.getArrayValues(userList)
total: int  = App.calculateGeneratedSize(arr, v_min, v_max)

App.msg(f'Total elements: {total:_}', 'i')
App.msg('Do you want to continue? (y/n)', 'i')
ans = input()

if ans != 'y':
    App.msg('Terminating...', 'i', True)


App.generateNumbers(arr, v_min, v_max)
