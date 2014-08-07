pyStock

Relational Diagram

Functional Dependencies
Broker
IDENTIFICATION_CODE -> NAME, ADDRESS, PHONE
Account

Tick
ASSET, REGISTER_NUMBER -> TICK_DATE, PRICE, BROKER_BUYER, BROKER_SELLER, rest of attributes

