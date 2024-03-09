import sys
import requests

if len(sys.argv) < 3:
    print("Please provide the HOST and API_KEY as command-line arguments.")
    sys.exit(1)

HOST = sys.argv[1]
API_KEY = sys.argv[2]

print(f"HOST: {HOST}")
print(f"API_KEY: {API_KEY}")

url = f"{HOST}/case"
headers = {
    "X-API-Key": API_KEY
}

def get_case():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        case_data = response.json()
        print("Case Information:")
        print(f"Name: {case_data['name']}")
        print(f"Period: {case_data['period']}")
        print(f"Tick: {case_data['tick']}")
        print(f"Ticks per Period: {case_data['ticks_per_period']}")
        print(f"Total Periods: {case_data['total_periods']}")
        print(f"Status: {case_data['status']}")
        print(f"Is Enforce Trading Limits: {case_data['is_enforce_trading_limits']}")
        return case_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except KeyError:
        print("Error: Unexpected response format from the API.")

def get_trader():
    url = f"{HOST}/trader"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        trader_data = response.json()
        print("Trader Information:")
        print(f"Trader ID: {trader_data['trader_id']}")
        print(f"First Name: {trader_data['first_name']}")
        print(f"Last Name: {trader_data['last_name']}")
        print(f"Net Liquidation Value (NLV): {trader_data['nlv']}")
        return trader_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except KeyError:
        print("Error: Unexpected response format from the API.")
