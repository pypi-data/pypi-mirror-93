"""Python backend logic for yangsuite-grpc-telemetry.

Nothing in this file should use any Django APIs.
"""

from concurrent import futures
from collections import deque
import grpc

from .generated import (
    add_gRPCMdtDialoutServicer_to_server,
    gRPCMdtDialoutServicer,
    Telemetry,
)

from yangsuite import get_logger

log = get_logger(__name__)


class YSGrpcMdtDialoutServicer(gRPCMdtDialoutServicer):
    """Concrete subclass of :class:`gRPCMdtDialoutServicer` stub."""

    def __init__(self, output_format="compact"):
        """Create an instance designed to handle inbound telemetry messages.

        Args:
          output_format (str): One of:

            - 'raw' (string representation provided by grpcio)
            - 'compact' (custom string representation, less verbose)
        """
        super(YSGrpcMdtDialoutServicer, self).__init__()
        self.output_format = output_format
        self.stdout_queue = deque()

    def walk_fields(self, fields, pfx=""):
        lines = []

        is_keys = False
        if pfx == '/content':
            pfx = ''
            lines.append('')
        elif pfx == '/keys':
            pfx = ''
            is_keys = True
            lines.append('')

        for field in fields:
            if field.fields:
                lines += self.walk_fields(field.fields, pfx + '/' + field.name)
            else:
                value = None
                if field.HasField('bytes_value'):
                    value = field.bytes_value
                elif field.HasField('string_value'):
                    value = field.string_value
                if field.HasField('bool_value'):
                    value = field.bool_value
                elif field.HasField('sint32_value'):
                    value = field.sint32_value
                elif field.HasField('sint64_value'):
                    value = field.sint64_value
                elif field.HasField('uint32_value'):
                    value = field.uint32_value
                elif field.HasField('uint64_value'):
                    value = field.uint64_value
                elif field.HasField('double_value'):
                    value = field.double_value
                elif field.HasField('float_value'):
                    value = field.float_value

                if value is None:
                    continue

                if is_keys:
                    lines.append("{0:17} : {1:20} : {2}".format(
                        'Key', pfx + '/' + field.name, value))
                else:
                    lines.append("{0:80} : {1}".format(
                        pfx + '/' + field.name, value))

        return lines

    def MdtDialout(self, request_iterator, context):
        """Handle an inbound telemetry message from the device."""
        for request in request_iterator:
            t = Telemetry()
            t.ParseFromString(request.data)
            if self.output_format == 'raw':
                self.stdout_queue.append(str(t))
            elif self.output_format == 'compact':
                msg = [
                    "{0:40} : {1}".format("Node", t.node_id_str),
                    "{0:40} : {1}".format("Subscription",
                                          t.subscription_id_str),
                    "{0:40} : {1}".format("Path", t.encoding_path),
                    # TODO? collection_id, collection_start_time, msg_timestamp
                ]
                for gpb in t.data_gpbkv:
                    msg += self.walk_fields(gpb.fields)
                self.stdout_queue.append("\n".join(msg))

            yield request


class YSGrpcTelemetryServer(object):
    """Class providing feature logic for yangsuite-grpc-telemetry.

    .. seealso:: https://github.com/grpc/grpc/blob/v1.13.x/examples/python/route_guide/route_guide_server.py
    """   # noqa: E501

    _ONE_DAY_IN_SECONDS = 60 * 60 * 24

    servers = {}

    @classmethod
    def serve(cls, address="192.113.193.1", port="5678"):
        """Run the server indefinitely."""
        if port in cls.servers:
            log.warning("Tried to start server on port %s, already running!",
                        port)
            return False, 'Server already running on port {0}'.format(port)
        # Create gRPC server instance
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # Tell it to listen at the given address and port number
        server_port = server.add_insecure_port("{0}:{1}".format(address, port))
        if server_port == 0:
            return False, 'Unable to start server on {0} port {1}'.format(
                address, port)
        # Tell it to pass inbound MDT RPCs to an instance of
        # YSGrpcMdtDialoutServicer for servicing
        servicer = YSGrpcMdtDialoutServicer()
        add_gRPCMdtDialoutServicer_to_server(servicer, server)
        # Start it - all above setup MUST be applied before calling start()!
        server.start()
        cls.servers[str(port)] = (server, servicer)
        log.warning("Server started on %s port %s", address, port)
        return True, 'Server started on {0} port {1}'.format(address, port)

    @classmethod
    def get(cls, port):
        return cls.servers.get(str(port), None)

    @classmethod
    def stop(cls, port):
        server = cls.get(port)
        if server:
            server[0].stop(0)
            del cls.servers[port]
            log.warning("Server stopped on port %s", port)
            return True, 'Server stopped on port {0}'.format(port)
        else:
            log.warning("Tried to stop server on port %s, not running!",
                        port)
            return (
                False,
                'Retry stop for server running on port {0}'.format(port)
            )
