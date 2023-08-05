import os
import psutil
import resource
import tracemalloc

# https://habr.com/ru/post/316806/
# https://pymotw.com/2/resource/
# https://docs.python.org/3.6/library/resource.html#resource-usage
# https://rtfm.co.ua/unix-raznica-mezhdu-virt-res-shr-i-swap-pamyatyu-d-rezultatx-top-i-ps/
# https://coderoad.ru/938733/%D0%9E%D0%B1%D1%89%D0%B0%D1%8F-%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D0%B5%D0%BC%D0%B0%D1%8F-%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%BC-Python
# https://medium.com/survata-engineering-blog/monitoring-memory-usage-of-a-running-python-program-49f027e3d1ba
# http://www-h.eng.cam.ac.uk/help/languages/python/pythonmemory.html


current_snapshot = None
prev_snapshot = None
_print = str


def set_print(new_print):
    global _print
    _print = new_print


def start_tracemalloc():
    tracemalloc.start()


def stop_tracemalloc():
    tracemalloc.stop()


def tracemalloc_take_snapshot(compare=True):
    # import copy
    global current_snapshot, prev_snapshot
    if current_snapshot is not None:
        prev_snapshot = current_snapshot

    current_snapshot = tracemalloc.take_snapshot()
    if compare:
        if prev_snapshot is not None:
            stats = current_snapshot.compare_to(prev_snapshot, 'filename')
            for i, stat in enumerate(stats[:5], 1):
                _print(f'since_start {i}: {str(stat)}')


def format_dec(_val, _dec=2):
    dec_proto = '{' + f'val:,.{_dec}f' + '}'
    dec_str = dec_proto.format(val=_val).replace(',', '`')
    return dec_str


def memory_usage():
    kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    pagesize = resource.getpagesize()
    _print(f'Memory usage : {format_dec(kb)} (kb); {format_dec(kb / 1024)} (mb); '
           f'pagesize: {format_dec(pagesize)}')


def memory_info(_pid=None, prefix='', print_out=False):
    _pid = os.getpid() if not _pid else _pid
    process = psutil.Process(_pid)
    memory_info = process.memory_info()
    print_string = (f'{prefix}'
                    f'pid: {_pid}; '
                    f'VIRT: {format_dec(memory_info.vms / 1024 / 1024)} (mb); '
                    f'RES: {format_dec(memory_info.rss / 1024 / 1024)} (mb); '
                    f'SHR: {format_dec(memory_info.shared / 1024 / 1024)} (mb)')
    if print_out:
        _print(print_string)
    return print_string
