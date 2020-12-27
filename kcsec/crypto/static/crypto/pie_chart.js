Chart.defaults.derivedDoughnut = Chart.defaults.doughnut;
Chart.controllers.derivedDoughnut = Chart.controllers.doughnut.extend({
    draw: function (ease) {
        const formatter = new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
        });
        Chart.controllers.doughnut.prototype.draw.apply(this, [ease]);
        const width = this.chart.chart.width,
            height = this.chart.chart.height,
            titleHeight = this.chart.titleBlock.height,
            legendHeight = this.chart.legend.height;
        const total = formatter.format(this.getMeta().total);
        const ctx = this.chart.chart.ctx;
        const fontSize = (
            this.chart.chart.width /
            (ctx.measureText(total.toString()).width * 7)
        ).toFixed(2);
        ctx.font = fontSize + "em Verdana";
        ctx.textBaseline = "middle";
        const text = total,
            textX = Math.round((width - ctx.measureText(text).width) / 2),
            textY = (height + titleHeight + legendHeight) / 2;

        ctx.fillText(text, textX, textY);
    },
});
