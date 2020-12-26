import ChartManager from "./chart_manager.js";

const cards = $("div.chart").toArray();

let charts_managers = cards.map((card) => {
    return new ChartManager(card);
});

const socket = new WebSocket("ws://" + window.location.host + "/ws/crypto/");

socket.onopen = async function (_) {
    socket.send(
        JSON.stringify({
            symbols: charts_managers.map((chart) => chart.symbol),
        })
    );
    const csrftoken = Cookies.get("csrftoken");
    for await (const manager of charts_managers) {
        const response = await fetch("http://localhost:8000/crypto/chart_data/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({symbol: manager.symbol}),
        });
        const data = await response.json();

        await manager.build_chart(data);
        await update_info(data, manager.symbol);
    }
};

socket.onmessage = async function (e) {
    const message = JSON.parse(e.data)["message"];
    for (const manager of charts_managers) {
        if (message["symbol"] !== manager.symbol) continue;
        await manager.update_chart(message);
        await update_info(message, manager.symbol, true);
    }
};

socket.onclose = function (_) {
    console.error("Socket closed unexpectedly");
};

$(window).resize(function () {
    charts_managers.forEach((chart_manager) => {
        chart_manager.resize();
    });
});

async function update_info(data, symbol, is_message = false) {
    const info_card = $(`#info-card-${symbol}`);
    const price = data["ohlcv"] ? data["ohlcv"] : data;

    // Update main price.
    info_card
        .find(`#${symbol}-price`)
        .text("$" + Number(price[price.length - 1].close).toFixed(2));

    let price_form = info_card.find(`#id_${symbol}_price`);
    price_form =
        price_form.length !== 0 ? price_form : info_card.find("#id_price");
    // Update placeholder price.
    price_form.attr(
        "placeholder",
        "$" + Number(price[price.length - 1].close).toFixed(2)
    );
    // Update price if price is not a market_order.
    if (
        price_form.find(`#id_${symbol}_order_type :selected`).text() !==
        "market_order"
    ) {
        price_form.val(Number(price[price.length - 1].close).toFixed(2));
    }

    if (is_message) {
        // Update today's percent and price change.
        let symbol_change = info_card.find(`#todays-change-${symbol}`);
        symbol_change.text(
            `$${Number(data["price_change"]).toFixed(2)} (${Number(
                data["percent_change"]
            ).toFixed(2)}%)`
        );
    }
    if (data["shares"]) {
        const share_data = data["share_data"];
        // Updates today's return
        let todays_return = info_card.find(`#todays-return-${symbol}`);
        todays_return.text(
            `${Number(share_data["todays_price"]).toFixed(2)} (${Number(
                share_data["todays_percent"]
            ).toFixed(2)}%)`
        );

        // Updates total return
        let total_return = info_card.find(`#total-return-${symbol}`);
        total_return.text(
            `${Number(share_data["total_price"]).toFixed(2)} (${Number(
                share_data["total_percent"]
            ).toFixed(2)}%)`
        );
    }
}

// ============================== End Chart/Sockets ====================

$(".btn-trade-type-radio").click(function () {
    // Set trade-type choice to active.
    $(".btn-trade-type-radio").removeClass("active");
    $(this).addClass("active");
});

// Disable price if order_type is a Market Order.
$(".order-btn-dropdown select").change(function () {
    const option = $(this).val();
    // Get current
    const symbol = $(this)
        .closest(".info-content")
        .find(".order-table")
        .find("input[id$='symbol']")
        .val();

    if (option === "market_order") {
        let form = $(this).closest("form");
        let price_form = form.find("#id_price");
        price_form =
            price_form.length === 0 ? form.find(`#id_${symbol}_price`) : price_form;
        price_form.attr("disabled", true);
    } else if (option === "limit_order") {
        let form = $(this).closest("form");
        let price_form = form.find("#id_price");
        price_form =
            price_form.length === 0 ? form.find(`#id_${symbol}_price`) : price_form;
        price_form.attr("disabled", false);
    }
});
