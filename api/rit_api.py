import sys
import requests

HOST = ""
API_KEY = ""

headers = {
    "X-API-Key": API_KEY
}


DEBUG = False
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def init(host,api_key):
    global HOST, API_KEY,headers
    HOST = host
    API_KEY = api_key
    headers = {
        "X-API-Key": API_KEY
    }

debug_print(f"HOST: {HOST}")
debug_print(f"API_KEY: {API_KEY}")

def get_case():
    url = f"{HOST}/case"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        case_data = response.json()
        debug_print("Case Information:")
        debug_print(f"Name: {case_data['name']}")
        debug_print(f"Period: {case_data['period']}")
        debug_print(f"Tick: {case_data['tick']}")
        debug_print(f"Ticks per Period: {case_data['ticks_per_period']}")
        debug_print(f"Total Periods: {case_data['total_periods']}")
        debug_print(f"Status: {case_data['status']}")
        debug_print(f"Is Enforce Trading Limits: {case_data['is_enforce_trading_limits']}")
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
        debug_print("Trader Information:")
        debug_print(f"Trader ID: {trader_data['trader_id']}")
        debug_print(f"First Name: {trader_data['first_name']}")
        debug_print(f"Last Name: {trader_data['last_name']}")
        debug_print(f"Net Liquidation Value (NLV): {trader_data['nlv']}")
        return trader_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except KeyError:
        print("Error: Unexpected response format from the API.")

def get_limits():
    url = f"{HOST}/limits"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        trading_limits = response.json()
        debug_print("Trading Limits:")
        for limit in trading_limits:
            debug_print(f"Name: {limit['name']}")
            debug_print(f"Gross: {limit['gross']}")
            debug_print(f"Net: {limit['net']}")
            debug_print(f"Gross Limit: {limit['gross_limit']}")
            debug_print(f"Net Limit: {limit['net_limit']}")
            debug_print(f"Gross Fine: {limit['gross_fine']}")
            debug_print(f"Net Fine: {limit['net_fine']}")
            debug_print("---")
        return trading_limits
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

most_recent_news_id = None
most_recent_news_tick = -1

