import ChartManager from "./chart_manager.js";
import InfoManager from "./info_manager.js";

const cards = $("div.chart").toArray();

const managers = cards.reduce(
    (o, card) =>
        Object.assign(o, {
            [card.id]: {
                info: new InfoManager(card.id, "info-card"),
                chart: new ChartManager(card),
            },
        }),
    {}
);

const ws_scheme = window.location.protocol  === "https:" ? "wss" : "ws";
const socket = new WebSocket(ws_scheme + "://" + window.location.host + "/ws/crypto/");

socket.onopen = async function (_) {
    socket.send(
        JSON.stringify({
            symbols: Object.keys(managers),
        })
    );
    for await (const [_, manager] of Object.entries(managers)) {
        await manager["chart"].init_chart();
    }
};

socket.onmessage = async function (e) {
    const message = JSON.parse(e.data)["message"];
    const manager = managers[message["symbol"]];

    await manager["chart"].update_chart(message);
    await manager["info"].update_symbol(message);
    await manager["info"].update_shares(message);
    await manager["info"].update_form(message);
};

socket.onclose = function (_) {
    console.error("Socket closed unexpectedly");
};

$(window).resize(function () {
    Object.values(managers).forEach((manager) => {
        manager["chart"].resize();
    });
});

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
