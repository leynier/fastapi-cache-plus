# FastAPI Cache Plus

> This project is a continuation of the project [fastapi_cache](https://github.com/comeuplater/fastapi_cache). Many thanks to Ivan Sushkov (the original author) for their work and contributions.

Implements simple lightweight cache system as dependencies in FastAPI.

## Installation

```sh
pip install fastapi-cache-plus
```

## Usage example

```python
from fastapi import Depends, FastAPI

from fastapi_cache_plus import caches, close_caches
from fastapi_cache_plus.backends.redis import CACHE_KEY, RedisCacheBackend

app = FastAPI()


def redis_cache():
    return caches.get(CACHE_KEY)


@app.get('/')
async def hello(
    cache: RedisCacheBackend = Depends(redis_cache)
):
    in_cache = await cache.get('some_cached_key')
    if not in_cache:
        await cache.set('some_cached_key', 'new_value', 5)

    return {'response': in_cache or 'default'}


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend('redis://redis')
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()
```
