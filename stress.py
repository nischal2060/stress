import argparse
import time
from mcstatus import MinecraftServer
import concurrent.futures

def stress_test(server_address, num_requests, num_threads):
    server = MinecraftServer.lookup(server_address)

    def query_server():
        try:
            status = server.status()
            print(f"Server has {status.players.online} players and replied in {status.latency} ms")
        except Exception as e:
            print(f"Failed to query server: {e}")

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(query_server) for _ in range(num_requests)]
        
        # Wait for all the futures to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Request failed: {e}")

    end_time = time.time()
    print(f"Load test completed in {end_time - start_time} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stress test a Minecraft server.")
    parser.add_argument("server_address", type=str, help="The Minecraft server address (e.g., example.com:25565).")
    parser.add_argument("num_requests", type=int, help="The total number of requests to send.")
    parser.add_argument("--threads", type=int, default=100, help="Number of concurrent threads (default: 100).")

    args = parser.parse_args()

    stress_test(args.server_address, args.num_requests, args.threads)
