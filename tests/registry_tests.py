from typing import Generator

import pytest

from fastapi_cache_plus import close_caches
from fastapi_cache_plus.backends.memory import CACHE_KEY, InMemoryCacheBackend
from fastapi_cache_plus.registry import CacheRegistry


@pytest.fixture
def cache_registry() -> Generator[CacheRegistry, None, None]:
    registry = CacheRegistry()
    yield registry
    registry.flush()


def test_get_from_registry_should_return_none_if_cache_not_registered(
    cache_registry: CacheRegistry,
) -> None:
    assert cache_registry.get("") is None


def test_get_from_registry_should_return_cache_instance(
    cache_registry: CacheRegistry,
) -> None:
    cache = InMemoryCacheBackend()
    cache_registry.set(CACHE_KEY, cache)
    assert cache_registry.get(CACHE_KEY) == cache


def test_retrieve_all_registered_caches_from_registry(
    cache_registry: CacheRegistry,
) -> None:
    cache = InMemoryCacheBackend()
    cache_registry.set(CACHE_KEY, cache)
    cache_registry.set("OTHER_CACHE_KEY", cache)
    assert cache_registry.all() == (cache, cache)


def test_registry_should_raise_error_on_dublicate_cache_key(
    cache_registry: CacheRegistry,
) -> None:
    cache = InMemoryCacheBackend()
    cache_registry.set(CACHE_KEY, cache)
    with pytest.raises(NameError, match="Cache with the same name already registered"):
        cache_registry.set(CACHE_KEY, cache)


def test_remove_cache_from_registry(cache_registry: CacheRegistry) -> None:
    cache = InMemoryCacheBackend()
    cache_registry.set(CACHE_KEY, cache)
    cache_registry.remove(CACHE_KEY)
    assert cache_registry.get(CACHE_KEY) is None


def test_remove_cache_from_registry_should_raise_error_if_cache_not_register(
    cache_registry: CacheRegistry,
) -> None:
    with pytest.raises(NameError, match="Cache with the same name not registered"):
        cache_registry.remove(CACHE_KEY)


def test_flush_should_remove_all_registered_cashes(
    cache_registry: CacheRegistry,
) -> None:
    cache = InMemoryCacheBackend()
    cache_registry.set(CACHE_KEY, cache)
    cache_registry.set("OTHER_CACHE_KEY", cache)
    cache_registry.flush()
    assert cache_registry.get(CACHE_KEY) is None
    assert cache_registry.get("OTHER_CACHE_KEY") is None


@pytest.mark.asyncio
async def test_close_caches_should_not_raise_exception(
    cache_registry: CacheRegistry,
) -> None:
    cache = InMemoryCacheBackend()
    cache_registry.set(CACHE_KEY, cache)
    cache_registry.set("OTHER_CACHE_KEY", cache)
    await close_caches()
    assert cache_registry.get(CACHE_KEY) is None


@pytest.mark.backwards
def test_registry_can_be_imported_by_older_path() -> None:
    import importlib

    fastapi_cache_plus = importlib.import_module("fastapi_cache_plus")
    assert hasattr(fastapi_cache_plus, "caches")
