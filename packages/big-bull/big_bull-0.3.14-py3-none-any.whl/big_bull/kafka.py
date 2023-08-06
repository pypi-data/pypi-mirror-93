import logging

import opentracing
from aiokafka import AIOKafkaConsumer
from big_bull import graph

logger = logging.getLogger("bigbull.kafka")

_kafka_consumer_registry = []


def get_kafka_consumer_span(message, tracer):
    logger.info("Received message with headers %s", message.headers)
    span_context = tracer.extract(
        format=opentracing.Format.HTTP_HEADERS,
        carrier=message.headers or {},
    )
    span = tracer.start_span(
        operation_name=f"from_{message.topic}", references=opentracing.follows_from(span_context)
    )
    span.set_tag("span.kind", "consumer")
    span.set_tag("message_bus.destination", message.topic)
    span.set_tag("message_bus.timestamp", message.timestamp)
    span.set_tag("message_bus.timestamp_type", message.timestamp_type)

    return span


def get_kafka_wrapper(func):
    async def inner(message, **kwargs):
        tracer = opentracing.global_tracer()
        span = get_kafka_consumer_span(message, tracer)
        with tracer.scope_manager.activate(span, True):
            return await func(message=message, **kwargs)
    return inner


def consumer(**kwargs):
    def decorator(func):
        _kafka_consumer_registry.append(func, kwargs)
        return get_kafka_wrapper(func)

    return decorator


async def kafka_consumer_task(func, fargs, *args, **kwargs):
    consumer = AIOKafkaConsumer(*args, **kwargs)
    try:
        await consumer.start()
        async for message in consumer:
            await get_kafka_wrapper(func)(message=message, **fargs)
    finally:
        await consumer.stop()


def register_kafka_consumers(injectables, loop):
    for (func, args, kwargs) in _kafka_consumer_registry:
        fargs = graph.get_arguments_to_inject(func, injectables, ignore_args=["message"])
        loop.create_task(kafka_consumer_task(func, fargs, *args, **kwargs))
