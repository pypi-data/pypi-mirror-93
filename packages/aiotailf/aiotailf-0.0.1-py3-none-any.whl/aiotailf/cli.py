import asyncio

import click

from . import async_tail


@click.command()
@click.argument("filename")
def cli(filename):

    async def print_line():
        async for line in async_tail(filename):
            print(line)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_line())
