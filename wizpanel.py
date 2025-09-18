import aiohttp
import asyncio
import sys
from time import time

class ignore:
  def write(self):
    pass

sys.stderr = ignore()

now = time()

address = sys.argv[1]
address = address if address[-1] == '/' else address+'/'

async def check_range(session, start, end):
    tasks = []
    chunk_size = (end - start) // int(sys.argv[2])
    for i in range(start, end, chunk_size):
        chunk_start = i
        chunk_end = i + chunk_size if i + chunk_size < end else end
        task = asyncio.create_task(check_range_chunk(session, chunk_start, chunk_end))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return any(results)

async def check_range_chunk(session, start, end):
    for i in range(start, end):
        url = f'{address}wizpanel10{str(i).zfill(5)}/login.php'
        async with session.get(url) as response:
            if response.status == 200:
                print(f'{address}wizpanel10{str(i).zfill(5)}')
                print(time()-now)
                exit()

async def main():
    async with aiohttp.ClientSession() as session:
        result = await check_range(session, 0, 100000)

if __name__ == "__main__":
    asyncio.run(main())
