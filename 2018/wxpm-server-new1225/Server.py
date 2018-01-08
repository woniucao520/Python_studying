import asyncio
import logging
import logging.config
import os
import signal
import yaml

import aioredis
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError

from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.tcpserver import TCPServer

from Commands.Command import Command

from Configuration import ConfigParser

class ClientConnection(object):

    def __init__(self, stream, redis_client):
        self._stream = stream
        self._redis = redis_client
        self.EOF = b'\n'

    @gen.coroutine
    def run(self):
        """
        Main connection loop, launches listen on given channel and keeps reading data
        from socket until it is closed
        """
        try:
            while True:
                try:
                    request = yield self._stream.read_until(self.EOF)
                    request_body = request.rstrip(self.EOF)
                except StreamClosedError:
                    self._stream.close(exc_info=True)
                    return
                else:
                    response_body = Command.process(request_body, self._redis)
                    response = response_body + self.EOF
                    try:
                        yield self._stream.write(response)
                    except StreamClosedError:
                        self._stream.close(exc_info=True)
        except Exception as e:
            if not isinstance(e, gen.Return):
                print("Unexcepted error occured in connetion loop:{}".format(e))
            else:
                print("Closing connection loop because socket was closed.")


    @gen.coroutine
    def update(self, message):
        """
        Handle updates and send data if necessary
        :param message: variable that represents the update message
        :return:
        """
        cmd, args = message.split(':', 1)
        response_body = Command.process_updates(cmd, args)
        response = response_body + self.EOF

        try:
            yield self._stream.write(response)
        except StreamClosedError:
            self._stream.close(exc_info=True)
            return


class Server(TCPServer):
    """
    This is a TCP Server that listens to clients and handles their requests
    made using socket and also listen to specified Redis 'channel' and handles updates
    on that channel
    """

    def __init__(self):
        super(Server, self).__init__()
        self._redis = None
        self._redis_pub = None
        self._channel = None
        self._connections = []

        logging.config.dictConfig(yaml.load(open(os.path.realpath('log.yaml'), 'r')))
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.WARN)


    @asyncio.coroutine
    def subscribe(self, channel_name):
        """
        Create async redis client and subscribe to the given PUB/SUB channel.
        Listen to the message and launch publish handler
        :param channel_name: string respresenting Redis PUB/SUB channel name
        :return:
        """
        try:
            self._redis = yield aioredis.create_redis((ConfigParser.get('wx.redis.config','host'),ConfigParser.get('wx.redis.config','port')))
            self._redis_pub = yield aioredis.create_redis((ConfigParser.get('wx.redis.config','host'),ConfigParser.get('wx.redis.config','port')))
        except aioredis.MultiExecError:
            print('Failed to conect to Redis Server at {}:{}'.format(ConfigParser.get('wx.redis.config','host'),ConfigParser.get('wx.redis.config','port')))
        else:
            channels = yield self._redis.subscribe(channel_name)
            print('Subscribed to "{}" Redis channel'.format(channel_name))
            self._channel = channels[0]

            yield self.listen_redis()

    @gen.coroutine
    def listen_redis(self):
        """
        Listen to the message from the subscribed Redis channel and launch publish handler
        :return:
        """
        while True:
            yield self._channel.wait_message()
            try:
                msg = yield self._channel.get(encoding='utf-8')
            except aioredis.ChannelClosedError:
                print("Redis channel was closed. Stopping listening")
                return

            if msg:
                body_utf8 = msg.encode('utf-8')
                yield [con.update(msg) for con in self._connections]

            print("Message in {}: {}".format(self._channel.name,msg))

    @gen.coroutine
    def handle_stream(self, stream, address):
        print('New request has come from our {} buddy...'.format(address))
        connection = ClientConnection(stream, self._redis_pub)
        self._connections.append(connection)
        yield connection.run()
        self._connections.remove(connection)

    @gen.coroutine
    def shutdown(self):
        super(Server, self).stop()
        yield self._redis.unsubscribe(self._channel)
        yield self._redis.quit()
        self.io_loop.stop()


if __name__ == '__main__':
    def sig_handler(sig, frame):
        print('Caught signal:{}'.format(sig))
        IOLoop.current().add_callback_from_signal(server.shutdown)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    AsyncIOMainLoop().install()
    server = Server()
    server.listen(ConfigParser.get('wx.server.config','port'))
    IOLoop.current().spawn_callback(server.subscribe, ConfigParser.get('wx.redis.config','channels')['broadcast'])

    print('Starting the server...')
    asyncio.get_event_loop().run_forever()
    print('Server has shutdown.')