export default class ChartManager {
    constructor(
        card,
        id = "ws-symbol",
        cs_series = true,
        area_series = true,
    ) {
        this.chart_card = document.createElement("div");
        this.symbol = card.getAttribute(id).toString();
        this.chart_card.id = "chart-" + this.symbol;

        card.appendChild(this.chart_card);
        this.chart = LightweightCharts.createChart(this.chart_card, {
            width: card.width,
            height: card.height,
        });
        this.chart.applyOptions({
            priceScale: this.priceScale,
            layout: this.layout,
            timeScale: this.timeScale,
            grid: this.grid,
        });

        this.chart.name = card.getAttribute(id);
        this.cs_series = cs_series;
        this.area_series = area_series;

        if (this.cs_series)
            this.candlestickSeries = this.chart.addCandlestickSeries();
        if (this.area_series) this.areaSeries = this.chart.addAreaSeries();
    }

    async build_chart(data) {
        if (this.area_series) this.areaSeries.setData(data);
        if (this.cs_series) this.candlestickSeries.setData(data);
    }

    async update_chart(message) {
        const coin_data = message[this.symbol]["ohlcv"];

        if (coin_data.length === 1) {
            if (this.cs_series) this.candlestickSeries.update(coin_data[0]);
            if (this.area_series) this.areaSeries.update(coin_data[0]);
        } else {
            if (this.cs_series) this.candlestickSeries.update(coin_data);
            if (this.area_series) this.areaSeries.update(coin_data);
        }
    }

    resize(symbol_body = ".chart-body") {
        const coin_body = $(symbol_body);
        this.chart.applyOptions({
            width: coin_body.innerWidth(),
            height: coin_body.innerHeight(),
        });
        this.chart.timeScale().scrollToRealTime();
    }

    // START OPTIONS
    get priceScale() {
        return {
            autoScale: true,
            borderVisible: true,
            entireTextOnly: true,
            borderColor: "cadetblue",
            drawTicks: false,
            scaleMargins: {
                top: 0.3,
                bottom: 0.25,
            },
        };
    }

    get layout() {
        return {
            backgroundColor: "#FAEBD7",
            textColor: "#696969",
            fontSize: 12,
            fontFamily: "Calibri",
        };
    }

    get timeScale() {
        return {
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
        };
    }

    get grid() {
        return {
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
        };
    }

    // END OPTIONS
}
