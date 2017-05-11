from random import randint
import os


def write_log_directory(output_dir = ''):
    if output_dir == '':
        return output_dir

    if not output_dir.endswith(os.sep):
        output_dir += os.sep

    if os.path.isabs(output_dir) and not os.path.exists(output_dir):
        print('No such directory: %s. Please create it will fallback to current directory', output_dir)
        return ''

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return output_dir


def write_sleep(min_delay = 0, max_dealy = 0):
    if min_delay == 0 and max_dealy == 0:
        return 0

    max_dealy = valid_delay(max_dealy)
    min_delay = valid_delay(min_delay)
    if max_dealy == 0 and min_delay != 0:
        max_dealy = + 10

    return randint(min_delay, max_dealy)


def valid_delay(num):
    return num if num > 0 else 0
