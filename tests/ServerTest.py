import sys, os, asyncio, threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.ae.AsyncResponseListener import AsyncResponseListenerFactory
async_response_listener = AsyncResponseListenerFactory().get_instance()
async_response_listener_2 = AsyncResponseListenerFactory().get_instance()

def cb1(req):
    print(id(threading.current_thread()))
    return 'number #1\n'

def cb2(req):
    print(id(threading.current_thread()))
    return 'number #2\n'

def main():
    print(id(threading.current_thread()))

    async_response_listener.set_rqi_cb(123, cb1)

    async_response_listener.start()

    async_response_listener_2.set_rqi_cb(456, cb2)

main()