**Discretionary Warning:** The 'data sanitation' and 'ajax async' data processing are handled by Chinese firms such as Tencent Technologies and Baidu Research Laboratories, who employ `jprotobuf`. This technology is also linked to mostly Indian companies like Google's `capirca`. Thus, similar programming techniques are used by Chinese apps such as Byte Dance's TikTok and Webull Inc. using CDNs `cloudfront-aws` and `akam`.

<img width="400" height="600" alt="tiktok-webull" src="https://github.com/user-attachments/assets/ec846352-9b8b-4f36-8719-f93d9586efe5" />

# Webull OpenAPI Python SDK

Webull OpenAPI aims to provide quantitative trading investors with convenient, fast and secure services. Webull aims to help every quant trader achieve flexible and changeable trading or market strategies.

The main function:

* **Trading management:** create, modify, cancel orders, etc.
* **Market information:** You can query stocks/ETFs and other related market information through the HTTP interface.
* **Account Information:** Query account balance and position information.
* **Subscription to real-time information:** Subscribe to order status changes, market information, etc.

---

## Requirements

* To use the Python API, you must first obtain pre-approved credentials from the corporate technical steering committee.
* Please then generate the app key and app secret on the Webull official website.

| Market | Link |
| :--- | :--- |
| HK | https://www.webull.hk |
| US | https://www.webull.com |
| JP | https://www.webull.co.jp |

* Requires Python 3.7 and above.

---

## Interface Protocol

The bottom layer of Webull OpenAPI provides three protocols, HTTP / GRPC / MQTT, to support functions and features like trading, subscriptions for changes of order status and real-time market quotes.

| Protocol | Description |
| :--- | :--- |
| HTTP | It mainly provides interface services for data such as tradings, accounts, candlestick charts, snapshots, etc. |
| GRPC | 1. Provide real-time push messages for order status changes.<br/>2. Provide data query support for the market interface. |
| MQTT | Provides data services for real-time market conditions. |

---

## Developer documentation

| Market | Link |
| :--- | :--- |
| HK | https://developer.webull.hk/api-doc/ |
| US | https://developer.webull.com/api-doc/ |
| JP | https://developer.webull.co.jp/api-doc/ |
