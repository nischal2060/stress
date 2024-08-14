import requests
import concurrent.futures
import time
import argparse

# Function to make a request
def make_request(url, verify):
    try:
        response = requests.get(url, verify=verify)  # Pass verification parameter
        print(f"Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Stress test a server by sending high-speed concurrent requests.")
    parser.add_argument("url", type=str, help="The URL to stress test.")
    parser.add_argument("num_requests", type=int, help="The total number of requests to send.")
    parser.add_argument("--threads", type=int, default=100, help="Number of concurrent threads (default: 100).")
    parser.add_argument("--ignore-ssl", action="store_true", help="Ignore SSL certificate warnings.")
    parser.add_argument("--cert-bundle", type=str, default=None, help="Path to a custom CA bundle for SSL verification.")

    args = parser.parse_args()

    url = args.url
    num_requests = args.num_requests
    num_threads = args.threads

    # Determine SSL verification setting
    if args.ignore_ssl:
        verify = False  # Disable SSL verification
    elif args.cert_bundle:
        verify = args.cert_bundle  # Path to custom CA bundle
    else:
        verify = True  # Default behavior (use system CA certificates)

    start_time = time.time()

    # Use ThreadPoolExecutor to create a pool of threads for high-speed concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit multiple requests to the executor
        futures = [executor.submit(make_request, url, verify) for _ in range(num_requests)]
        
        # Process the results as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Retrieve result to check for exceptions
            except Exception as e:
                print(f"Request failed: {e}")

    end_time = time.time()
    print(f"Load test completed in {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
