export default class InfoManager {
    constructor(symbol, component_id) {
        this.symbol = symbol;
        this.component = $("#" + component_id + "-" + this.symbol);
    }

    price_percent(price, percent) {
        return `${price} (${Number(percent).toFixed(2)}%)`;
    }

    async update_symbol(data) {
        this.component.find(`#price-${this.symbol}`).text(data["price"]);
        // Update today's percent and price change.
        let symbol_change = this.component.find(`#symbol-change-${this.symbol}`);
        symbol_change.text(
            this.price_percent(data["price_change"], data["percent_change"])
        );
    }

    async update_shares(data) {
        if (!data["share_data"]) {
            return;
        }
        const share_data = data["share_data"];
        // Updates today's return

        this._update_price_percent(
            `#todays-return-${this.symbol}`,
            share_data["todays_price"],
            share_data["todays_percent"]
        );

        // Updates total return
        this._update_price_percent(
            `#total-return-${this.symbol}`,
            share_data["total_price"],
            share_data["total_percent"]
        );
    }

    async update_form(data) {
        let price_form = this.component.find(`#id_${this.symbol}_price`);
        // Update placeholder price.
        price_form.attr("placeholder", data["price"]);
        // Update price if price is not a market_order.
        if (
            price_form.find(`#id_${this.symbol}_order_type :selected`).text() !==
            "market_order"
        ) {
            price_form.val(data["price"]);
        }
    }

    _update_price_percent(tag, price, percent) {
        let total_return = this.component.find(tag);
        total_return.text(this.price_percent(price, percent));
    }
}
