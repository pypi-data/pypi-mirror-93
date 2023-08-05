# Copyright 2016 Cisco Systems, Inc
import socket
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from yangsuite import get_logger
from .grpctelemetry import YSGrpcTelemetryServer

log = get_logger(__name__)


@login_required
def render_main_page(request):
    """Return the main grpctelemetry.html page."""
    return render(request, 'ysgrpctelemetry/grpctelemetry.html')


@login_required
def start_servicer(request, port):
    """Start servicer listening on the given port (and IP)."""
    try:
        address = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        address = request.POST.get('address')
    result, message = YSGrpcTelemetryServer.serve(address, port)
    return JsonResponse({'result': result, 'message': message})


@login_required
def stop_servicer(request, port):
    """Stop servicer listening on the given port."""
    result, message = YSGrpcTelemetryServer.stop(port)
    return JsonResponse({'result': result, 'message': message})


@login_required
def get_output(request, port):
    """Get the latest output from any given listener stream."""
    server = YSGrpcTelemetryServer.get(port)
    result = {'output': []}
    if server:
        while len(server[1].stdout_queue):
            result['output'].append(server[1].stdout_queue.popleft())

    return JsonResponse(result)
