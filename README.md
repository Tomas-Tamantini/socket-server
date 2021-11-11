# socket-server
A (hopefully) simple python socket server

## Author
Tomás Tamantini - Nov. 2021

## Usage
Just import the async method **run\_server** from the *socket\_server* module. You can pass as arguments:

- the address
- the port to serve
- an object which implements the [**Consumer** protocol](socket_server/consumer.py) (optional), to handle messages coming from the clients.
- an object which implements the [**Producer** protocol](socket_server/producer.py) (optional), that will produce messages to send to the clients.
- Alternatively, a single object which implements both protocols can be used.


Remember to run the code asynchronously:
```py
async def main():
    await run_server('localhost', 8080, consumer, producer)

if __name__ == '__main__':
    asyncio.run(main())
```

See a more detailed example [here](usage_example.py). 