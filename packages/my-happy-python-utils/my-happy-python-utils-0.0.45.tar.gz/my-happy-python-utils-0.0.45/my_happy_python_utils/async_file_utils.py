"""
async file utils
"""
import aiofiles

from pathlib import Path


from . import version

__version__ = version.get_current()


async def write_sh_file(opt={}):
    async with aiofiles.open(
                        Path(opt['file_name']),
                        mode='w',
                        encoding='utf-8') as f:
        await f.write('#!/bin/sh')
        await f.write('\n')
        await f.write(opt['data'])


async def write_text_file(opt={}):
    async with aiofiles.open(
                        Path(opt['file_name']),
                        mode='w',
                        encoding='utf-8') as f:
        await f.write(opt['data'])
