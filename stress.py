import argparse
import asyncio
from mcpy import MinecraftBot
from mcpy.exceptions import ConnectionException
import time

async def connect_bot(server_address, server_port):
    bot = MinecraftBot()
    try:
        await bot.connect(server_address, server_port)
        await bot.disconnect()
        print(f"Bot connected and disconnected successfully.")
    except ConnectionException as e:
        print(f"Failed to connect: {e}")

async def stress_test(server_address, server_port, num_bots, num_concurrent):
    sem = asyncio.Semaphore(num_concurrent)
    tasks = []

    async def bot_task():
        async with sem:
            await connect_bot(server_address, server_port)

    for _ in range(num_bots):
        tasks.append(bot_task())

    start_time = time.time()
    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Stress test completed in {end_time - start_time} seconds")

def main():
    parser = argparse.ArgumentParser(description="Stress test a Minecraft server by pushing multiple bots.")
    parser.add_argument("server_address", type=str, help="The Minecraft server address (e.g., example.com).")
    parser.add_argument("server_port", type=int, help="The Minecraft server port (e.g., 25565).")
    parser.add_argument("num_bots", type=int, help="The total number of bots to connect.")
    parser.add_argument("--concurrent", type=int, default=100, help="Number of concurrent bot connections (default: 100).")

    args = parser.parse_args()

    asyncio.run(stress_test(args.server_address, args.server_port, args.num_bots, args.concurrent))

if __name__ == "__main__":
    main()
