#! /usr/bin/env python3

import asyncio
import sys
import os
#local
import controller


async def loop(func, args=[]):
    while True:
        delay = getattr(controller, func)(*args)
        await asyncio.sleep(delay)

async def main():
    await asyncio.gather(
        loop('monitor'),
        loop('respond'),
        loop('operate'),
    )

async def input_enter():
    message = input("Press enter to quit\n\n")
    await message

### # TESTING # ###

def once():
    controller.monitor(test=True)
    controller.respond(test=True)
    controller.operate(test=True)

async def test():
    await asyncio.gather(
        loop('monitor', [1, True]),
        loop('respond', [0.05, True]),
        loop('operate', [5, True]),
    )


if __name__ == "__main__":
    command = sys.argv[1]
    if command == 'once':
        once()
    elif command == 'test':
        asyncio.run(test())
    elif command == 'git':
        os.chdir(os.getcwd() + "//ccci-controller")
        os.system('git config --global user.name “ccci-io” \
            && git config --global user.email “i@ccci.io” \
                && git add . && git commit -m "Dev commits" \
                    && git push origin master')
    elif command == 'run':
        asyncio.run(main())
    #globals()['age']
