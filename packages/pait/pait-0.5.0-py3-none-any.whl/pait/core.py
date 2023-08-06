import inspect
from functools import wraps
from typing import Callable, List, Optional, Tuple, Type, Union

from pait.app.base import BaseAppHelper, BaseAsyncAppHelper
from pait.g import pait_data
from pait.model import FuncSig, PaitCoreModel, PaitResponseModel, PaitStatus
from pait.param_handle import async_class_param_handle, async_func_param_handle, class_param_handle, func_param_handle
from pait.util import get_func_sig


def pait(
    app_helper_class: "Type[Union[BaseAppHelper, BaseAsyncAppHelper]]",
    author: Optional[Tuple[str]] = None,
    desc: Optional[str] = None,
    status: Optional[PaitStatus] = None,
    group: Optional[str] = None,
    tag: Optional[Tuple[str, ...]] = None,
    response_model_list: List[Type[PaitResponseModel]] = None,
):
    def wrapper(func: Callable):
        func_sig: FuncSig = get_func_sig(func)
        qualname = func.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0]

        pait_id: str = f"{qualname}_{id(func)}"
        func._pait_id = pait_id
        pait_data.register(
            PaitCoreModel(
                author=author,
                desc=desc,
                func=func,
                pait_id=pait_id,
                status=status,
                group=group,
                tag=tag,
                response_model_list=response_model_list,
            )
        )

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def dispatch(*args, **kwargs):
                # only use in runtime, support cbv
                class_ = getattr(inspect.getmodule(func), qualname)
                # real param handle
                app_helper: BaseAsyncAppHelper = app_helper_class(class_, args, kwargs)
                # auto gen param from request
                func_args, func_kwargs = await async_func_param_handle(app_helper, func_sig)
                # support sbv
                await async_class_param_handle(app_helper)
                return await func(*func_args, **func_kwargs)

            return dispatch
        else:

            @wraps(func)
            def dispatch(*args, **kwargs):
                # only use in runtime
                class_ = getattr(inspect.getmodule(func), qualname)
                # real param handle
                app_helper: BaseAppHelper = app_helper_class(class_, args, kwargs)
                # auto gen param from request
                func_args, func_kwargs = func_param_handle(app_helper, func_sig)
                # support sbv
                class_param_handle(app_helper)
                return func(*func_args, **func_kwargs)

            return dispatch

    return wrapper
