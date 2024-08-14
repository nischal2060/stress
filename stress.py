import requests
import concurrent.futures
import time

# Function to make a request
def make_request(url):
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def main():
    # Get user input for URL and number of requests
    url = input("Enter the URL to stress test: ")
    num_requests = int(input("Enter the number of concurrent requests: "))

    start_time = time.time()

    # Use ThreadPoolExecutor to create a pool of threads for concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit multiple requests to the executor
        futures = [executor.submit(make_request, url) for _ in range(num_requests)]
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Retrieve result to check for exceptions
            except Exception as e:
                print(f"Request failed: {e}")

    end_time = time.time()
    print(f"Load test completed in {end_time - start_time} seconds")

if __name__ == "__main__":
    main() 
