# -*- coding: utf-8 -*-

from time import sleep

# Print iterations progress
import sys

import os


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    # str_format = "{0:." + str(decimals) + "f}"
    # percents = str_format.format(100 * (iteration / float(total)))
    # filled_length = int(round(length * iteration / float(total)))
    # bar = '█' * filled_length + '-' * (length - filled_length)
    # sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    # if iteration == total:
    #     sys.stdout.write('\n')
    percents = f'{100 * (iteration / float(total)):.2f}'
    # "{0:." + str(decimals) + "f}"
    # percents = str_format.format(100 * (iteration / float(total)))

    filled_length = int(round(length * iteration / float(total)))
    bar = f'{"█" * filled_length}{"-" * (length - filled_length)}'
    # '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write(f'\r{prefix} |{bar}| {percents}% {suffix}'),
    # '\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)
    sys.stdout.flush()


#
# Sample Usage
#
if __name__ == '__main__':
    # A List of Items
    items = list(range(0, 57))
    l = len(items)

    # Initial call to print 0% progress
    print_progress(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, item in enumerate(items):
        # Do stuff...
        sleep(0.1)
        sys.stdout.write(f'\r\r{i}{os.linesep}')
        sys.stdout.flush()
        # Update Progress Bar
        print_progress(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
