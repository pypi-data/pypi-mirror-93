import asyncio

import click

from . import async_tail


@click.command()
@click.argument("filename")
def cli(filename):
    async def print_line():
        async for line in async_tail(filename):
            print(line)

    asyncio.run(print_line())
