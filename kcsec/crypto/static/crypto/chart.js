const preloaded_ohlcv = JSON.parse(
  document.getElementById("preloaded-ohlcv").textContent
);
const cards = Array.from(document.getElementsByClassName("coin-body"));

let coins = cards.map((card) => card.getAttribute("ws-coin"));
let charts = cards.map(create_chart);

const socket = new WebSocket("ws://" + window.location.host + "/ws/crypto/");

let chart_info = {};
charts.forEach((chart) => {
  const candlestickSeries = chart.addCandlestickSeries();
  candlestickSeries.setData(preloaded_ohlcv[chart.name]);

  const areaSeries = chart.addAreaSeries();
  areaSeries.setData(preloaded_ohlcv[chart.name]);

  chart_info[chart.name] = {
    candle_stick_series: candlestickSeries,
    area_series: areaSeries,
  };
});

socket.onopen = function (e) {};

socket.onmessage = function (e) {
  const message = JSON.parse(e.data)["message"];
  Object.keys(message).forEach((coin) => {
    if (coin in chart_info) {
      const coin_data = message[coin]["ohlcv"];
      chart_info[coin]["candle_stick_series"].update(coin_data[0]);
      chart_info[coin]["area_series"].update(coin_data[0]);
    }
  });
};

socket.onclose = function (_) {
  console.error("Socket closed unexpectedly");
};

$(window).resize(function () {
  charts.forEach((chart) => {
    const coin_body = $(".coin-body");
    chart.applyOptions({
      width: coin_body.innerWidth(),
      height: coin_body.innerHeight() * 0.9,
    });
    chart.timeScale().scrollToRealTime();
  });
});

function create_chart(card) {
  let chart_card = document.createElement("div");
  chart_card.id = "coin-chart-" + card.getAttribute("ws-coin");

  chart_card.style = "position: absolute; width: 100%; height: 90%;";
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

  chart.name = card.getAttribute("ws-coin");
  return chart;
}
