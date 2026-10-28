import asyncio
import aiohttp
import aiofiles
from prettytable import PrettyTable
import os

async def downloading(session, link, path):
    try:
        async with session.get(link) as response:
            if response.status == 200:
                img = await response.read()
                file_name = os.path.join(path, link.split('/')[-1])
                async with aiofiles.open(file_name, 'wb') as f:
                    await f.write(img)
                return link, "OK"
            else:
                return link, "Error"
    except:
        return link, "Error"

async def main():
    path = input("Enter the path where the images will be saved: ").strip()

    while not os.path.isdir(path) or not os.access(path, os.W_OK):
        print("You cannot access the directory or the path is incorrect. Please try again.")
        path = input("Enter the path where the images will be saved: ").strip()

    tasks = []
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        while True:
            link = input("Enter the image link: ").strip()

            if not link:
                break

            task = asyncio.create_task(downloading(session, link, path))
            tasks.append(task)

        if tasks and not all(task.done() for task in tasks):
            print("Download...")

        results = await asyncio.gather(*tasks) if tasks else []

    table = PrettyTable(["Link", "Status"])
    for link, status in results:
        table.add_row([link, status])

    print(table)

if __name__ == "__main__":
    asyncio.run(main())