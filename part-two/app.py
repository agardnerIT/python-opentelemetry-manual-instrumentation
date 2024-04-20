# Code snippets for this video: https://youtu.be/jEbArKXtd0Y
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import Resource
import time

resource = Resource(attributes={"service.name": "Adams-MacBook-Air", "os-version": 1234.56, "cluster": "A", "datacentre": "BNE"})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

@tracer.start_as_current_span("add")
def add(first, second):
    current_span = trace.get_current_span()
    current_span.set_status(trace.StatusCode.OK)

    current_span.set_attributes(attributes={
      "first-value": first,
      "second-value": second
    })

    time.sleep(1)
    current_span.add_event(name="myEvent", attributes={"foo4": 222, "addition_process": "complete"}, timestamp=time.time_ns())

    return first + second

if __name__ == "__main__":
    result = add(11, 3)
    print(f"The result is: {result}")
