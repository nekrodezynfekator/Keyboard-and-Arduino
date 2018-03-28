import time
import serial
import pygame
import multiprocessing as mp

'''
Background (child) process to collect the data.
Main (paret) procesess to watch for keystrokes.
'''


def mp_data_collect(state, curr_time):

    ser = serial.Serial('/dev/ttyUSB0', 9600)

    while not terminate.is_set():

        dataSer = ser.readline()

        with open(output_path, 'a') as f:
            # TODO pass strip from child process (instead of `s`).
            row = '%s,%s,%s\n' % (dataSer, state.value, curr_time.value)
            f.write(row)

    ser.close()


output_path = 'test.txt'

terminate = mp.Event()

state = mp.Value('i', 0)
curr_time = mp.Value('i', 0)

# `state` should be like:
# state = mp.Value('c', 0)
# But i don't know how to get `1 byte char` in python.
# See:
# https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Value
# and:
# https://docs.python.org/2/library/array.html#module-array

collector = mp.Process(name='proc_acq', target=mp_data_collect,
                       args=(state, curr_time,))
collector.start()


pygame.init()
time.sleep(2)
print('started')

start = time.time()

screen = pygame.display.set_mode((50, 50))
while not terminate.is_set():
    # FIXME in milliseconds so that it can be stored as int, now it will
    # throw an error.
    curr_time.value = '%.4f' % (time.time()-start)
    # FIXME: doesn't listens keystrokes, I don't know why yet.
    # It has sth to with the way int is stored in the `state` variable.
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                state.value = 1
            elif event.key == pygame.K_m:
                state.value = 2
                terminate.set()
        else:
            state.value = 0

collector.join()
pygame.quit()
