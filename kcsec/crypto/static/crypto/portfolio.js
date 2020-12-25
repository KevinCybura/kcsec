const cards = Array.from($(".share-card"));
const symbol_ids = cards.map((card) => card.id);

const socket = new WebSocket("ws://" + window.location.host + "/ws/crypto/");

socket.onopen = async function (_) {
    socket.send(
        JSON.stringify({
            symbols: symbol_ids,
        })
    );
};

socket.onmessage = async function (e) {
    const message = JSON.parse(e.data)["message"];
    update_price(message, message["symbol"], true);
};

socket.onclose = function (_) {
    console.error("Socket closed unexpectedly");
};

function update_price(data, symbol, is_message = false) {
    const price = data["ohlcv"] ? data["ohlcv"] : data;
    let card_body = $("#" + symbol);
    card_body
        .find(`#price-${symbol}`)
        .text("$" + Number(price[0].close).toFixed(2));

    if (is_message) {
        const share_data = data["share_data"];
        // Update today's percent and price change.
        let price = card_body.find(`#symbol-change-${symbol}`);
        price.text(
            `${Number(data["price_change"]).toFixed(2)} (${Number(
                data["percent_change"]
            ).toFixed(2)}%)`
        );

        // Updates today's return
        let todays_return = card_body.find(`#todays-return-${symbol}`);
        todays_return.text(
            `${Number(share_data["todays_price"]).toFixed(2)} (${Number(
                share_data["todays_percent"]
            ).toFixed(2)}%)`
        );

        // Updates total return
        let total_return = card_body.find(`#total-return-${symbol}`);
        total_return.text(
            `${Number(share_data["total_price"]).toFixed(2)} (${Number(
                share_data["total_percent"]
            ).toFixed(2)}%)`
        );
    }
}

// ============================== End Chart/Sockets ====================
