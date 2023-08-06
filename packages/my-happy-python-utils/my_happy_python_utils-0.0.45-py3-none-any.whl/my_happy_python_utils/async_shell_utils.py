"""
async shell utils
"""
import asyncio



from . import version

__version__ = version.get_current()


async def run_commands(opt={}):

    process = await asyncio.create_subprocess_exec(
                        *opt['commands'],
                        stdin=asyncio.subprocess.DEVNULL,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        start_new_session=True,
                        cwd=opt['cwd'])

    stdout, stderr = await process.communicate()

    command_output_list = []

    if len(stderr) > 0:
        command_output_list.append(stderr.decode('utf-8'))

    if len(stdout) > 0:
        command_output_list.append(stdout.decode('utf-8'))

    command_output = '\n'.join(command_output_list)


    return command_output
