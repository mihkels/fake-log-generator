from random import randint


def write_sleep(min_delay = 0, max_dealy = 0):
    ooutput = 0
    if min_delay == 0 and max_dealy == 0:
        return ooutput

    internal_max = valid_delay(max_dealy)
    internal_min = valid_delay(min_delay)
    if internal_max == 0 and internal_min != 0:
        internal_max = internal_min + 10

    return randint(internal_min, internal_max)


def valid_delay(num):
    if num > 0:
        return num
    else:
        return 0
