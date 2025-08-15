"""
Caching utilities for offline mode and performance optimization
"""
import json
import pickle
import hashlib
import time
from pathlib import Path
from typing import Any, Optional, Dict, Union
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class CacheManager:
    """Manages caching for model predictions and API responses"""
    
    def __init__(self, cache_dir: str = "cache", default_ttl: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.default_ttl = default_ttl  # Time to live in seconds
        self.memory_cache = {}
        
        # Create subdirectories for different cache types
        (self.cache_dir / "predictions").mkdir(exist_ok=True)
        (self.cache_dir / "api_responses").mkdir(exist_ok=True)
        (self.cache_dir / "models").mkdir(exist_ok=True)
    
    def _generate_key(self, data: Union[str, Dict, Any]) -> str:
        """Generate a unique cache key from input data"""
        if isinstance(data, str):
            content = data
        elif isinstance(data, dict):
            content = json.dumps(data, sort_keys=True)
        else:
            content = str(data)
        
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, key: str, cache_type: str = "predictions") -> Path:
        """Get the file path for a cache entry"""
        return self.cache_dir / cache_type / f"{key}.cache"
    
    def _is_expired(self, cache_path: Path, ttl: int) -> bool:
        """Check if cache entry is expired"""
        if not cache_path.exists():
            return True
        
        file_age = time.time() - cache_path.stat().st_mtime
        return file_age > ttl
    
    def get(self, key: str, cache_type: str = "predictions", ttl: Optional[int] = None) -> Optional[Any]:
        """
        Retrieve data from cache
        
        Args:
            key: Cache key
            cache_type: Type of cache (predictions, api_responses, models)
            ttl: Time to live in seconds (uses default if None)
            
        Returns:
            Cached data or None if not found/expired
        """
        if ttl is None:
            ttl = self.default_ttl
        
        # Check memory cache first
        memory_key = f"{cache_type}:{key}"
        if memory_key in self.memory_cache:
            cached_item = self.memory_cache[memory_key]
            if time.time() - cached_item['timestamp'] < ttl:
                return cached_item['data']
            else:
                del self.memory_cache[memory_key]
        
        # Check file cache
        cache_path = self._get_cache_path(key, cache_type)
        
        if self._is_expired(cache_path, ttl):
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            
            # Store in memory cache for faster access
            self.memory_cache[memory_key] = {
                'data': data,
                'timestamp': time.time()
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Error reading cache {cache_path}: {e}")
            return None
    
    def set(self, key: str, data: Any, cache_type: str = "predictions", ttl: Optional[int] = None):
        """
        Store data in cache
        
        Args:
            key: Cache key
            data: Data to cache
            cache_type: Type of cache
            ttl: Time to live in seconds
        """
        if ttl is None:
            ttl = self.default_ttl
        
        # Store in memory cache
        memory_key = f"{cache_type}:{key}"
        self.memory_cache[memory_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        # Store in file cache
        cache_path = self._get_cache_path(key, cache_type)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
            
            logger.debug(f"Cached data with key {key} in {cache_type}")
            
        except Exception as e:
            logger.error(f"Error writing cache {cache_path}: {e}")
    
    def delete(self, key: str, cache_type: str = "predictions"):
        """Delete a cache entry"""
        # Remove from memory cache
        memory_key = f"{cache_type}:{key}"
        if memory_key in self.memory_cache:
            del self.memory_cache[memory_key]
        
        # Remove from file cache
        cache_path = self._get_cache_path(key, cache_type)
        if cache_path.exists():
            try:
                cache_path.unlink()
                logger.debug(f"Deleted cache entry {key} from {cache_type}")
            except Exception as e:
                logger.error(f"Error deleting cache {cache_path}: {e}")
    
    def clear(self, cache_type: Optional[str] = None):
        """Clear cache entries"""
        if cache_type:
            # Clear specific cache type
            cache_dir = self.cache_dir / cache_type
            if cache_dir.exists():
                for cache_file in cache_dir.glob("*.cache"):
                    try:
                        cache_file.unlink()
                    except Exception as e:
                        logger.error(f"Error deleting {cache_file}: {e}")
            
            # Clear from memory cache
            keys_to_delete = [k for k in self.memory_cache.keys() if k.startswith(f"{cache_type}:")]
            for key in keys_to_delete:
                del self.memory_cache[key]
        else:
            # Clear all caches
            for cache_type_dir in self.cache_dir.iterdir():
                if cache_type_dir.is_dir():
                    for cache_file in cache_type_dir.glob("*.cache"):
                        try:
                            cache_file.unlink()
                        except Exception as e:
                            logger.error(f"Error deleting {cache_file}: {e}")
            
            self.memory_cache.clear()
        
        logger.info(f"Cleared cache: {cache_type or 'all'}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        stats = {
            'memory_cache_size': len(self.memory_cache),
            'cache_types': {}
        }
        
        for cache_type_dir in self.cache_dir.iterdir():
            if cache_type_dir.is_dir():
                cache_files = list(cache_type_dir.glob("*.cache"))
                total_size = sum(f.stat().st_size for f in cache_files)
                
                stats['cache_types'][cache_type_dir.name] = {
                    'file_count': len(cache_files),
                    'total_size_bytes': total_size,
                    'total_size_mb': round(total_size / (1024 * 1024), 2)
                }
        
        return stats

def cached(cache_type: str = "predictions", ttl: Optional[int] = None, key_func: Optional[callable] = None):
    """
    Decorator for caching function results
    
    Args:
        cache_type: Type of cache to use
        ttl: Time to live in seconds
        key_func: Function to generate cache key from arguments
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                key_data = {
                    'function': func.__name__,
                    'args': args,
                    'kwargs': kwargs
                }
                cache_key = cache_manager._generate_key(key_data)
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key, cache_type, ttl)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, cache_type, ttl)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        
        return wrapper
    return decorator

class OfflineModeManager:
    """Manages offline mode functionality"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager
        self.offline_mode = False
        self.offline_responses = {}
        self._load_offline_responses()
    
    def enable_offline_mode(self):
        """Enable offline mode"""
        self.offline_mode = True
        logger.info("Offline mode enabled")
    
    def disable_offline_mode(self):
        """Disable offline mode"""
        self.offline_mode = False
        logger.info("Offline mode disabled")
    
    def is_offline(self) -> bool:
        """Check if currently in offline mode"""
        return self.offline_mode
    
    def _load_offline_responses(self):
        """Load predefined offline responses"""
        offline_file = Path(__file__).parent.parent / "data" / "offline_responses.json"
        
        try:
            if offline_file.exists():
                with open(offline_file, 'r') as f:
                    self.offline_responses = json.load(f)
        except Exception as e:
            logger.error(f"Error loading offline responses: {e}")
            self.offline_responses = {}
    
    def get_offline_response(self, query_type: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get offline response for a query type"""
        if query_type in self.offline_responses:
            response = self.offline_responses[query_type].copy()
            response['offline_mode'] = True
            response['message'] = "Response generated in offline mode - limited functionality"
            return response
        
        return {
            'error': 'Service unavailable in offline mode',
            'offline_mode': True,
            'suggestion': 'Please connect to internet for full functionality'
        }

# Global cache manager instance
cache_manager = CacheManager()
offline_manager = OfflineModeManager(cache_manager)