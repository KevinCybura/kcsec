export default class ChartManager {
    constructor(card, cs_series = true, area_series = true) {
        this.chart_card = document.createElement("div");
        this.symbol = card.id;
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
            watermark: this.wartermark,
            handleScale: {
                axisPressedMouseMove: {
                    time: true,
                    price: false,
                },
            },
        });

        this.chart.name = card.id;
        this.cs_series = cs_series;
        this.area_series = area_series;

        if (this.cs_series)
            this.candlestickSeries = this.chart.addCandlestickSeries();
        if (this.area_series) this.areaSeries = this.chart.addAreaSeries();
    }

    async init_chart() {
        const response = await fetch("/crypto/chart_data/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": Cookies.get("csrftoken"),
            },
            body: JSON.stringify({symbol: this.symbol}),
        });
        const data = await response.json();
        await this.build_chart(data);
    }

    async build_chart(data) {
        if (this.area_series) this.areaSeries.setData(data);
        if (this.cs_series) this.candlestickSeries.setData(data);
    }

    async update_chart(message) {
        const coin_data = message["ohlcv"];

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
    get wartermark() {
        return {
            color: "rgba(11, 94, 29, 0.4)",
            visible: true,
            text: this.symbol,
            fontSize: 24,
            horzAlign: "left",
            vertAlign: "bottom",
        };
    }

    get priceScale() {
        return {
            autoScale: true,
            borderVisible: true,
            entireTextOnly: true,
            borderColor: "cadetblue",
            drawTicks: true,
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
            rightOffset: 20,
            barSpacing: 6,
            fixLeftEdge: true,
            lockVisibleTimeRangeOnResize: true,
            rightBarStaysOnScroll: false,
            borderVisible: true,
            borderColor: "cadetblue",
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
