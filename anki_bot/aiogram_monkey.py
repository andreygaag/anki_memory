import asyncio
from asyncio import Future
from typing import Optional

from aiogram.utils import executor
from aiogram.utils.executor import _setup_callbacks


class MyExecutor(executor.Executor):
    async def start_polling(
        self,
        reset_webhook=None,
        timeout=20,
        relax=0.1,
        fast=True,
        allowed_updates: Optional[list[str]] = None,
    ):
        """
        Start bot in long-polling mode

        :param reset_webhook:
        :param timeout:
        """
        self._prepare_polling()
        loop = asyncio.get_event_loop()
        if loop.is_running():
            try:
                await self._startup_polling()
                asyncio.create_task(
                    self.dispatcher.start_polling(
                        reset_webhook=reset_webhook,
                        timeout=timeout,
                        relax=relax,
                        fast=fast,
                        allowed_updates=allowed_updates,
                    ),
                )
                await Future()
            except (KeyboardInterrupt, SystemExit):
                pass
            finally:
                asyncio.create_task(self._shutdown_polling())
        else:
            try:
                loop.run_until_complete(self._startup_polling())
                loop.create_task(
                    self.dispatcher.start_polling(
                        reset_webhook=reset_webhook,
                        timeout=timeout,
                        relax=relax,
                        fast=fast,
                        allowed_updates=allowed_updates,
                    ),
                )
                loop.run_forever()
            except (KeyboardInterrupt, SystemExit):
                # loop.stop()
                pass
            finally:
                loop.run_until_complete(self._shutdown_polling())
                log.warning("Goodbye!")  # type: ignore


async def start_polling(
    dispatcher,
    *,
    loop=None,
    skip_updates=False,
    reset_webhook=True,
    on_startup=None,
    on_shutdown=None,
    timeout=20,
    relax=0.1,
    fast=True,
    allowed_updates: Optional[list[str]] = None
):
    executor = MyExecutor(dispatcher, skip_updates=skip_updates, loop=loop)
    _setup_callbacks(executor, on_startup, on_shutdown)

    await executor.start_polling(
        reset_webhook=reset_webhook,
        timeout=timeout,
        relax=relax,
        fast=fast,
        allowed_updates=allowed_updates,
    )
