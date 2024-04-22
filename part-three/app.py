from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import time
from opentelemetry.semconv.trace import SpanAttributes

resource = Resource(attributes={"service.name": "Adams-MacBook-Air", "os-version": 1234.56, "cluster": "A", "datacentre": "BNE"})
provider = TracerProvider(resource=resource)

COLLECTOR_ENDPOINT = "127.0.0.1"
COLLECTOR_GRPC_PORT = 6004

#processor = BatchSpanProcessor(ConsoleSpanExporter())
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"http://{COLLECTOR_ENDPOINT}:{COLLECTOR_GRPC_PORT}"))
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

@tracer.start_as_current_span("add")
def add(first, second):
    current_span = trace.get_current_span()

    # Assume a call to a feature flag backend
    feature_flag_key = "is_feature_enabled"
    flag_value = True

    if feature_flag_key == "is_feature_enabled" and flag_value:
        time.sleep(2)

    current_span.set_attributes({
        SpanAttributes.FEATURE_FLAG_PROVIDER_NAME: "MyFakeFeatureFlagBackend",
        SpanAttributes.FEATURE_FLAG_KEY: feature_flag_key,
        SpanAttributes.FEATURE_FLAG_VARIANT: flag_value
    })
    return first + second

if __name__ == "__main__":
    result = add(11, 3)
    print(f"The result is: {result}")
