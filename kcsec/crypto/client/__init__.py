from kcsec.crypto.client.consumer import Consumer
from kcsec.crypto.client.gemini import GeminiConsumer
from kcsec.crypto.client.order_book import OrderBook

connections = [
    ("wss://api.gemini.com/v2/marketdata", GeminiConsumer),
]
