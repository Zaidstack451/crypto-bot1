import asyncio
import aiohttp

TELEGRAM_TOKEN = "8843319352:AAFbTYSHeHUAWe_FTpG0wBVWjtp3fSf-YA"
TELEGRAM_CHAT_ID = "@zaid_crypto_smc_signals"

SYMBOLS = ["BTC_USDT", "ETH_USDT", "SOL_USDT", "XRP_USDT", "AVAX_USDT", "ADA_USDT", "DOGE_USDT", "LINK_USDT", "NEAR_USDT", "SUI_USDT"]

async def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        async with aiohttp.ClientSession() as session:
            await session.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"})
    except: pass

async def check_symbol(symbol):
    url = f"https://contract.mexc.com/api/v1/contract/kline/{symbol}?interval=Min15"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()
                if "data" in data:
                    c_price = float(data["data"]["close"][-1])
                    await send_telegram(f"Bot Active: {symbol} Price: {c_price}")
    except: pass

async def main():
    while True:
        tasks = [check_symbol(s) for s in SYMBOLS]
        await asyncio.gather(*tasks)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
