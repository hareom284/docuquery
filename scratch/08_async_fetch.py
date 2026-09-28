"""Day 3 — async / await.

Each URL below takes about 1 second on the server side, so the timings are obvious.

TASK — fill in the three functions, then run the file.

  1. fetch_sequential()  — await the 10 requests ONE AFTER ANOTHER.
                           Expect roughly 10 x 1s.

  2. fetch_concurrent()  — send the same 10 with asyncio.gather().
                           Expect roughly 1 x 1s (plus network overhead).

  3. fetch_blocking()    — same as fetch_concurrent, but put time.sleep(1)
                           in the middle of the worker. Watch the gain vanish.

WHAT TO NOTICE
  `await` means "I am waiting — loop, go run something else."
  The event loop is ONE thread. Nothing overlaps unless you hand control back.
  time.sleep() never hands control back, so it freezes the whole loop —
  in FastAPI that means every other request waits too.

DONE WHEN
  Concurrent clearly beats sequential, and you can explain why step 3 kills it.

Run:  uv run python scratch/08_async_fetch.py
"""

import asyncio
import time

import httpx

URL = "https://httpbin.org/delay/1"
N = 10


async def fetch_one(client: httpx.AsyncClient, i: int) -> int:
    """Fetch URL once and return the status code. Nothing to change here."""
    response = await client.get(URL, timeout=30)
    return response.status_code


async def fetch_sequential() -> list[int]:
    """Await each request one after another (a normal `for` loop with await)."""
    async with httpx.AsyncClient() as client:
        results = []
        # TODO: loop over range(N) and `await fetch_one(client, i)` each time,
        for i in range(N):
            result = await fetch_one(client, i)
            results.append(result)
        #       appending the status code to results.
        return results


async def fetch_concurrent() -> list[int]:
    """Start all N requests, then wait for them together."""
    async with httpx.AsyncClient() as client:
        # TODO: build a list of coroutines: [fetch_one(client, i) for i in range(N)]
        #       then `return await asyncio.gather(*tasks)`
        #       Note: calling fetch_one() does NOT start it; awaiting does.
        tasks = [fetch_one(client, i) for i in range(N)]
        return await asyncio.gather(*tasks)


async def blocking_worker(client: httpx.AsyncClient, i: int) -> int:
    """Same as fetch_one, but with a BLOCKING sleep in the middle."""
    # TODO: response = await client.get(URL, timeout=30)
    #       time.sleep(1)        <- blocking: never gives the loop back
    #       return response.status_code
    response = await client.get(URL, timeout=30)
    time.sleep(1)  # blocking: never gives the loop back
    return response.status_code


async def fetch_blocking() -> list[int]:
    async with httpx.AsyncClient() as client:
        tasks = [blocking_worker(client, i) for i in range(N)]
        return await asyncio.gather(*tasks)


async def safe_worker(client: httpx.AsyncClient, i: int) -> int:
    """Same blocking sleep, but moved off the event loop onto a worker thread."""
    response = await client.get(URL, timeout=30)
    await asyncio.to_thread(time.sleep, 1)  # loop stays free while this runs
    return response.status_code


async def fetch_safe() -> list[int]:
    async with httpx.AsyncClient() as client:
        tasks = [safe_worker(client, i) for i in range(N)]
        return await asyncio.gather(*tasks)


async def timed(name: str, coro) -> float:
    start = time.perf_counter()
    results = await coro
    elapsed = time.perf_counter() - start
    print(f"{name:<12} {elapsed:6.2f}s   {len(results)} responses")
    return elapsed


async def main() -> None:
    sequential = await timed("sequential", fetch_sequential())
    concurrent = await timed("concurrent", fetch_concurrent())
    blocking = await timed("blocking", fetch_blocking())
    safe = await timed("safe-thread", fetch_safe())

    if concurrent:
        print(f"\nconcurrent is {sequential / concurrent:.1f}x faster than sequential")
        print(f"blocking is  {blocking / concurrent:.1f}x slower than concurrent")
        print(f"safe-thread is {blocking / safe:.1f}x faster than blocking (same sleep!)")


if __name__ == "__main__":
    asyncio.run(main())
