import asyncio
from asyncio import Future
from typing import Optional

from aiogram.utils import executor
from aiogram.utils.executor import _setup_callbacks


class CurrentEventLoopExecutor(executor.Executor):
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


async def start_polling_in_current_loop(
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
    executor = CurrentEventLoopExecutor(
        dispatcher,
        skip_updates=skip_updates,
        loop=loop,
    )
    _setup_callbacks(executor, on_startup, on_shutdown)

    await executor.start_polling(
        reset_webhook=reset_webhook,
        timeout=timeout,
        relax=relax,
        fast=fast,
        allowed_updates=allowed_updates,
    )
