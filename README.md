pyStock

[![Build Status](https://travis-ci.org/llazzaro/pystock.svg)](https://travis-ci.org/llazzaro/pystock) [![Coverage Status](https://coveralls.io/repos/llazzaro/pystock/badge.svg?branch=master&service=github)](https://coveralls.io/github/llazzaro/pystock?branch=master)

Relational Diagram

Functional Dependencies
Broker
IDENTIFICATION_CODE -> NAME, ADDRESS, PHONE
Account

Tick
ASSET, REGISTER_NUMBER -> TICK_DATE, PRICE, BROKER_BUYER, BROKER_SELLER, rest of attributes

