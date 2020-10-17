import ChartManager from "./chart_manager.js";

const cards = Array.from(document.getElementsByClassName("chart"));

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

  for await (const manager of charts_managers) {
    const response = await fetch("http://localhost:8000/crypto/chart_data/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbol: manager.symbol }),
    });
    const data = await response.json();

    await manager.build_chart(data);
    await update_price(data, manager.symbol);
  }
};

socket.onmessage = async function (e) {
  const message = JSON.parse(e.data)["message"];
  for (const manager of charts_managers) {
    if (!Object.keys(message).includes(manager.symbol)) continue;
    await manager.update_chart(message);
    await update_price(message[manager.symbol]["ohlcv"], manager.symbol);
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

async function update_price(data, symbol) {
  let info_body = $("#info-" + symbol).children(".price");
  info_body.text(data[data.length - 1].close);
}
