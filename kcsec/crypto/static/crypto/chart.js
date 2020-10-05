const cards = Array.from(document.getElementsByClassName("chart"));

let coins = cards.map((card) => card.getAttribute("ws-symbol"));
let charts = cards.map(create_chart);

const chart_info = {};
for (const chart of charts) {
  chart_info[chart.name] = build_chart(chart);
}

const socket = new WebSocket("ws://" + window.location.host + "/ws/crypto/");

socket.onopen = function (e) {};

socket.onmessage = async function (e) {
  const message = JSON.parse(e.data)["message"];
  const keys = Object.keys(message);
  for (const coin of keys) {
    if (coin in chart_info) {
      const coin_data = message[coin]["ohlcv"];
      const chart = await chart_info[coin];
      if (coin_data.length === 1) {
        chart["candle_stick_series"].update(coin_data[0]);
        chart["area_series"].update(coin_data[0]);
      } else {
        chart["candle_stick_series"].setData(coin_data);
        chart["area_series"].setData(coin_data);
      }
    }
  }
};

socket.onclose = function (_) {
  console.error("Socket closed unexpectedly");
};

$(window).resize(function () {
  charts.forEach((chart) => {
    const coin_body = $(".chart-body");
    chart.applyOptions({
      width: coin_body.innerWidth(),
      height: coin_body.innerHeight(),
    });
    chart.timeScale().scrollToRealTime();
  });
});

function create_chart(card) {
  let chart_card = document.createElement("div");
  chart_card.id = "chart-" + card.getAttribute("ws-symbol");

  card.appendChild(chart_card);
  let chart = LightweightCharts.createChart(chart_card, {
    width: card.width,
    height: card.height,
  });
  chart.applyOptions({
    priceScale: {
      autoScale: true,
      borderVisible: true,
      entireTextOnly: true,
      borderColor: "cadetblue",
      drawTicks: false,
      scaleMargins: {
        top: 0.3,
        bottom: 0.25,
      },
    },
    layout: {
      backgroundColor: "#FAEBD7",
      textColor: "#696969",
      fontSize: 12,
      fontFamily: "Calibri",
    },
    timeScale: {
      rightOffset: 100,
      barSpacing: 3,
      fixLeftEdge: true,
      lockVisibleTimeRangeOnResize: true,
      rightBarStaysOnScroll: true,
      borderVisible: false,
      borderColor: "#fff000",
      visible: true,
      timeVisible: true,
      secondsVisible: false,
    },
    grid: {
      vertLines: {
        color: "rgba(70, 130, 180, 0.5)",
        style: 2,
        visible: true,
      },
      horzLines: {
        color: "rgba(70, 130, 180, 0.5)",
        style: 2,
        visible: true,
      },
    },
  });

  chart.name = card.getAttribute("ws-symbol");
  return chart;
}

async function build_chart(chart) {
  const response = await fetch("http://localhost:8000/crypto/chart_data/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symbol: chart.name }),
  }).catch((e) => {
    console.error(e);
  });
  const coin_data = await response.json();
  const candlestickSeries = chart.addCandlestickSeries();
  candlestickSeries.setData(coin_data);

  const areaSeries = chart.addAreaSeries();
  areaSeries.setData(coin_data);

  return {
    candle_stick_series: candlestickSeries,
    area_series: areaSeries,
  };
}
