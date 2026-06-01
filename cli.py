import click
from bot.client import BinanceFuturesClient

@click.command()
@click.option('--symbol', required=True, help='e.g., BTCUSDT, ETHUSDT')
@click.option('--side', type=click.Choice(['BUY', 'SELL'], case_sensitive=False), required=True, help='Order side')
@click.option('--type', 'order_type', type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False), required=True, help='Order type')
@click.option('--quantity', type=float, required=True, help='Order quantity')
@click.option('--price', type=float, help='Required only if order type is LIMIT')
def main(symbol, side, order_type, quantity, price):
    """Primetrade.ai - Simplified Trading Bot for Binance Futures Testnet"""
    
    # Input Validation: Agar limit order hai aur price nahi di
    if order_type.upper() == "LIMIT" and not price:
        click.echo(click.style("Error: --price dena zaroori hai agar order type LIMIT ho!", fg="red"))
        return

    click.echo(click.style("=== Order Request Summary ===", fg="cyan"))
    click.echo(f"Symbol: {symbol.upper()}\nSide: {side.upper()}\nType: {order_type.upper()}\nQuantity: {quantity}")
    if price:
        click.echo(f"Price: {price}")
    click.echo("=============================\n")

    try:
        # Client initialize karna aur order lagana
        client = BinanceFuturesClient()
        result = client.place_order(symbol, side, order_type, quantity, price)

        if result["success"]:
            data = result["data"]
            click.echo(click.style("✓ ORDER PLACED SUCCESSFULLY", fg="green", bold=True))
            click.echo(f"Order ID: {data.get('orderId')}")
            click.echo(f"Status: {data.get('status')}")
            click.echo(f"Executed Qty: {data.get('executedQty')}")
            click.echo(f"Avg Price: {data.get('avgPrice', 'N/A')}")
        else:
            click.echo(click.style(f"✗ ORDER FAILED: {result['error']}", fg="red", bold=True))

    except Exception as e:
        click.echo(click.style(f"✗ CRITICAL ERROR: {str(e)}", fg="red", bold=True))

if __name__ == "__main__":
    main()