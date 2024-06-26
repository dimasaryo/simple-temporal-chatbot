import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from chat_workflow import ChatWorkflow, bot_reply

interrupt_event = asyncio.Event()


async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="chatbot-task-queue",
        activities=[
            bot_reply,
        ],
        workflows=[ChatWorkflow],
    ):
        logging.info("Worker started, ctrl+c to exit")
        await interrupt_event.wait()
        logging.info("Shutting down")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())

