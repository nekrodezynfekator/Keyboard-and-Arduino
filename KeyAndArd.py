import time
import serial
import pygame
import multiprocessing as mp


def mp_data_collect(state, curr_time):

    ser = serial.Serial('/dev/ttyACM0', 9600)

    while not terminate.is_set():

        dataSer = ser.readline()

        with open(output_path, 'a') as f:
            row = '%s,%s,%s\n' % (dataSer.strip(), state.value, curr_time.value)
            f.write(row)

    ser.close()


output_path = 'test.txt'

terminate = mp.Event()

state = mp.Value('i', 0)
curr_time = mp.Value('i', 0)

collector = mp.Process(name='proc_acq', target=mp_data_collect,
                       args=(state, curr_time,))
collector.start()

pygame.init()
time.sleep(2)
print('started')

start = time.time()

screen = pygame.display.set_mode((50, 50))
while not terminate.is_set():
    curr_time.value = int(round((time.time()-start)*1000, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                state.value = 1
            elif event.key == pygame.K_w:
                state.value = 2
            elif event.key == pygame.K_e:
                state.value = 3
            elif event.key == pygame.K_a:
                state.value = 4
            elif event.key == pygame.K_s:
                state.value = 5
            elif event.key == pygame.K_d:
                state.value = 6
            elif event.key == pygame.K_m:
                state.value = 7
                terminate.set()
        else:
            state.value = 0

collector.join()
pygame.quit()
