#!/usr/bin/env python3

import asyncio


class LeakyBucket:
    def __init__(self, rate_limit: int) -> None:
        self.rate_limit = rate_limit    # rate_limit parameter which is the number of requests per second
        self.token_queue = asyncio.Queue(rate_limit)
        self.token_consumer_task = asyncio.create_task(self.consume_tokens())   # tokens_consumer_task to consume tokens from the queue 
                                                                                # at a fairly constant rate.
        
    
    async def add_token(self) ->  None:
        pass
    
    async def consume_token(self) -> None:
        pass

