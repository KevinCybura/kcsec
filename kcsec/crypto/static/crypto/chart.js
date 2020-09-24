const cards = Array.from(document.getElementsByClassName("coin-body"));
let charts = cards.map(create_chart);
let coins = cards.map((card) => card.getAttribute("ws-coin"));
const socket = new WebSocket("ws://" + window.location.host + "/ws/crypto/");
socket.onopen = function (e) {
  socket.send(
    JSON.stringify({
      coins: coins,
    })
  );
};

socket.onmessage = function (e) {
  const message = JSON.parse(e.data)["message"];
  charts.forEach((chart) => {
    const ohlcv = message[chart.name];
    if (ohlcv) {
      const ohlcv2 = ohlcv["ohlcv"] || [];
      const candlestickSeries = chart.addCandlestickSeries();
      candlestickSeries.setData(ohlcv2);
      const areaSeries = chart.addAreaSeries();
      areaSeries.setData(ohlcv2);
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
    timeScale: {
      rightOffset: 12,
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
  });
  const candlestickSeries = chart.addCandlestickSeries();
  candlestickSeries.setData([]);
  const areaSeries = chart.addAreaSeries();
  areaSeries.setData([]);
  chart.name = card.getAttribute("ws-coin");
  return chart;
}
