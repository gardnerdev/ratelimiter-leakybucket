#!/usr/bin/env python3

import asyncio
from time import sleep
import time
class LeakyBucket:
    def __init__(self, rate_limit: int) -> None:
        self.rate_limit = rate_limit    # rate_limit parameter which is the number of requests per second
        self.token_queue = asyncio.Queue(rate_limit) #tokens_queue queue with a max size of rate_limit
        self.token_consumer_task = asyncio.create_task(self.consume_tokens())   # tokens_consumer_task to consume tokens from the queue 
                                                                                # at a fairly constant rate.
        
    
    async def add_token(self) ->  None:
        """
        Put an item into the queue. If the queue is full, wait until a free slot is available before adding the item
        so we put 1 into the tokens_queue, if the queue is full it will block the request until a token is consumed from the queue.
        """
        await self.token_queue.put(1)
        return None
    
    
    async def consume_token(self) -> None:
        consumption_rate = 1 / self.rate_limit  # for example, if we have a rate_limit of 100 requests per second,
                                                # it means the rate is 1 request per 0.01 of a second meaning,
                                                # the consumption_rate is 0.01.
        last_consumption_time = 0
        
        while True:  # start an endless loop to continuously consume tokens from the queue and free slots from the queue.
            if self.token_queue.empty():
                await asyncio.sleep(consumption_rate)   # if the queue is empty we have nothing to do 
                continue                                # but sleep for a consumption_rate seconds (or fraction of a second) and try again.
                
                
            current_consumption_time = time.monotonic() # Return the value (in fractional seconds) of a monotonic clock, i.e. a clock that cannot go backwards.
            total_tokens = self.tokens_queue.gsize() # get the size of queue
            
            
            # making sure that freeing slots from queue is happening on constant rate. (no control over the scheduling of corountines so 
            #                                                                           it's needed to find out how much time has passed 
            #                                                                           since the last iteration and translate that to the
            #                                                                           number of tokens that need to be consumed)
            tokens_to_consume = self.get_tokens_amount_to_consume( # to implement
                consumption_rate,
                current_consumption_time,
                last_consumption_time,
                total_tokens
            )
            
            for i in range(0, tokens_to_consume): # Consume token from the queue
                self.token_queue.get_nowait()
            
            last_consumption_time = time.monotonic()
            
            await asyncio.sleep(consumption_rate)

