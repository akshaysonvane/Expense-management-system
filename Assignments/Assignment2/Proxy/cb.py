from functools import wraps
from datetime import datetime, timedelta

from redis import Redis

redis = Redis(host='172.18.0.3', port=6379)

circuitBreakerMap = {}
url = ""


class CircuitBreaker(object):
    def __init__(self, name=None, expected_exception=ArithmeticError, max_failure_to_open=3, reset_timeout=3):
        self._name = name
        self._expected_exception = expected_exception
        self._max_failure_to_open = max_failure_to_open
        self._reset_timeout = reset_timeout
        # Set the initial state
        self.close()

    def close(self):
        self._is_closed = True
        self._failure_count = 0

    def open(self):
        self._is_closed = False
        self._opened_since = datetime.utcnow()

    def can_execute(self):
        if not self._is_closed:
            self._open_until = self._opened_since + timedelta(seconds=self._reset_timeout)
            self._open_remaining = (self._open_until - datetime.utcnow()).total_seconds()
            return self._open_remaining <= 0
        else:
            return True

    def __call__(self, func):
        if self._name is None:
            self._name = func.__name__

        @wraps(func)
        def with_circuitbreaker(*args, **kwargs):
            global url
            url = args[1] + ':' + str(args[2])
            if url not in circuitBreakerMap:
                circuitBreaker = CircuitBreaker(max_failure_to_open=self._max_failure_to_open,
                                                reset_timeout=self._reset_timeout)
                circuitBreakerMap[url] = circuitBreaker
            return circuitBreakerMap[url].call(func, *args, **kwargs)

        return with_circuitbreaker

    def call(self, func, *args, **kwargs):
        if not self.can_execute():
            err = 'CircuitBreaker[%s] is OPEN until %s (%d failures, %d sec remaining)' % (
                self._name,
                self._open_until,
                self._failure_count,
                round(self._open_remaining)
            )
            print Exception(err)
            for key in redis.scan_iter():
                if redis.get(key) == url:
                    redis.delete(key)
                    break
            print "Entry removed: " + url
            return False

        # try:
        result = func(*args, **kwargs)
        # except self._expected_exception:
        if not result:
            self._failure_count += 1
            print "Failure count: ", self._failure_count
            if self._failure_count >= self._max_failure_to_open:
                self.open()
            # raise
            return False
        self.close()
        return result
