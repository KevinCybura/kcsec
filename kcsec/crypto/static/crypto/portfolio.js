const cards = Array.from($(".share-card"));
const symbol_ids = cards.map((card) => card.id);

const socket = new WebSocket("ws://" + window.location.host + "/ws/crypto/");

socket.onopen = async function (_) {
    socket.send(
        JSON.stringify({
            symbols: symbol_ids,
        })
    );

    let data = {};
    let url = new URL("http://localhost:8000/crypto/ohlcv/");

    for await (const symbol_id of symbol_ids) {
        url.search = new URLSearchParams({
            symbol: symbol_id,
            exchange: "gemini",
            limit: 1,
            o: "-time_open",
        }).toString();

        const response = await fetch(url.toString(), {method: "GET"});
        data[symbol_id] = await response.json();
    }
    symbol_ids.forEach((symbol) => update_price(data[symbol], symbol));
};

socket.onmessage = async function (e) {
    const message = JSON.parse(e.data)["message"];
    for (const symbol of symbol_ids) {
        if (!Object.keys(message).includes(symbol)) continue;
        update_price(message[symbol], symbol);
    }
};

socket.onclose = function (_) {
    console.error("Socket closed unexpectedly");
};

function update_price(data, symbol, is_message = false) {
    const price = data["ohlcv"] ? data["ohlcv"] : data;
    let info_body = $("#" + symbol).find(".symbol-price");
    console.log(data);
    info_body.text("$" + Number(price[0].close).toFixed(2));

    if (is_message) {
        $("#info-card-" + symbol)
            .find(`#${symbol}-percent-change span`)
            .text(data["updated_share"]["total_percent_change"]);
        // Update today's percent and price change.
        const change = data["24h_change"];
        let price = info_body.find(`#todays-change-${symbol}`);
        price.text(
            `${Number(change["price_change"]).toFixed(2)} (${Number(
                change["percent_change"]
            ).toFixed(2)}%)`
        );
    }
}

// ============================== End Chart/Sockets ====================
