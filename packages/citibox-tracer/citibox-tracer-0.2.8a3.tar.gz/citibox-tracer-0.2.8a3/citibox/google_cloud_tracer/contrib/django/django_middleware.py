import json
import logging

import django
import six
from django.db import connection

from opencensus.ext.django.middleware import (
    OpencensusMiddleware,
    _trace_db_call,
    EXCLUDELIST_PATHS,
    EXCLUDELIST_HOSTNAMES,
    execution_context,
    HTTP_HOST, HTTP_METHOD, HTTP_PATH, HTTP_ROUTE, HTTP_URL, SPAN_THREAD_LOCAL_KEY, REQUEST_THREAD_LOCAL_KEY,
    _get_current_tracer,
)
from opencensus.trace import tracer as tracer_module
from opencensus.trace import span as span_module
from opencensus.trace import utils
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
from opencensus.trace.propagation.google_cloud_format import GoogleCloudFormatPropagator
from opencensus.common import configuration
from opencensus.trace import samplers

from citibox.google_cloud_tracer import SpanContextFactory
from citibox.google_cloud_tracer.tracer import disable_tracer_environment

logger = logging.getLogger(__name__)

DJANGO_VIEW = 'django.view'


class GoogleCloudDjangoMiddleware(OpencensusMiddleware):

    def __init__(self, get_response=None):
        self.get_response = get_response
        settings = getattr(django.conf.settings, 'TRACING', {})

        self.sampler = (settings.get('SAMPLER', None)
                        or samplers.AlwaysOffSampler())
        if isinstance(self.sampler, six.string_types):
            self.sampler = configuration.load(self.sampler)

        self.exporter = settings.get('EXPORTER', None) or \
            stackdriver_exporter.StackdriverExporter(project_id=settings.get('PROJECT_ID', None))
        if isinstance(self.exporter, six.string_types):
            self.exporter = configuration.load(self.exporter)

        self.propagator = settings.get('PROPAGATOR', None) or \
            GoogleCloudFormatPropagator()
        if isinstance(self.propagator, six.string_types):
            self.propagator = configuration.load(self.propagator)

        self.excludelist_paths = settings.get(EXCLUDELIST_PATHS, None)

        self.excludelist_hostnames = settings.get(EXCLUDELIST_HOSTNAMES, None)

        if django.VERSION >= (2,):  # pragma: NO COVER
            connection.execute_wrappers.append(_trace_db_call)

        self._span_context_factory = SpanContextFactory(self.propagator)

    def _get_request_body(self, request) -> dict:
        body = {}
        body_unicode = request.body.decode('utf-8')
        if body_unicode:
            body = json.loads(body_unicode)
        return body

    def process_request(self, request):
        """Called on each request, before Django decides which view to execute.

        :type request: :class:`~django.http.request.HttpRequest`
        :param request: Django http request.
        """
        if disable_tracer_environment() or utils.disable_tracing_url(request.path, self.excludelist_paths):
            return

        execution_context.set_opencensus_attr(
            REQUEST_THREAD_LOCAL_KEY,
            request)

        execution_context.set_opencensus_attr(
            'excludelist_hostnames',
            self.excludelist_hostnames)

        try:

            span_context_builder = self._span_context_factory.get_span_context_builder(
                request.META.get('HTTP_USER_AGENT', 'default')
            )
            span_context = span_context_builder.build_span_context(
                headers=request.META,
                body=self._get_request_body(request)
            )
            tracer = tracer_module.Tracer(
                span_context=span_context,
                sampler=self.sampler,
                exporter=self.exporter,
                propagator=self.propagator
            )

            span = tracer.start_span()
            span.span_kind = span_module.SpanKind.SERVER
            span.name = f'[{span_context_builder.SPAN_PREFIX} - {request.method}] {request.path}'

            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_HOST,
                attribute_value=request.get_host())
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_METHOD,
                attribute_value=request.method)
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_PATH,
                attribute_value=str(request.path))
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_ROUTE,
                attribute_value=str(request.path))
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_URL,
                attribute_value=str(request.build_absolute_uri()))

            execution_context.set_opencensus_attr(
                SPAN_THREAD_LOCAL_KEY,
                span)

        except Exception:  # pragma: NO COVER
            logger.error('Failed to trace request', exc_info=True)
            pass

    def process_view(self, request, view_func, *args, **kwargs):
        """Process view is executed before the view function, here we get the
        function name add set it as the span name.
        """

        # Do not trace if the url is excludelisted
        if utils.disable_tracing_url(request.path, self.excludelist_paths):
            return

        try:
            # Get the current span and set the span name to the current
            # function name of the request.
            tracer = _get_current_tracer()
            tracer.add_attribute_to_current_span(
                attribute_key=DJANGO_VIEW,
                attribute_value=request.method)
        except Exception:  # pragma: NO COVER
            logger.error('Failed to trace request', exc_info=True)

    def process_response(self, request, response):
        if disable_tracer_environment():
            return response

        return super().process_response(request, response)
