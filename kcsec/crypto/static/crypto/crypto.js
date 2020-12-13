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
  const csrftoken = Cookies.get("csrftoken");
  for await (const manager of charts_managers) {
    const response = await fetch("http://localhost:8000/crypto/chart_data/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
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
  let info_body = $("#info-" + symbol).children(".symbol-price");
  info_body.text("$" + data[data.length - 1].close);
  let table = $(".order-table-" + symbol);

  let price_form = table.find(`#id_${symbol}_price`);
  price_form = price_form.length === 0 ? price_form : table.find("#id_price");
  price_form.attr("placeholder", "$" + data[data.length - 1].close);
  price_form.val(data[data.length - 1].close);

  let quantity_form = table.find(`#id_${symbol}_shares`);
  quantity_form.attr("placeholder", "0");
}

// ============================== End Chart/Sockets ====================

$(".btn-trade-type-radio").click(function () {
  // Set trade-type choice to active.
  $(".btn-trade-type-radio").removeClass("active");
  $(this).addClass("active");
});

$(function (e) {
  const order_type = $(this).find("select[id$='order_type']").val();
  if (order_type === "Market Order") {
    $(this).find(".order-price").attr("disabled", true);
  } else {
    $(this).find(".order_price").removeAttr("disabled");
  }
});

// Disable price if its a Market Order.
$(".order-btn-dropdown select").change(function () {
  const option = $(this).val();
  const parent = $(this).closest(".info-content");

  const table = parent.find(".order-table");
  const symbol = table.find("input[id$='crypto_symbol'").val();
  if (option === "Market Order") {
    let form = $(this).closest("form");
    let price_form = form.find("#id_price");
    price_form =
      price_form.length === 0 ? form.find(`#id_${symbol}_price`) : price_form;
    price_form.attr("disabled", true);
  } else if (option === "Limit Order") {
    let form = $(this).closest("form");
    let price_form = form.find("#id_price");
    price_form =
      price_form.length === 0 ? form.find(`#id_${symbol}_price`) : price_form;
    price_form.attr("disabled", false);
  }
});
