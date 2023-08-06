Tornado web services @ your fingertips
===============================================================================

**dizzydecor** is a python library that makes it easy to create web services 
in tornado. To accomplish this, the library adds two new classes and decorators 
that help eliminate the need for boilerplate code. 

New in version 0.0.4
----------------------------------------------------------------------------
* Support for handler initialization with keyword arguments to the ``webservice`` decorator
* Added support for path arguments (anything included in the url after the method name is added to a path_args list that will be passed to the called method)
* Custom service paths (use the path keyword argument in the ``webservice`` decorator)
* Custom method names (use the name keyword argument in the ``servicemethod`` decorator)
* Bypass body parsing on a per-method basis with the ignore_body keyword argument on the ``servicemethod`` decorator

Example
----------------------------------------------------------------------------

Here is an example to show how **dizzydecor**, works:

.. code:: python

    from tornado.ioloop import IOLoop

    from dizzydecor import (
        WSApplication,
        WebserviceHandler,
        webservice,
        servicemethod
    )
    
    # The webservice decorator accepts keyword argument that will be used in
    # the handler's initialize method
    @webservice(greeting="This is my custom greeting")
    class MyWebService(WebserviceHandler):

        def initialize(self, greeting):
            self.greeting = greeting
        
        @servicemethod()
        async def echo(self, message):
            return f"You said: {message}"
            
        @servicemethod(httpmethod="GET")
        async def my_greeting(self):
            return dict(greeting="Hello, welcome to my web service demo!")

        # Use the name argument to setup custom method names
        # anything included in the url after the method name is sent to the
        # method in an array named path_args
        @servicemethod(ignore_body=True, name="greet")
        async def my_other_greeting(self, path_args):
            # with ignore_body set to True, you can parse the body yourself
            body = self.request.body.decode("utf-8")
            return dict(greeting=self.greeting, body=body, path_args=path_args) 

    # The path argument allows you to configure a custom path for this webservice
    @webservice(path=r"/custom-name/(.+)")
    class TotallyNonsensicalName(WebserviceHandler):

        @servicemethod()
        async def echo(self, message):
            return dict(message=message)
            
    if __name__ == "__main__":
        app = WSApplication()
        app.listen(8080)
        IOLoop.current().start()
    
This will create two web services. The first has three methods: echo, my_greeting, and my_other_greeting.
By default, service methods respond to POST requests; however, the ``httpmethod``
argument to ``servicemethod`` can change this behaviour. For instance, 
my_greeting is setup to respond to GET requests.

Paths are generated based on class and method names. 
    * A web service's path is the lower-case class name with each word joined by a hyphen. (MyWebService -> my-web-service)
    * A method's path is the method's name with underscores replaced with hyphens. (my_greeting -> my-greeting)

Paths can also be configured manually.
    * The ``path`` argument can be used with the ``webservice`` decorator to configure the web service's base path
    * Method names can be configured with the ``servicemethod`` decorator's ``name`` argument 

If a service method does not get all of its arguments, the service handler sends a 400 HTTP status code automatically.

To test, you can use curl::

    $ curl http://localhost:8080/my-web-service/echo -d '{"message": "This is my message"}'
    "You said: This is my message"
    
    $ curl http://localhost:8080/my-web-service/my-greeting
    {"greeting": "Hello, welcome to my web service demo!"}
    
    $ curl -d '{"a": 1}' http://localhost:8080/my-web-service/greet/t
    {"greeting": "This is my custom greeting", "body": "{\"a\": 1}", "path_args": ["t"]}
    
    $ curl -d '{"message": "test"}' http://localhost:8080/custom-name/echo
    {"message": "test"}

    $ curl -d '{"messag": "test"}' http://localhost:8080/custom-name/echo
    "<html><title>400: Bad Request</title><body>400: Bad Request</body></html>"
    
You may have noticed that the example uses JSON.

What if I do not want to use JSON?
----------------------------------------------------------------------------

In this case, all you need to do is override the ``load`` and ``dump``
methods in a subclass of ``WebserviceHandler`` or ``SyncWebserviceHandler``

Here is an example with `PyYAML <http://pyyaml.org/wiki/PyYAML>`_:

.. code:: python

    # -- snip --

    import yaml

    class YAMLServiceHandler(WebserviceHandler):
        
        def load(self, request):
            return yaml.safe_load(request)
            
        def dump(self, response):
            # You can also set content-type here with self.set_header
            return yaml.safe_dump(response)
    
    @webservice()
    class YetAnotherService(YAMLServiceHandler):
        
        @servicemethod()
        async def join(self, arr, delim):
            return dict(message=delim.join(map(str, arr)))

    # -- snip --
            
The rest is exactly the same, except now your service will use YAML.

Here's how to test it with curl::
    
    $ curl http://localhost:8080/yet-another-service/join --data-binary @"/dev/stdin"<<_eof_
    arr:
        - Hello
        - world
    delim: " "
    _eof_
    message: Hello world

Installation
----------------------------------------------------------------------------

Install with pip or easy_install::

    $ pip install dizzydecor

**dizzydecor** is only available for Python 3

What about non-standard HTTP methods? (Experimental)
----------------------------------------------------------------------------

In this case, all you need to do is extend the SUPPORTED_METHODS property 
of the service handler class.

.. code:: python

    # -- snip --

    @webservice()
    class NotificationService(WebserviceHandler):
        SUPPORTED_METHODS = WebserviceHandler.SUPPORTED_METHODS + ("NOTIFY",)

        @servicemethod(httpmethod="NOTIFY")
        async def notification(self, message):
            # etc
    
    # -- snip --

The script for the new HTTP method is added to the service handler 
during the creation of the web service. After that, all you need to 
do is setup to service method to respond to that request type. Depending 
on the situation, you might also need to customize the way arguments are 
parsed by overriding prepare.

What if I want to use a custom tornado request handler?
----------------------------------------------------------------------------

If you want to add a handler that does not fit the web service mold, you can append it to the WSApplication's endpoints class variable.
For example, maybe you want to add a websocket:

.. code:: python

    ws_clients = []
    msg_buffer = []

    class EchoWebSocket(WebSocketHandler):

        def open(self):
            print("WebSocket opened")
            ws_clients.append(self)
            for msg in msg_buffer:
                self.write_message(msg)

        def on_message(self, message):
            global msg_buffer
            message = u"Someone said: " + message
            msg_buffer = msg_buffer[:19]
            msg_buffer.append(message)
            for client in ws_clients:
                client.write_message(message)

        def on_close(self):
            print("WebSocket closed")
            ws_clients.remove(self)

        def check_origin(self, origin):
            return True

    if __name__ == "__main__":
        WSApplication.endpoints.append((r"/websocket", EchoWebSocket))
        # The keyword arguments websocket_ping_interval and websocket_ping_timeout 
        # are passed to the underlying Application class
        app = WSApplication(websocket_ping_interval=3, websocket_ping_timeout=5)
        app.listen(8080)
        IOLoop.current().start()

Any web services you added with dizzydecor decorators will still work.

Synchronous services
----------------------------------------------------------------------------

The ``WebserviceHandler`` is asynchronous; however, you can make synchronous 
service handlers using the ``SyncWebserviceHandler`` class.

.. code:: python

    # -- snip --

    @webservice()
    class MySyncService(SyncWebserviceHandler):

        # This time the method is not async
        @servicemethod(httpmethod="GET")
        def my_greeting(self):
            return dict(greeting="Hello...")

    # -- snip --