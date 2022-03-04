#!/usr/bin/env python3

import asyncio


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
        pass

