from typing import (
    Tuple,
    Union,
    Callable,
    Awaitable,
    Optional,
    TypeVar
)

import inspect
import asyncio


RetryPolicyStrategy = Tuple[bool, Union[int, float]]

RetryPolicy = Callable[[int, Exception], RetryPolicyStrategy]
BeforeRetry = Callable[[int, Exception], Optional[Awaitable[None]]]

ParamRetryPolicy = Union[RetryPolicy, str]
ParamBeforeRetry = Union[BeforeRetry, str]

TargetFunction = Callable[..., Awaitable]
Exceptions = Tuple[Exception, ...]
ExceptionsOrException = Union[Exceptions, Exception]

T = TypeVar('T', RetryPolicy, BeforeRetry)


async def await_coro(coro):
    if inspect.isawaitable(coro):
        return await coro

    return coro


async def perform(
    fails: int,
    fn: TargetFunction,
    retry_policy: RetryPolicy,
    before_retry: Optional[BeforeRetry],
    *args,
    **kwargs
):
    while True:
        try:
            return await fn(*args, **kwargs)
        except Exception as e:
            fails += 1
            abandon, delay = retry_policy(fails, e)

            if abandon:
                raise e

            if before_retry is not None:
                try:
                    await await_coro(before_retry(fails, e))
                except Exception as e:
                    raise RuntimeError(
                        f'[aioretry] before_retry failed, reason: {e}'
                    )

            # `delay` could be 0
            if delay > 0:
                await asyncio.sleep(delay)


def get_method(
    target: Union[T, str],
    args: Tuple,
    name: str,
) -> T:
    if type(target) is not str:
        return target

    if len(args) == 0:
        raise RuntimeError(
            f'[aioretry] decorator should be used for instance method if {name} as a str `"{target}"` '
        )

    self = args[0]

    return getattr(self, target)  # type: ignore


def retry(
    retry_policy: ParamRetryPolicy,
    before_retry: Optional[ParamBeforeRetry] = None
) -> Callable[[TargetFunction], TargetFunction]:
    """Creates a decorator function

    Args:
        retry_policy (RetryPolicy, str): the retry policy
        before_retry (BeforeRetry, str, None): the function to be called after each failure of fn and before the corresponding retry.

    Returns:
        A wrapped function which accepts the same arguments as fn and returns an Awaitable

    Usage::
        @retry(retry_policy)
        async def coro_func():
            ...
    """

    def wrapper(fn: TargetFunction) -> TargetFunction:
        async def wrapped(*args, **kwargs):
            return await perform(
                0,
                fn,
                get_method(
                    retry_policy,
                    args,
                    'retry_policy'
                ),
                get_method(
                    before_retry,
                    args,
                    'before_retry'
                ) if before_retry is not None else None,
                *args,
                **kwargs
            )

        return wrapped

    return wrapper
