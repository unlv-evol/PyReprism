"""Ordered parallel map over files, used by batch processing and clone detection.

Files are analyzed independently, so work is spread over processes (threads
would serialize on the interpreter lock). Results come back in input order,
so parallel and serial runs return identical reports.
"""
import os
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Iterable, List, Optional, TypeVar

T = TypeVar('T')
R = TypeVar('R')

# Below this many items, starting worker processes costs more than it saves.
MIN_PARALLEL_ITEMS = 64


def resolve_jobs(jobs: Optional[int]) -> int:
    """``None`` or ``0`` means one worker per CPU; otherwise at least 1."""
    if not jobs:
        return os.cpu_count() or 1
    return max(1, int(jobs))


def pmap(fn: Callable[[T], R], items: Iterable[T], jobs: Optional[int] = 1) -> List[R]:
    """``[fn(x) for x in items]``, in order, over ``jobs`` processes.

    ``fn`` and the items must be picklable (e.g. a module-level function).
    """
    items = list(items)
    workers = min(resolve_jobs(jobs), len(items))
    if workers <= 1 or len(items) < MIN_PARALLEL_ITEMS:
        return [fn(x) for x in items]
    chunksize = max(1, len(items) // (workers * 8))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(fn, items, chunksize=chunksize))


def language(name: str):
    """Resolve a language class by its class name inside a worker process."""
    from .languages.registry import LanguageRegistry
    cls = LanguageRegistry.get(name)
    if cls is None:
        from .languages import _load_all_languages
        _load_all_languages()
        cls = LanguageRegistry.get(name)
    return cls
