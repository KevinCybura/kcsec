# PaperTrader

***

This django application is an online paper trading platform 
for cryptocurrencies. ["A paper trade is a simulated trade that allows an investor to practice buying
and selling without risking real money"](https://www.investopedia.com/terms/p/papertrade.asp)

## Requirements
* Postgres
* Redis
* [Poetry](https://python-poetry.org/)
## Quick start

```bash
poetry install
make db
make crypto_sockets
# In another terminal
make serve
```

## Project architecture

There are three main parts to this app the django web server which serves data to the user, 
websocket connection through which the frontend receives real time data from the backend, and a
consumer that receives real time data from a third party api and push it to the django server.

### Django server
Serves static files, user and cryptocurrency data to the frontend. The websocket connections and 
messages from the frontend is also run on the server.

### Websocket server
The websocket connections between the server and the frontend are how the frontend is able to
receive realtime data. This is done using django [channels](
https://channels.readthedocs.io/en/stable/). When a user goes to view a certain cryptocurrency
the frontend attempts to establish a websocket connection and sends the serve the 
`cryptocurrency_id` and the `user_id` if there is one. The `cryptocurrency_id` is used to ignore
messages from the real time data consumer if the message is for a different cryptocurrency which
prevents a server from pushing irrelevant data. If the user is logged in the frontend sends a
`user_id`, the backend uses the id query the database for the users shares which are used to 
calculate other data such as `percent_change` and `equity_change`.

### Real time data consumer

Real time data consumer, consumes the gemini websocket api for realtime candle stick data. When a
message comes in the data is store, processed then sent to the crypto channels group which the 
Websocket server receives and sends to the front end.
