[![PyPI](https://img.shields.io/pypi/v/aiotailf.svg)](https://pypi.org/project/aiotailf/) <img src="https://github.com/Yangzhenzhao/aiotailf/workflows/CI/badge.svg" />


### Installation

`pip install --upgrade aiotailf`        

### Examples

```py
import asyncio

from aiotailf import async_tail


async def tail_lines():
    async for line in async_tail("test.log"):
        print(line)


asyncio.run(tail_lines())
```


### BasedOn

<a href="https://gist.github.com/amitsaha/5990310#gistcomment-3305811" target="_blank">https://gist.github.com/amitsaha/5990310#gistcomment-3305811</a>


### Cli

```
Usage: tailf [OPTIONS] FILENAME

Options:
  --help  Show this message and exit.
```