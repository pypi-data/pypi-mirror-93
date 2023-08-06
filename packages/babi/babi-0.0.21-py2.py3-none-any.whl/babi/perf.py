import contextlib
import cProfile
import time
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple


class Perf:
    def __init__(self) -> None:
        self._prof: Optional[cProfile.Profile] = None
        self._records: List[Tuple[str, float]] = []
        self._name: Optional[str] = None
        self._time: Optional[float] = None

    def start(self, name: str) -> None:
        if self._prof:
            assert self._name is None, self._name
            self._name = name
            self._time = time.monotonic()
            self._prof.enable()

    def end(self) -> None:
        if self._prof:
            assert self._name is not None
            assert self._time is not None
            self._prof.disable()
            self._records.append((self._name, time.monotonic() - self._time))
            self._name = self._time = None

    def init_profiling(self) -> None:
        self._prof = cProfile.Profile()
        self.start('startup')

    def save_profiles(self, filename: str) -> None:
        assert self._prof is not None
        self._prof.dump_stats(f'{filename}.pstats')
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write('μs\tevent\n')
            for name, duration in self._records:
                f.write(f'{int(duration * 1000 * 1000)}\t{name}\n')


@contextlib.contextmanager
def perf_log(filename: Optional[str]) -> Generator[Perf, None, None]:
    perf = Perf()
    if filename is None:
        yield perf
    else:
        perf.init_profiling()
        try:
            yield perf
        finally:
            perf.end()
            perf.save_profiles(filename)
