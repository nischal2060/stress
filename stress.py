import aiohttp
import asyncio
import time
import argparse
from aiohttp import ClientSession, ClientTimeout, ClientConnectorError

# Function to make an asynchronous request with retry logic
async def make_request(session, url, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    print("Success")
                else:
                    print(f"Status Code: {response.status}")
                return
        except ClientConnectorError as e:
            print(f"Connection error: {e}")
        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
        await asyncio.sleep(1)  # Delay before retrying
        attempt += 1

async def worker(url, num_requests, semaphore):
    timeout = ClientTimeout(total=30)  # Custom timeout
    connector = aiohttp.TCPConnector(limit_per_host=100)  # Custom connection pooling
    async with ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for _ in range(num_requests):
            async with semaphore:
                tasks.append(make_request(session, url))
        await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Stress test a server with high-speed concurrent asynchronous requests.")
    parser.add_argument("url", type=str, help="The URL to stress test.")
    parser.add_argument("num_requests", type=int, help="The total number of requests to send.")
    parser.add_argument("--threads", type=int, default=1000, help="Number of concurrent threads (default: 1000).")
    parser.add_argument("--rate-limit", type=int, default=1000, help="Number of requests per second (default: 1000).")

    args = parser.parse_args()

    url = args.url
    num_requests = args.num_requests
    num_threads = args.threads
    rate_limit = args.rate_limit

    semaphore = asyncio.Semaphore(rate_limit)

    start_time = time.time()

    # Create multiple workers to handle the stress test
    async def main_task():
        tasks = [worker(url, num_requests // num_threads, semaphore) for _ in range(num_threads)]
        await asyncio.gather(*tasks)

    asyncio.run(main_task())

    end_time = time.time()
    print(f"Load test completed in {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