def get_news(since=most_recent_news_id, limit=20):
    url = f"{HOST}/news"
    params = {"limit": limit}
    if since is not None:
        params["since"] = since

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        news_data = response.json()
        debug_print("Recent News:")
        for news_item in news_data:
            global most_recent_news_id, most_recent_news_tick
            if news_item['tick'] > most_recent_news_tick:
                most_recent_news_id = news_item['news_id']
                most_recent_news_tick = news_item['tick']
            debug_print(f"News ID: {news_item['news_id']}")
            debug_print(f"Period: {news_item['period']}")
            debug_print(f"Tick: {news_item['tick']}")
            debug_print(f"Ticker: {news_item['ticker']}")
            debug_print(f"Headline: {news_item['headline']}")
            debug_print(f"Body: {news_item['body']}")
            debug_print("---")
        return news_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def get_assets(ticker=None):
    url = f"{HOST}/assets"
    params = {}
    if ticker:
        params["ticker"] = ticker

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        assets_data = response.json()
        debug_print("Available Assets:")
        for asset in assets_data:
            debug_print(f"Ticker: {asset['ticker']}")
            debug_print(f"Type: {asset['type']}")
            debug_print(f"Description: {asset['description']}")
            debug_print(f"Total Quantity: {asset['total_quantity']}")
            debug_print(f"Available Quantity: {asset['available_quantity']}")
            debug_print(f"Lease Price: {asset['lease_price']}")
            debug_print("Convert From:")
            for convert_from in asset.get('convert_from', []):
                debug_print(f"  Ticker: {convert_from['ticker']}, Quantity: {convert_from['quantity']}")
            debug_print("Convert To:")
            for convert_to in asset.get('convert_to', []):
                debug_print(f"  Ticker: {convert_to['ticker']}, Quantity: {convert_to['quantity']}")
            if 'containment' in asset:
                debug_print(f"Containment: Ticker: {asset['containment']['ticker']}, Quantity: {asset['containment']['quantity']}")
            debug_print(f"Ticks per Conversion: {asset['ticks_per_conversion']}")
            debug_print(f"Ticks per Lease: {asset['ticks_per_lease']}")
            debug_print(f"Is Available: {asset['is_available']}")
            debug_print(f"Start Period: {asset['start_period']}")
            debug_print(f"Stop Period: {asset['stop_period']}")
            debug_print("---")
        return assets_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def get_asset_history(ticker=None, period=None, limit=None):
    url = f"{HOST}/assets/history"
    params = {}
    if ticker:
        params["ticker"] = ticker
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        asset_history_data = response.json()
        debug_print("Asset History:")
        for asset_history in asset_history_data:
            debug_print(f"Ticker: {asset_history['ticker']}")
            debug_print(f"Tick: {asset_history['tick']}")
            debug_print(f"Action: {asset_history['action']}")
            debug_print(f"Cost: {asset_history['cost']}")
            debug_print("Convert From:")
            for convert_from in asset_history.get('convert_from', []):
                debug_print(f"  Ticker: {convert_from['ticker']}, Quantity: {convert_from['quantity']}")
            debug_print("Convert To:")
            for convert_to in asset_history.get('convert_to', []):
                debug_print(f"  Ticker: {convert_to['ticker']}, Quantity: {convert_to['quantity']}")
            debug_print("Convert From Price:")
            for convert_from_price in asset_history.get('convert_from_price', []):
                debug_print(f"  Ticker: {convert_from_price['ticker']}, Quantity: {convert_from_price['quantity']}")
            debug_print("Convert To Price:")
            for convert_to_price in asset_history.get('convert_to_price', []):
                debug_print(f"  Ticker: {convert_to_price['ticker']}, Quantity: {convert_to_price['quantity']}")
            debug_print("---")
        return asset_history_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def get_securities(ticker=None):
   url = f"{HOST}/securities"
   params = {}
   if ticker:
       params["ticker"] = ticker

   try:
       response = requests.get(url, headers=headers, params=params)
       response.raise_for_status()
       securities_data = response.json()
       for security in securities_data:
           debug_print(f"Ticker: {security['ticker']}")
           debug_print(f"Type: {security['type']}")
           debug_print(f"Size: {security['size']}")
           debug_print(f"Position: {security['position']}")
           debug_print(f"VWAP: {security['vwap']}")
           debug_print(f"NLV: {security['nlv']}")
           debug_print(f"Last: {security['last']}")
           debug_print(f"Bid: {security['bid']}")
           debug_print(f"Bid Size: {security['bid_size']}")
           debug_print(f"Ask: {security['ask']}")
           debug_print(f"Ask Size: {security['ask_size']}")
           debug_print(f"Volume: {security['volume']}")
           debug_print(f"Unrealized: {security['unrealized']}")
           debug_print(f"Realized: {security['realized']}")
           debug_print(f"Currency: {security['currency']}")
           debug_print(f"Total Volume: {security['total_volume']}")
           debug_print("Limits:")
           for limit in security.get('limits', []):
               debug_print(f"  Name: {limit['name']}, Units: {limit['units']}")
           debug_print(f"Interest Rate: {security['interest_rate']}")
           debug_print(f"Is Tradeable: {security['is_tradeable']}")
           debug_print(f"Is Shortable: {security['is_shortable']}")
           debug_print(f"Start Period: {security['start_period']}")
           debug_print(f"Stop Period: {security['stop_period']}")
           debug_print(f"Description: {security['description']}")
           debug_print(f"Unit Multiplier: {security['unit_multiplier']}")
           debug_print(f"Display Unit: {security['display_unit']}")
           debug_print(f"Start Price: {security['start_price']}")
           debug_print(f"Min Price: {security['min_price']}")
           debug_print(f"Max Price: {security['max_price']}")
           debug_print(f"Quoted Decimals: {security['quoted_decimals']}")
           debug_print(f"Trading Fee: {security['trading_fee']}")
           debug_print(f"Limit Order Rebate: {security['limit_order_rebate']}")
           debug_print(f"Min Trade Size: {security['min_trade_size']}")
           debug_print(f"Max Trade Size: {security['max_trade_size']}")
           debug_print(f"Required Tickers: {security['required_tickers']}")
           debug_print(f"Bond Coupon: {security['bond_coupon']}")
           debug_print(f"Interest Payments Per Period: {security['interest_payments_per_period']}")
           debug_print(f"Base Security: {security['base_security']}")
           debug_print(f"Fixing Ticker: {security['fixing_ticker']}")
           debug_print(f"API Orders Per Second: {security['api_orders_per_second']}")
           debug_print(f"Execution Delay (ms): {security['execution_delay_ms']}")
           debug_print(f"Interest Rate Ticker: {security['interest_rate_ticker']}")
           debug_print(f"OTC Price Range: {security['otc_price_range']}")
           debug_print("---")
       return securities_data
   except requests.exceptions.RequestException as e:
       print(f"Error: {e}")
   except (KeyError, IndexError):
       print("Error: Unexpected response format from the API.")

