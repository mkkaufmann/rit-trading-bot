'use client'
import Image from "next/image";
import styles from "./page.module.css";
import Graph from "@/components/Graph";
import OrderBookChart from "@/components/OrderBookChart";
import React from "react";

const generateRandomOrders = (n: number, price: number): OrderBook => {
  const fakeBidOrders: Order[] = [];
  const fakeAskOrders: Order[] = [];

  for (let i = 0; i < n; i++) {
    const bidPrice = price - Math.random() * 0.1; // Generate bid prices slightly below the given price
    const askPrice = price + Math.random() * 0.1; // Generate ask prices slightly above the given price

    const bidQuantity = Math.floor(Math.random() * 5000) + 500; // Generate bid quantities between 50 and 150
    const askQuantity = Math.floor(Math.random() * 5000) + 500; // Generate ask quantities between 50 and 150

    const bidOrder: Order = {
      order_id: i + 1, // Unique order ID
      period: 1,
      tick: i + 1,
      trader_id: `trader${i + 1}`,
      ticker: 'CRZY',
      type: 'LIMIT',
      quantity: bidQuantity,
      action: 'BUY',
      price: bidPrice,
      quantity_filled: 0,
      vwap: 0,
      status: 'OPEN',
    };

    const askOrder: Order = {
      order_id: i + 1 + n, // Unique order ID
      period: 1,
      tick: i + 1 + n,
      trader_id: `trader${i + 1 + n}`,
      ticker: 'CRZY',
      type: 'LIMIT',
      quantity: askQuantity,
      action: 'SELL',
      price: askPrice,
      quantity_filled: 0,
      vwap: 0,
      status: 'OPEN',
    };

    fakeBidOrders.push(bidOrder);
    fakeAskOrders.push(askOrder);
  }

  const fakeOrderBook: OrderBook = {
    bid: fakeBidOrders,
    ask: fakeAskOrders,
  };

  return fakeOrderBook;
};


export default function Home() {
  const [fakeOrderBook,setFakeOrderBook] = React.useState(generateRandomOrders(10, 14.21));
  setInterval(()=>{setFakeOrderBook(generateRandomOrders(10,14.21))},5000);
  React.useEffect(()=>{
  },[fakeOrderBook]);
  return (
    <main className={styles.main}>
        <OrderBookChart {...fakeOrderBook}/>
    </main>
  );
}
