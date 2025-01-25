# Changelog
  
* 0.1.0 Added TTL support for InMemoryCacheBackend. Added `expire()` method that update ttl value for key.

* 0.0.6 Added typings for backends. Specific arguments now need to be passed through **kwargs.
Set default encoding to utf-8 for redis backend, removed default TTL for redis keys.
