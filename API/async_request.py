import httpx
import asyncio
import yappi

async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def main():
    server_url = "http://127.0.0.1:8000" 
    urls = [f"{server_url}/" for _ in range(5)]

    results = await asyncio.gather(*[fetch(url) for url in urls])

    print(f"Results: {results}")

if __name__ == "__main__":

    yappi.set_clock_type("wall")
    yappi.start()

    asyncio.run(main())

    yappi.stop()
    stats = yappi.get_func_stats()
    stats.sort("ttot", sort_order="desc")
    stats.print_all()


# python -m profile <name>.py
