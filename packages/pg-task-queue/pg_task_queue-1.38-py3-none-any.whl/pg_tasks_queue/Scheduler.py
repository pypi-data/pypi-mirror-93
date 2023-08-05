import sys
import time
import datetime
import signal
import os
import json
import copy
import multiprocessing
import importlib.util
from croniter import croniter
from pg_tasks_queue.Config import cfg as config
from pg_tasks_queue.Logging import init_logger
import pg_tasks_queue.Database as database
import pg_tasks_queue.procinfo as procinfo

import logging
logger = logging.getLogger(__name__)


name = 'Scheduler'
ver = '1.1'
release_date = '2020-07-03 10:00'
version = f'"{name}" ver: {ver} ({release_date})'

_print = print


def set_print(new_print):
    global _print
    _print = new_print


class Scheduler:

    _started = False
    _workers = list()
    _pid = None

    def signal_handler(self, _sig_num, frame):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        _print(f'{func_name}; received: {_sig_num}; ; pid={os.getpid()}; '
               f'self._pid={self._pid}; frame: {frame}')
        if self._pid == os.getpid():
            _print('Set self._started = False')
            self._started = False

    def check_module(self, module_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        module_spec = importlib.util.find_spec(module_name)
        if module_spec is None:
            logger.error(f'Error in {func_name}: module: "{module_name}" not found')
            return None
        else:
            return module_spec

    def import_module(self, module_name):
        module_spec = self.check_module(module_name)
        if module_spec is None:
            return None
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def import_function_from_module(self, module_name, function_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        module = self.import_module(module_name)
        if module is None:
            return None
        if not hasattr(module, function_name):
            logger.error(f'Error in {func_name}: module: "{module_name}"; '
                         f'function: "{function_name}" not found')
            return None
        return getattr(module, function_name)

    def worker(self, task_dict):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        _print(f'{func_name}; os.getpid(): {os.getpid()}; os.getppid(): {os.getppid()}')
        task_module = task_dict.get('module')

        task_func = task_dict.get('func')
        func = self.import_function_from_module(task_module, task_func)
        if func is None:
            error = f'Error in {func_name}: ' \
                    f'import_function_from_module({task_module}, {task_func}) is None'
            logger.error(error)
            return {'status': 'error', 'result': error}
        else:
            params = task_dict.get('params')
            if isinstance(params, str):
                params = json.loads(params)
            if not isinstance(params, dict):
                params = dict()
            logger.info(f'Started task (id={task_dict.get("task_id")}) '
                        f'at {datetime.datetime.now()}; task_dict: {task_dict}')
            res = func(**params)
            logger.info(f'Finished task (id={task_dict.get("task_id")}) '
                        f'at {datetime.datetime.now()}; result: {res}')
            return res

    def worker_process(self, queue, task_dict):
        result = self.worker(task_dict)
        _print(f'result({task_dict.get("task_id")}): {result}')
        queue.put(result)

    def update_tasks(self):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        now = datetime.datetime.now()
        _print(f'Start {func_name} at {now}')

        cronjob_tasks = database.get_cronjob_tasks()
        if not isinstance(cronjob_tasks, list):
            error = f'Error in {func_name}: not isinstance(cronjob_tasks, list)...'
            logger.error(error)
            return error

        start_of_min = datetime.datetime.strptime(now.strftime('%Y-%m-%d %H:%M:00'), '%Y-%m-%d %H:%M:00')

        for cronjob_task in cronjob_tasks:

            itr = croniter(cronjob_task.schedule, start_of_min)
            scheduled_time = itr.get_next(datetime.datetime)

            task = database.get_task_for_cronjob(cronjob_task, start_of_min)

            if task is None:

                # _print(f'{func_name}; apply cronjob_task   : {cronjob_task}')
                cronjob_task.last_start_time = cronjob_task.next_start_time
                cronjob_task.next_start_time = scheduled_time
                cronjob_task = database.update(cronjob_task)
                # _print(f'{func_name}; updated cronjob_task : {cronjob_task}')

                new_task_dict = {'priority': 1,
                                 'create_time': start_of_min,
                                 'scheduled_time': scheduled_time,
                                 'cronjob_task_id': cronjob_task.task_id}

                task_columns = list(database.get_table_columns(database.Task()).keys())
                task_columns.remove('task_id')
                for task_column in task_columns:
                    if task_column in cronjob_task.__table__.columns:
                        new_task_dict[task_column] = getattr(cronjob_task, task_column)
                new_task = database.add_task(new_task_dict)
                logger.info(f'{func_name}; create new task: {new_task}')

        return None

    def start(self, cfg=None, config_id=None):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'

        init_logger()
        logger.warning(f'Start {version}')

        self._pid = os.getpid()
        logger.warning(f"Started {func_name} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}; "
                       f"{procinfo.memory_info()}")

        id_counter = 0
        write_config = True
        print_func = 'print'
        pool_size = 2
        kill_timeout_sec = 30.
        sleep_sec = 5.
        raise_exception = False

        try:

            if not cfg:
                if not isinstance(config.cfg, dict):
                    logger.error(f'Error in {func_name}: not isinstance(config.cfg, dict)...')
                    return
                cfg = config.cfg
            logger.warning(f'cfg: {cfg}')

            database_cfg = cfg.get('database')
            if not database.init(database_cfg):
                logger.error(f'Error in {func_name}: not database.init()...')
                return

            scheduler_cfg = cfg.get('scheduler')
            scheduler_cfg = dict() if not isinstance(scheduler_cfg, dict) else scheduler_cfg
            if 'pool_size' in scheduler_cfg:
                scheduler_cfg['pool_size'] = int(scheduler_cfg.get('pool_size'))
            if 'kill_timeout_sec' in scheduler_cfg:
                scheduler_cfg['kill_timeout_sec'] = float(scheduler_cfg.get('kill_timeout_sec'))
            if 'sleep_sec' in scheduler_cfg:
                scheduler_cfg['sleep_sec'] = float(scheduler_cfg.get('sleep_sec'))
            if 'write_config' in scheduler_cfg:
                if isinstance(scheduler_cfg.get('write_config'), bool):
                    write_config = scheduler_cfg.get('write_config')

            if write_config:
                if config_id is None:
                    if database_cfg.get('project') is None:
                        config_id = 'scheduler.all'
                    else:
                        config_id = f"scheduler.{database_cfg.get('project')}"

                db_cfg = database.get_config(config_id)
                if db_cfg is None:
                    write_cfg = copy.deepcopy(scheduler_cfg)
                    if 'write_config' in write_cfg:
                        del write_cfg['write_config']
                    db_cfg = database.Config(config_id=config_id, config=write_cfg)
                    database.add_new_record(db_cfg, database.Config)
                else:
                    for key in scheduler_cfg.keys():
                        if key in db_cfg.config:
                            scheduler_cfg[key] = db_cfg.config.get(key)
                    for key in db_cfg.config.keys():
                        if key not in scheduler_cfg:
                            scheduler_cfg[key] = db_cfg.config.get(key)

            if 'pool_size' in scheduler_cfg:
                pool_size = scheduler_cfg.get('pool_size')
            if 'kill_timeout_sec' in scheduler_cfg:
                kill_timeout_sec = scheduler_cfg.get('kill_timeout_sec')
            if 'sleep_sec' in scheduler_cfg:
                sleep_sec = scheduler_cfg.get('sleep_sec')
            if 'print_func' in scheduler_cfg:
                print_func = scheduler_cfg.get('print_func')
                if print_func is None:
                    set_print(str)
                elif print_func == 'logger.warning':
                    set_print(logger.warning)
                elif print_func == 'logger.info':
                    set_print(logger.info)
                elif print_func == 'print':
                    set_print(print)
                else:
                    logger.warning(f'{func_name}: unknown print func.: {print_func}')

            logger.warning(f'pool_size: {pool_size}; '
                           f'sleep_sec: {sleep_sec}; '
                           f'kill_timeout_sec: {kill_timeout_sec}; '
                           f'print_func: {print_func}; '
                           f'write_config: {write_config}; '
                           f'config_id: {config_id}')

            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)

            def update_worker_queue(_worker_dict):
                _worker_id = _worker_dict.get('id')
                _queue = _worker_dict.get('queue')
                _task = _worker_dict.get('task')
                if not _queue.empty():
                    _result = _queue.get_nowait()
                    _print(f'worker({_worker_id}): queue.get_nowait(): {_result}')
                else:
                    error = f'Error in {func_name}: worker({_worker_id}) queue is empty()...'
                    logger.error(error)
                    _result = {'status': 'error', 'result': error}
                database.update_worker_task(_result, _task, None)

            self._started = True
            _last_updated_tasks = None
            while self._started:

                now = datetime.datetime.now()
                _print(f"Start cycle at {now.strftime('%Y-%m-%d %H:%M:%S')}; {procinfo.memory_info()}")

                # == update cronjobs

                start_of_min = datetime.datetime.strptime(now.strftime('%Y-%m-%d %H:%M:00'), '%Y-%m-%d %H:%M:00')
                if _last_updated_tasks is not None:
                    if _last_updated_tasks != start_of_min:
                        _last_updated_tasks = None

                if _last_updated_tasks is None:
                    self.update_tasks()
                    _last_updated_tasks = start_of_min

                # == delete finished workers from workers list

                workers_count = len(self._workers)
                for i in range(workers_count):
                    counter = workers_count - i - 1
                    worker_dict = self._workers[counter]
                    worker = worker_dict.get('worker')
                    worker_id = worker_dict.get('id')
                    if worker.is_alive():
                        _print(f'worker({worker_id}) is alive')
                    else:
                        update_worker_queue(worker_dict)
                        _print(f'remove worker({worker_id})')
                        del self._workers[counter]

                # == start new workers processes

                free_workers = pool_size - len(self._workers)
                if free_workers > 0:
                    new_tasks = database.get_new_tasks(free_workers)
                    for task in new_tasks:
                        task.started_time = now
                        database.update(task)
                        task_dict = database.get_record_dict(task)
                        queue = multiprocessing.Queue()
                        worker = multiprocessing.Process(target=self.worker_process,
                                                         args=(queue, task_dict,))
                        id_counter += 1
                        worker_dict = {'id': id_counter,
                                       'started': datetime.datetime.now(),
                                       'worker': worker,
                                       'queue': queue,
                                       'task': task}
                        self._workers.append(worker_dict)
                        _print(f'Start worker({id_counter})')
                        worker.start()
                        time.sleep(0.5)

                # _print(f'Waiting {self._sleep_sec} sec.; now: {datetime.datetime.now()}')
                time.sleep(sleep_sec)

            logger.info(f"{func_name}; end while loop; "
                        f"waiting kill_timeout_sec: {kill_timeout_sec} sec.; "
                        f"now: {now.strftime('%Y-%m-%d %H:%M:%S')}; "
                        f"{procinfo.memory_info()}")
            time.sleep(kill_timeout_sec)

            for worker_dict in self._workers:
                worker = worker_dict.get('worker')
                worker_id = worker_dict.get('id')
                if worker.is_alive():
                    error = f'Error in {func_name}: ' \
                            f'worker({worker_id}).is_alive() => worker.terminate()'
                    logger.error(error)
                    worker.terminate()
                    _task = worker_dict.get('task')
                    database.update_worker_task({'status': 'error', 'result': error}, _task, None)
                else:
                    update_worker_queue(worker_dict)

        except Exception as e:
            logger.exception(f'Error in {func_name}: {type(e)}: {str(e)}...')
            if raise_exception:
                raise e
        finally:
            logger.warning(f"End {func_name} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}; "
                           f"{procinfo.memory_info()}")


if __name__ == '__main__':
    Scheduler().start()