def get_security_book(ticker, limit=20):
   url = f"{HOST}/securities/book"
   params = {
       "ticker": ticker,
       "limit": limit
   }

   try:
       response = requests.get(url, headers=headers, params=params)
       response.raise_for_status()
       book_data = response.json()
       debug_print(f"Order Book for {ticker}:")
       debug_print("Bids:")
       for bid in book_data.get("bids", []):
           debug_print(f"  Order ID: {bid['order_id']}, Period: {bid['period']}, Tick: {bid['tick']}, Trader ID: {bid['trader_id']}, Type: {bid['type']}, Quantity: {bid['quantity']}, Action: {bid['action']}, Price: {bid['price']}, Quantity Filled: {bid['quantity_filled']}, VWAP: {bid['vwap']}, Status: {bid['status']}")
       debug_print("Asks:")
       for ask in book_data.get("asks", []):
           debug_print(f"  Order ID: {ask['order_id']}, Period: {ask['period']}, Tick: {ask['tick']}, Trader ID: {ask['trader_id']}, Type: {ask['type']}, Quantity: {ask['quantity']}, Action: {ask['action']}, Price: {ask['price']}, Quantity Filled: {ask['quantity_filled']}, VWAP: {ask['vwap']}, Status: {ask['status']}")
       return book_data
   except requests.exceptions.RequestException as e:
       debug_print(f"Error: {e}")
   except (KeyError, IndexError):
       debug_print("Error: Unexpected response format from the API.")

def get_security_history(ticker, period=None, limit=None):
   url = f"{HOST}/securities/history"
   params = {
       "ticker": ticker
   }
   if period:
       params["period"] = period
   if limit:
       params["limit"] = limit

   try:
       response = requests.get(url, headers=headers, params=params)
       response.raise_for_status()
       history_data = response.json()
       debug_print(f"OHLC History for {ticker}:")
       for data in history_data:
           debug_print(f"  Tick: {data['tick']}, Open: {data['open']}, High: {data['high']}, Low: {data['low']}, Close: {data['close']}")
       return history_data
   except requests.exceptions.RequestException as e:
       print(f"Error: {e}")
   except (KeyError, IndexError):
       print("Error: Unexpected response format from the API.")

def get_security_tas(ticker, after=None, period=None, limit=None):
   url = f"{HOST}/securities/tas"
   params = {
       "ticker": ticker
   }
   if after is not None:
       params["after"] = after
   elif period is not None:
       params["period"] = period
       if limit is not None:
           params["limit"] = limit

   try:
       response = requests.get(url, headers=headers, params=params)
       response.raise_for_status()
       tas_data = response.json()
       for data in tas_data:
           debug_print(f"ID: {data['id']}, Period: {data['period']}, Tick: {data['tick']}, Price: {data['price']}, Quantity: {data['quantity']}")
       return tas_data
   except requests.exceptions.RequestException as e:
       print(f"Error: {e}")
   except (KeyError, IndexError):
       print("Error: Unexpected response format from the API.")

