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
            asset_id_base: symbol_id.slice(0, 3),
            asset_id_quote: symbol_id.slice(3),
            limit: 1,
            o: "-time_open",
        }).toString();

        const response = await fetch(url, {method: "GET"});
        data[symbol_id] = await response.json();
    }
    update_price(data, symbol_ids);
};

socket.onmessage = async function (e) {
    const message = JSON.parse(e.data)["message"];
    for (const symbol of symbol_ids) {
        if (!Object.keys(message).includes(symbol)) continue;
        update_price(message[symbol]["ohlcv"], symbol);
        $("#info-card-" + symbol)
            .find(`#${symbol}-percent-change span`)
            .text(message[symbol]["updated_share"]["percent_change"]);
    }
};

socket.onclose = function (_) {
    console.error("Socket closed unexpectedly");
};

function update_price(data, symbols) {
    for (const symbol of symbols) {
        let info_body = $("#" + symbol).find(".symbol-price");
        info_body.text("$" + Number(data[symbol][0].close).toFixed(2));
    }
}

// ============================== End Chart/Sockets ====================
