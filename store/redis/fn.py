from redis import Redis

from store.redis import redis_pool


def sync_publish(event: str, msg):
    # if jh.is_unit_testing():
    #     raise EnvironmentError(
    #         "sync_publish() should be NOT called during testing. There must be something wrong"
    #     )
    #
    # async with Redis(connection_pool=redis_pool) as redis:
    #     await redis.publish(
    #     f"{ENV_VALUES['APP_PORT']}:channel:1",
    #     json.dumps(
    #         {"id": os.getpid(), "event": f"{jh.app_mode()}.{event}", "data": msg},
    #         ignore_nan=True,
    #         cls=NpEncoder,
    #     ),
    # )
    ...