def get_orders(status="OPEN"):
   url = f"{HOST}/orders"
   params = {"status": status}

   try:
       response = requests.get(url, headers=headers, params=params)
       response.raise_for_status()
       orders_data = response.json()
       for order in orders_data:
           debug_print(f"Order ID: {order['order_id']}, Period: {order['period']}, Tick: {order['tick']}, Trader ID: {order['trader_id']}, Ticker: {order['ticker']}, Type: {order['type']}, Quantity: {order['quantity']}, Action: {order['action']}, Price: {order['price']}, Quantity Filled: {order['quantity_filled']}, VWAP: {order['vwap']}, Status: {order['status']}")
       return orders_data
   except requests.exceptions.RequestException as e:
       print(f"Error: {e}")
   except (KeyError, IndexError):
       print("Error: Unexpected response format from the API.")

def post_order(ticker, order_type, quantity, action, price=None, dry_run=None):
    url = f"{HOST}/orders"
    params = {
        "ticker": ticker,
        "type": order_type,
        "quantity": quantity,
        "action": action
    }
    if price is not None:
        params["price"] = price
    if dry_run is not None:
        params["dry_run"] = dry_run

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        order_data = response.json()
        debug_print(f"Order ID: {order_data['order_id']}, Period: {order_data['period']}, Tick: {order_data['tick']}, Trader ID: {order_data['trader_id']}, Ticker: {order_data['ticker']}, Type: {order_data['type']}, Quantity: {order_data['quantity']}, Action: {order_data['action']}, Price: {order_data['price']}, Quantity Filled: {order_data['quantity_filled']}, VWAP: {order_data['vwap']}, Status: {order_data['status']}")
        return order_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def get_order(order_id):
    url = f"{HOST}/orders/{order_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        order_data = response.json()
        debug_print(f"Order ID: {order_data['order_id']}, Period: {order_data['period']}, Tick: {order_data['tick']}, Trader ID: {order_data['trader_id']}, Ticker: {order_data['ticker']}, Type: {order_data['type']}, Quantity: {order_data['quantity']}, Action: {order_data['action']}, Price: {order_data['price']}, Quantity Filled: {order_data['quantity_filled']}, VWAP: {order_data['vwap']}, Status: {order_data['status']}")
        return order_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def delete_order(order_id):
    url = f"{HOST}/orders/{order_id}"

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        success_data = response.json()
        debug_print(f"Success: {success_data['success']}")
        return success_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def get_tenders():
    url = f"{HOST}/tenders"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tenders_data = response.json()
        for tender in tenders_data:
            debug_print(f"Tender ID: {tender['tender_id']}, Period: {tender['period']}, Tick: {tender['tick']}, Expires: {tender['expires']}, Caption: {tender['caption']}, Quantity: {tender['quantity']}, Action: {tender['action']}, Is Fixed Bid: {tender['is_fixed_bid']}, Price: {tender['price']}")
        return tenders_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def post_tender(tender_id, price=None):
    url = f"{HOST}/tenders/{tender_id}"
    params = {}
    if price is not None:
        params["price"] = price

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        success_data = response.json()
        debug_print(f"Success: {success_data['success']}")
        return success_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def delete_tender(tender_id):
    url = f"{HOST}/tenders/{tender_id}"

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        success_data = response.json()
        debug_print(f"Success: {success_data['success']}")
        return success_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def get_leases():
    url = f"{HOST}/leases"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        leases_data = response.json()
        for lease in leases_data:
            debug_print(f"ID: {lease['id']}, Ticker: {lease['ticker']}, Type: {lease['type']}, Start Lease Period: {lease['start_lease_period']}, Start Lease Tick: {lease['start_lease_tick']}, Next Lease Period: {lease['next_lease_period']}, Next Lease Tick: {lease['next_lease_tick']}, Containment Usage: {lease['containment_usage']}")
            debug_print("Convert From:")
            for convert_from in lease.get('convert_from', []):
                debug_print(f"  Ticker: {convert_from['ticker']}, Quantity: {convert_from['quantity']}")
            debug_print("Convert To:")
            for convert_to in lease.get('convert_to', []):
                debug_print(f"  Ticker: {convert_to['ticker']}, Quantity: {convert_to['quantity']}")
        return leases_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")
