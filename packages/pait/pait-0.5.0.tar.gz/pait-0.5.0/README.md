# pait
Pait is an api tool that can be used in any python web framework (currently only `flask`, `starlette` are supported, other frameworks will be supported once Pait is stable).

The core functionality of Pait is to allow you to have FastAPI-like type checking and type conversion functionality (dependent on Pydantic and inspect) in any Python web framework, as well as documentation output

Pait's vision of documentation output is both code and documentation, with a simple configuration, you can get an md document or openapi (json, yaml)

[中文文档](https://github.com/so1n/pait/blob/master/README_ZH.md)
# Installation
```Bash
pip install pait
```
# Usage
Note: The following code does not specify, all default to use the `starlette` framework. 
## 1.type checking and parameter type conversion
### 1.1Use in route handle
A simple starlette route handler example:
```Python
import uvicorn

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse


async def demo_post(request: Request):
    body_dict: dict = await request.json()
    uid: int = body_dict.get('uid')
    user_name: str = body_dict.get('user_name')
    # The following code is only for demonstration, in general, we do some wrapping 
    if not uid:
        raise ValueError('xxx')
    if type(uid) != int:
        raise TypeError('xxxx')
    if 10 <= uid <= 1000:
        raise ValueError('xxx')

    if not user_name:
        raise ValueError('xxx')
    if type(user_name) != str:
        raise TypeError('xxxx')
    if 2 <= len(user_name) <= 4:
        raise ValueError('xxx')
    
    return JSONResponse(
        {
            'result': {
                'uid': body_dict['uid'],
                'user_name': body_dict['user_name']
            } 
        }
    )


app = Starlette(
    routes=[
        Route('/api', demo_post, methods=['POST']),
    ]
)


uvicorn.run(app)
```
use pait in starletter route handler:

```Python
import uvicorn

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse

from pait.field import Body
from pait.app.starlette import pait
from pydantic import (
    BaseModel,
    conint,
    constr,
)


# Create a Model based on Pydantic.BaseModel 
class PydanticModel(BaseModel):
    uid: conint(gt=10, lt=1000)  # Whether the auto-check type is int, and whether it is greater than or equal to 10 and less than or equal to 1000 
    user_name: constr(min_length=2, max_length=4)  # Whether the auto-check type is str, and whether the length is greater than or equal to 2, less than or equal to 4



# Decorating functions with the pait decorator
@pait()
async def demo_post(
    # pait through the Body () to know the current need to get the value of the body from the request, and assign the value to the model, 
    # and the structure of the model is the above PydanticModel, he will be based on our definition of the field automatically get the value and conversion and judgment
    model: PydanticModel = Body()
):
    # Get the corresponding value to return
    return JSONResponse({'result': model.dict()})


app = Starlette(
    routes=[
        Route('/api', demo_post, methods=['POST']),
    ]
)

uvicorn.run(app)
```
As you can see, you just need to add a `pait` decorator to the routing function and change the parameters of `demo_post` to `model: PydanticModel = Body()`.
pait through `Body` to know the need to get the post request body data, and according to `conint(gt=10, lt=1000)` on the data conversion and restrictions, and assigned to `PydanticModel`, the user only need to use `Pydantic` as the call `model` can get the data.

Here is just a simple demo, because we write the model can be reused, so you can save a lot of development time, the above parameters are only used to a way to write, the following will introduce pait support for the two ways to write and use.

### 1.2Parameter expression supported by pait
pait in order to facilitate the use of users, support a variety of writing methods (mainly the difference between TypeHints)
- TypeHints  is PaitBaseModel:
    PaitBaseModel can be used only for args parameters, it is the most flexible, PaitBaseModel has most of the features of Pydantic. BaseModel, which is not possible with Pydantic.:
    ```Python
    from pait.app.starlette import pait
    from pait.field import Body, Header
    from pait.model import PaitBaseModel


    class TestModel(PaitBaseModel):
        uid: int = Body()
        content_type: str = Header(default='Content-Type')


    @pait()
    async def test(model: PaitBaseModel):
        return {'result': model.dict()}
    ```
- TypeHints is Pydantic.BaseModel: 
    BaseModel can only be used with kwargs parameters, and the type hints of the parameters must be a class that inherits from `pydantic.BaseModel`, using the example:
    ````Python
    from pydantic import BaseModel
    from pait.app.starlette import pait
    from pait.field import Body
    
    
    class TestModel(BaseModel):
        uid: int
        user_name: str
    
    
    @pait()
    async def test(model: BaseModel = Body()):
        return {'result': model.dict()}
    ````
- When TypeHints is not one of the above two cases:
    can only be used for kwargs parameters and type hints are not the above two cases, if the value is rarely reused, or if you do not want to create a Model, you can consider this approach
    ```Python
    from pait.app.starlette import pait
    from pait.field import Body


    @pait()
    async def test(uid: int = Body(), user_name: str = Body()):
        return {'result': {'uid': uid, 'user_name': user_name}}
    ```
### 1.3Field
Field will help pait know how to get data from request.
Before introducing the function of Field, let’s take a look at the following example. `pait` will obtain the body data of the request according to Field.Body, and obtain the value with the parameter named key. Finally, the parameter is verified and assigned to the uid.
```Python
from pait.app.starlette import pait
from pait.field import Body


@pait()
async def demo_post(
        # get uid from request body data
        uid: int = Body()
):
    pass
```
The following example will use a parameter called default.
Since you can't use Content-Type to name the variables in Python, you can only use content_type to name them according to the naming convention of python, so there is no way to get the value directly from the header, so you can set the value of `default` to Content-Type, and then Pait can get the value of Content-Type in the Header and assign it to the content_type variable.

```Python
from pait.app.starlette import pait
from pait.field import Body, Header


@pait()
async def demo_post(
        # get uid from request body data
        uid: int = Body(),
        # get Content-Type from header
        content_type: str = Header(default='Content-Type')
):
    pass
```
The above only demonstrates the Body and Header of the field, but there are other fields as well::
- Field.Body   Get the json data of the current request
- Field.Cookie Get the cookie data of the current request
- Field.File   Get the file data of the current request, depending on the web framework will return different file object types
- Field.Form   Get the form data of the current request
- Field.Header Get the header data of the current request
- Field.Path   Get the path data of the current request (e.g. /api/{version}/test, you can get the version data)
- Field.Query  Get the url parameters of the current request and the corresponding data

All the fields above are inherited from `pydantic.fields.FieldInfo`, most of the parameters here are for api documentation, see for specific usage[pydantic doc](https://pydantic-docs.helpmanual.io/usage/schema/#field-customisation)


In addition there is a field named Depends, he inherits from `object`, he provides the function of dependency injection, he only supports one parameter and the type of function, and the function's parameters are written in the same way as the routing function, the following is an example of the use of Depends, through Depends, you can reuse in each function to get the token function:

```Python
from pait.app.starlette import pait
from pait.field import Body, Depends


def demo_depend(uid: str = Body(), password: str = Body()) -> str:
    # fake db
    token: str = db.get_token(uid, password)
    return token


@pait()
async def test_depend(token: str = Depends(demo_depend)):
    return {'token': token}
```

## 2.requests object
After using `Pait`, the proportion of the number of times the requests object is used will decrease, so `pait` does not return the requests object. If you need the requests object, you can fill in the parameters like `requests: Requests` (you need to use the TypeHints format) , You can get the requests object corresponding to the web framework
```Python
from starlette.requests import Request


@params_verify()
async def demo_post(
    request: Requests,
    # get uid from request body data
    uid: int = Body()  
):
    pass
```

## 3.Exception
### 3.1Exception Handling
Pait will leave the exception to the user to handle it. Under normal circumstances, pait will only throw the exception of `pydantic` and `PaitBaseException`. The user needs to catch the exception and handle it by himself, for example:
```Python
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from pait.exceptions import PaitBaseException
from pydantic import ValidationError

async def api_exception(request: Request, exc: Exception) -> Response:
    """
    Handle exception code    
    """

APP = Starlette()
APP.add_exception_handler(PaitBaseException, api_exception)
APP.add_exception_handler(ValidationError, api_exception)
```
### 3.2Error Tip
When you use pait incorrectly, pait will indicate in the exception the file path and line number of the function.
```Bash
  File "/home/so1n/github/pait/pait/func_param_handle.py", line 101, in set_value_to_kwargs_param
    f'File "{inspect.getfile(func_sig.func)}",'
PaitBaseException: 'File "/home/so1n/github/pait/example/starlette_example.py", line 28, in demo_post\n kwargs param:content_type: <class \'str\'> = Header(key=None, default=None) not found value, try use Header(key={key name})'
```
If you need more information, can set the log level to debug to get more detailed information
```Python
DEBUG:root:
async def demo_post(
    ...
    content_type: <class 'str'> = Header(key=None, default=None) <-- error
    ...
):
    pass
```
## 4.Document Generation
In addition to parameter verification and conversion, pait also provides the ability to output api documentation, which can be configured with simple parameters to output perfect documentation.
Note: Currently only md, json, yaml type documents and openapi documents for json and yaml are supported for output. 

Currently pait supports most of the functions of openapi, a few unrealized features will be gradually improved through iterations (response-related more complex)

The openapi module of pait supports the following parameters (more parameters will be provided in the next version):
- title: openapi's title 
- open_api_info: openapi's info param  
- open_api_tag_list: related description of openapi tag 
- open_api_server_list: openapi server list
- type_: The type of output, optionally json and yaml 
- filename: Output file name, or if empty, output to terminal

The following is the sample code output from the openapi documentation (modified by the 1.1 code). See [Example code](https://github.com/so1n/pait/tree/master/example/api_doc) and [doc example](https://github.com/so1n/pait/blob/master/example/api_doc/example_doc)
```Python
import uvicorn

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse

from pait.field import Body
from pait.app.starlette import pait
from pydantic import (
    BaseModel,
    conint,
    constr,
)


# Create a Model based on Pydantic.BaseModel 
class PydanticModel(BaseModel):
    uid: conint(gt=10, lt=1000)  # Whether the auto-check type is int, and whether it is greater than or equal to 10 and less than or equal to 1000 
    user_name: constr(min_length=2, max_length=4)  # Whether the auto-check type is str, and whether the length is greater than or equal to 2, less than or equal to 4



# Decorating functions with the pait decorator
@pait()
async def demo_post(
    # pait through the Body () to know the current need to get the value of the body from the request, and assign the value to the model, 
    # and the structure of the model is the above PydanticModel, he will be based on our definition of the field automatically get the value and conversion and judgment
    model: PydanticModel = Body()
):
    # Get the corresponding value to return
    return JSONResponse({'result': model.dict()})


app = Starlette(
    routes=[
        Route('/api', demo_post, methods=['POST']),
    ]
)

uvicorn.run(app)
# --------------------

from pait.app import load_app
from pait.api_doc.open_api import PaitOpenApi


# Extracting routing information to pait's data module
load_app(app)
# Generate openapi for routing based on data from the data module
PaitOpenApi()
```
## 5.How to used in other web framework?
If the web framework is not supported, which you are using.
Can be modified sync web framework according to [pait.app.flask](https://github.com/so1n/pait/blob/master/pait/app/flask.py)

Can be modified async web framework according to [pait.app.starlette](https://github.com/so1n/pait/blob/master/pait/app/starlette.py)
## 6.IDE Support
While pydantic will work well with any IDE out of the box.
- [PyCharm plugin](https://pydantic-docs.helpmanual.io/pycharm_plugin/)
- [Mypy plugin](https://pydantic-docs.helpmanual.io/mypy_plugin/)

## 7.Full example
For more complete examples, please refer to[example](https://github.com/so1n/pait/tree/master/example)