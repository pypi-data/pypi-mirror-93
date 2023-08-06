from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
from enum import Enum
from psutil import Process, NoSuchProcess
from asyncio import get_event_loop, sleep, iscoroutinefunction
# backwards compatibility in case used from Python < 3.7
try:
    from asyncio import create_task as _ensure_future
except ImportError:
    from asyncio import ensure_future as _ensure_future


class StopCondition(Enum):
    # this condition is too restrictive in most cases, as processes rarely keep handles open indefinitely
    FILE_CLOSED = 1
    PROCESS_STOPPED = 2


class AIORegexMatchingEventHandler(RegexMatchingEventHandler):
    def __init__(self, *args, handler, loop=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._loop = loop or get_event_loop()
        self._handler = handler

    def dispatch(self, event):
        # instead of dispatching to the appropriate handler, always dispatch to the same
        self._loop.call_soon_threadsafe(_ensure_future, self._handler(event))


class TextFileReader:
    def __init__(self, witness, src_path):
        self.witness = witness
        self.src_path = src_path
        self._reading = False

    async def start(self):
        self._reading = True
        with open(self.src_path, 'r') as f:
            while self._reading:
                line = f.readline()
                try:
                    if line != '':
                        if self.witness.handler_is_coro:
                            await self.witness.handler(self.src_path, line.strip('\n'))
                        else:
                            self.witness.handler(self.src_path, line.strip('\n'))
                    elif self.witness.stop_condition == StopCondition.PROCESS_STOPPED:
                        # check if the process isn't terminated, otherwise stop reading
                        if self.witness.process.status() == 'terminated':
                            await self.async_stop()
                        else:
                            await sleep(self.witness.read_period)
                    elif self.witness.stop_condition == StopCondition.FILE_CLOSED:
                        # check if the process still has an open file handle, otherwise stop reading
                        for open_file in self.witness.process.open_files():
                            if Path(open_file.path).samefile(self.src_path):
                                await sleep(self.witness.read_period)
                                break
                        else:
                            await self.async_stop()
                    else:
                        raise ValueError('Unknown stop condition.')
                except NoSuchProcess:
                    # if the process no longer exists, stop reading
                    await self.async_stop()

    def stop(self):
        self._reading = False
        self.witness.handler(self.src_path, None)

    async def async_stop(self):
        self._reading = False
        if self.witness.handler_is_coro:
            await self.witness.handler(self.src_path, None)
        else:
            self.witness.handler(self.src_path, None)


class FileWitness:
    def __init__(self, pid, root, file_regexes, handler,
                 stop_condition=StopCondition.PROCESS_STOPPED, obs_timeout=2, read_period=1, file_type='text',
                 **kwargs):
        self._pid = pid
        self._p = Process(self._pid)

        self._root = root
        self._regexes = file_regexes
        self._obs_timeout = obs_timeout

        self.handler = handler
        self.handler_is_coro = iscoroutinefunction(handler)

        self._wde = AIORegexMatchingEventHandler(self._regexes, handler=self._add_reader, **kwargs)
        self._reading = False
        self._file_type = file_type

        self.read_period = read_period
        self.stop_condition = stop_condition

        self._observer = Observer(self._obs_timeout)
        self._observer.schedule(self._wde, root)
        self._observer.start()

        self._readers = {}

    @property
    def process(self):
        return self._p

    async def async_stop(self, src_path=None):
        if src_path is None:
            for s, r in self._readers.items():
                await r.stop()
            self._observer.stop()
            self._observer.join()
        elif src_path not in self._readers:
            return
        else:
            await self._readers[src_path].stop()

    def stop(self, src_path=None):
        if src_path is None:
            for s, r in self._readers.items():
                r.stop()
            self._observer.stop()
            self._observer.join()
        elif src_path not in self._readers:
            return
        else:
            self._readers[src_path].stop()

    async def _add_reader(self, event):
        if event.src_path in self._readers:
            return
        if not event.is_directory:
            if self._file_type == 'text':
                self._readers[event.src_path] = TextFileReader(self, event.src_path)
                await self._readers[event.src_path].start()