def post_lease(ticker, from1=None, quantity1=None, from2=None, quantity2=None, from3=None, quantity3=None):
    url = f"{HOST}/leases"
    params = {"ticker": ticker}
    if from1 is not None:
        params["from1"] = from1
    if quantity1 is not None:
        params["quantity1"] = quantity1
    if from2 is not None:
        params["from2"] = from2
    if quantity2 is not None:
        params["quantity2"] = quantity2
    if from3 is not None:
        params["from3"] = from3
    if quantity3 is not None:
        params["quantity3"] = quantity3

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        lease_data = response.json()
        debug_print(f"ID: {lease_data['id']}, Ticker: {lease_data['ticker']}, Type: {lease_data['type']}, Start Lease Period: {lease_data['start_lease_period']}, Start Lease Tick: {lease_data['start_lease_tick']}, Next Lease Period: {lease_data['next_lease_period']}, Next Lease Tick: {lease_data['next_lease_tick']}, Containment Usage: {lease_data['containment_usage']}")
        debug_print("Convert From:")
        for convert_from in lease_data.get('convert_from', []):
            debug_print(f"  Ticker: {convert_from['ticker']}, Quantity: {convert_from['quantity']}")
        debug_print("Convert To:")
        for convert_to in lease_data.get('convert_to', []):
            debug_print(f"  Ticker: {convert_to['ticker']}, Quantity: {convert_to['quantity']}")
        return lease_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def get_lease(lease_id):
    url = f"{HOST}/leases/{lease_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        lease_data = response.json()
        debug_print(f"ID: {lease_data['id']}, Ticker: {lease_data['ticker']}, Type: {lease_data['type']}, Start Lease Period: {lease_data['start_lease_period']}, Start Lease Tick: {lease_data['start_lease_tick']}, Next Lease Period: {lease_data['next_lease_period']}, Next Lease Tick: {lease_data['next_lease_tick']}, Containment Usage: {lease_data['containment_usage']}")
        debug_print("Convert From:")
        for convert_from in lease_data.get('convert_from', []):
            debug_print(f"  Ticker: {convert_from['ticker']}, Quantity: {convert_from['quantity']}")
        debug_print("Convert To:")
        for convert_to in lease_data.get('convert_to', []):
            debug_print(f"  Ticker: {convert_to['ticker']}, Quantity: {convert_to['quantity']}")
        return lease_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def post_lease_use(lease_id, from1, quantity1, from2=None, quantity2=None, from3=None, quantity3=None):
    url = f"{HOST}/leases/{lease_id}"
    params = {
        "from1": from1,
        "quantity1": quantity1
    }
    if from2 is not None:
        params["from2"] = from2
    if quantity2 is not None:
        params["quantity2"] = quantity2
    if from3 is not None:
        params["from3"] = from3
    if quantity3 is not None:
        params["quantity3"] = quantity3

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        lease_data = response.json()
        debug_print(f"ID: {lease_data['id']}, Ticker: {lease_data['ticker']}, Type: {lease_data['type']}, Start Lease Period: {lease_data['start_lease_period']}, Start Lease Tick: {lease_data['start_lease_tick']}, Next Lease Period: {lease_data['next_lease_period']}, Next Lease Tick: {lease_data['next_lease_tick']}, Containment Usage: {lease_data['containment_usage']}")
        debug_print("Convert From:")
        for convert_from in lease_data.get('convert_from', []):
            debug_print(f"  Ticker: {convert_from['ticker']}, Quantity: {convert_from['quantity']}")
        debug_print("Convert To:")
        for convert_to in lease_data.get('convert_to', []):
            debug_print(f"  Ticker: {convert_to['ticker']}, Quantity: {convert_to['quantity']}")
        return lease_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def delete_lease(lease_id):
    url = f"{HOST}/leases/{lease_id}"

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        success_data = response.json()
        debug_print(f"Success: {success_data['success']}")
        return success_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")

def post_cancel_orders(all=None, ticker=None, ids=None, query=None):
    url = f"{HOST}/commands/cancel"
    params = {}
    if all is not None:
        params["all"] = all
    elif ticker is not None:
        params["ticker"] = ticker
    elif ids is not None:
        params["ids"] = ids
    elif query is not None:
        params["query"] = query

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        cancel_data = response.json()
        debug_print(f"Cancelled Order IDs: {cancel_data['cancelled_order_ids']}")
        return cancel_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except (KeyError, IndexError):
        print("Error: Unexpected response format from the API.")
