from time import time, sleep
import math

"""
    The algorithm consists of a bucket with a maximum capacity of N tokens which refills at a rate R tokens per second. 
    Each token typically represents a quantity of whatever resource is being rate limited (network bandwidth, connections, etc.).
    This allows for a fixed rate of flow R with bursts up to N without impacting the consumer.
    This implementation is not thread-safe.
"""


class LeakyBucket:
    
    def __init__(self, tokens, fill_rate):
        """tokens is the total tokens in the bucket. fill_rate is the
        rate in tokens/second that the bucket will be refilled
        """
        self.capacity = tokens
        self._tokens = tokens
        self.fill_rate = fill_rate
        self.timestamp = time()
        
    
    def consume(self, tokens):
        """Consume tokens from the bucket. Returns True if there were
        sufficient tokens otherwise False"""
        if tokens <= self.tokens:
            self._tokens -= tokens
        else:
            return False
        return True
    
    def get_tokens(self):
        if self._tokens < self.capacity:
            now = time()
            delta =  math.floor(self.fill_rate * (now - self.timestamp))
            self._tokens = min(self.capacity, self._tokens + delta)
            self.timestamp = now
        return self._tokens
    
    tokens = property(get_tokens) # allow to create methods that behave like attributes
                                  # property() is the Pythonic way to avoid formal getter and setter methods in code
                                  # With property(), you can attach getter and setter methods to given class attributes. 
                                  # This way, you can handle the internal implementation for that attribute without exposing getter and setter methods in your API. 
                                  # You can also specify a way to handle attribute deletion and provide an appropriate docstring for your properties.
                                  # property(fget=None, fset=None, fdel=None, doc=None)


if __name__ == '__main__':
    bucket = LeakyBucket(tokens=80, fill_rate=1)
    print(f"tokens = {bucket.tokens}")
    print(f"consume(10) = {bucket.consume(10)}")
    print(f"consume(10) = {bucket.consume(10)}")
    sleep(1)
    print(f"tokens = {bucket.tokens}")
    sleep(1)
    print(f"tokens = {bucket.tokens}")
    print(f"consume(90) = {bucket.consume(90)}")
    sleep(1)
    print(f"tokens = {bucket.tokens}")