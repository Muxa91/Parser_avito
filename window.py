import tkinter as tk
import parserAvito
from time import sleep
import threading
from datetime import datetime

root = tk.Tk()
root.title('Сканер Авито')
root.geometry('420x190+300+300')
root.resizable(False, False)
checking_parser = True


def start_parser():
    find = find_string.get()
    value_cost_min = cost_min.get()
    value_cost_max = cost_max.get()
    value_sleep = sleep_timer.get()
    global checking_parser
    checking_parser = True
    btm_start_parser['state'] = ['disabled']
    while checking_parser is True:
        parserAvito.AvitoParser().parse_all_pages(find_string=find,
                                                  cost_min=int(value_cost_min),
                                                  cost_max=int(value_cost_max)
                                                  )
        time_of_pars.config(text=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        sleep(int(value_sleep) * 60)


def stop_parser():
    btm_start_parser['state'] = ['normal']
    global checking_parser
    checking_parser = False


def callback(value):
    if value.isdigit() or value == "":
        return True
    else:
        return False


vcmd = root.register(callback)  # validatecommand for Entry

tk.Label(root, text='Ввод для поиска   ').grid(row=0, column=0, stick='w', pady=3, padx=3)
find_string = tk.Entry(root, width='40')
find_string.insert(0, 'раздатка даймос уаз бу')
find_string.grid(row=0, column=1, stick='w', columnspan=4)

tk.Label(root, text='Максимальная цена').grid(row=1, column=0, stick='w', pady=3, padx=3)
tk.Label(root, text='Руб.').grid(row=1, column=2, stick='w')
cost_max = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
cost_max.insert(0, '10000')
cost_max.grid(row=1, column=1, stick='w')

tk.Label(root, text='Минимальная цена    ').grid(row=2, column=0, stick='w', pady=3, padx=3)
tk.Label(root, text='Руб.').grid(row=2, column=2, stick='w')
cost_min = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
cost_min.insert(0, '0')
cost_min.grid(row=2, column=1, stick='w')

tk.Label(root, text='Сканировать каждые ').grid(row=3, column=0, stick='w', pady=3, padx=3)
tk.Label(root, text='Мин.').grid(row=3, column=2, stick='w')
sleep_timer = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
sleep_timer.insert(0, '30')
sleep_timer.grid(row=3, column=1, stick='w')

btm_start_parser = tk.Button(root, text='Сканирование',
                             command=lambda: threading.Thread(target=start_parser, daemon=True).start())
btm_start_parser.grid(row=4, column=0, stick='w', pady=3, padx=15)

btm_stop_parser = tk.Button(root, text='Отмена', command=stop_parser)
btm_stop_parser.grid(row=5, column=0, stick='w', pady=3, padx=15)

tk.Label(root, text=f'Последнее сканирование').grid(row=4, column=1, stick='w')
time_of_pars = tk.Label(root, text='')
time_of_pars.grid(row=4, column=2, stick='w')
root.parserAvitoloop()
