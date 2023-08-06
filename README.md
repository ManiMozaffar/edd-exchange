# edd-exchange
This repo is only proto-type, that's why there's no github acion/test and etc.
A SOA EDD exchange service, that uses different APIs and currencies and crypto dynamically to deliver orders implemented with redis stream.
The reason I used redis stream was that I wanted to experience something different than Kafka and RabbitMQ.

Services:
  - IDENTITY: Authroize users
  - WEB APP: Web application for exchange backend
  - Exchanger: Exchange event driven application to perform exchange operation
  - Shared: shared library between services


Most codes are in shared service. Inside shared service:
  - Money: represent real money like USD
  - Crypto: represent crypto like Tether, Bitcoin and etc
  - Integration: represent API integration implementation, like BinanceAPI, to use to deliver the order
