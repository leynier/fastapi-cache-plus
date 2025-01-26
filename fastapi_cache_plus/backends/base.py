from typing import Generic, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class BaseCacheBackend(Generic[KT, VT]):
    async def add(self, key: KT, value: VT, **kwargs) -> bool:
        raise NotImplementedError  # pragma: no cover

    async def get(self, key: KT, default: VT = None, **kwargs) -> VT:
        raise NotImplementedError  # pragma: no cover

    async def set(self, key: KT, value: VT, **kwargs) -> bool:
        raise NotImplementedError  # pragma: no cover

    async def expire(self, key: KT, ttl: int) -> bool:
        raise NotImplementedError  # pragma: no cover

    async def exists(self, *keys: KT) -> bool:
        raise NotImplementedError  # pragma: no cover

    async def delete(self, key: KT) -> bool:
        raise NotImplementedError  # pragma: no cover

    async def flush(self) -> None:
        raise NotImplementedError  # pragma: no cover

    async def close(self) -> None:
        raise NotImplementedError  # pragma: no cover
