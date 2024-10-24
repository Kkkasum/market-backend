import asyncio

from src.repo.fill import Fill


async def main():
    await Fill().all()


if __name__ == '__main__':
    asyncio.run(main())
