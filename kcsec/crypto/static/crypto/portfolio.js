import InfoManager from "./info_manager.js";

const cards = Array.from($(".share-card"));
const symbol_ids = cards.map((card) => card.id);
const info_managers = cards.reduce(
    (o, card) => Object.assign(o, {[card.id]: new InfoManager(card.id, "")}),
    {}
);

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

    let manager = info_managers[message["symbol"]];
    await manager.update_shares(message);
    await manager.update_symbol(message);
};

socket.onclose = function (_) {
    console.error("Socket closed unexpectedly");
};


// ============================== End Sockets ====================

$(document).ready(async function () {
    const user_id = $("#user_id").text();
    const csrftoken = Cookies.get("csrftoken");
    let url = new URL("http://localhost:8000/crypto/chart");

    url.search = new URLSearchParams({
        user_id: user_id,
    }).toString();

    const response = await fetch(url, {
        method: "GET",
        headers: {
            "X-CSRFTOKEN": csrftoken,
        },
    });

    const data = await response.json();

    let ctx = $("#share-chart").get(0).getContext("2d");
    new Chart(ctx, {
        type: "derivedDoughnut",
        data: data.data,
        options: {
            responsive: true,
            legend: {
                labels: {
                    fontColor: "#ccc",
                },
            },
        },
    });
});
