[![PyPI](https://img.shields.io/pypi/v/aiotailf.svg)](https://pypi.org/project/aiotailf/) <img src="https://github.com/Yangzhenzhao/aiotailf/workflows/CI/badge.svg" />


### Installation

安装: `pip install --upgrade aiotailf`        
卸载: `pip uninstall aiotailf -y`  

### Examples

```py
import asyncio


async def tail_lines():
    async for line in async_tail("test.log"):
        print(line)


loop = asyncio.get_event_loop()
loop.run_until_complete(print_line())
```


### BasedOn

<a href="https://gist.github.com/amitsaha/5990310#gistcomment-3305811" target="_blank">https://gist.github.com/amitsaha/5990310#gistcomment-3305811</a>


### Cli

```
Usage: tailf [OPTIONS] FILENAME

Options:
  --help  Show this message and exit.
```