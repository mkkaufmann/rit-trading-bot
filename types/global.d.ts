interface Order {
  order_id: number;
  period: number;
  tick: number;
  trader_id: string;
  ticker: string;
  type: 'LIMIT'|'MARKET';
  quantity: number;
  action: 'BUY'|'SELL';
  price: number;
  quantity_filled: number;
  vwap: number;
  status: 'OPEN'|'TRANSACTED'|'CANCELLED';
}

interface OrderBook {
  bid: Order[];
  ask: Order[];
}
