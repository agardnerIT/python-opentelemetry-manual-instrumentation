#
# Extension to app.py
# This version generates sub-spans during the add function
# to demonstrate how context is passed to child spans
#
# Usage
# python app.py --birth_day INT --birth_month INT
# eg. python app.py --birth_day 27 --birth_month 10
# Expected output: 27.10
#
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import argparse

resource = Resource(attributes={"service.name": "Adams-MacBook-Air", "os-version": 1234.56, "cluster": "A", "datacentre": "BNE"})

COLLECTOR_ENDPOINT = "127.0.0.1"
COLLECTOR_GRPC_PORT = 6004
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"http://{COLLECTOR_ENDPOINT}:{COLLECTOR_GRPC_PORT}", insecure=True))
provider.add_span_processor(processor)


parser = argparse.ArgumentParser("simple_example")
parser.add_argument("-bd", "--birth_day", help="What is your birth day? Eg. 15", type=int)
parser.add_argument("-bm", "--birth_month", help="What is your birth month? Eg. 3", type=int)
args = parser.parse_args()
BIRTH_DAY = args.birth_day
BIRTH_MONTH = args.birth_month

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

def set_attributes(*attrs):
    span = trace.get_current_span()
    combined = {}
    for attr in attrs:
        combined.update(attr)
    span.set_attributes(combined)

@tracer.start_as_current_span("add")
def add(first, second):
    set_attributes({"first": first},{ "second": second }, {"result": first + second })

    count = 1
    while count <= second:
        with tracer.start_as_current_span(f"add-loop-{count}") as span:
            if count == 6:
                span.set_attributes({"special-number": "yes!", "loop-number": count})
            print(f"A Message at count: {count}")
            count += 1

    return first + second

@tracer.start_as_current_span("subtract")
def subtract(first, second):
    set_attributes({"first": first},{ "second": second }, {"result": first - second })
    return first - second

@tracer.start_as_current_span("divide")
def divide(first, second):
    set_attributes({"first": first},{ "second": second }, {"result": first / second })
    return first / second

@tracer.start_as_current_span("multiply")
def multiply(first, second):
    set_attributes({"first": first},{ "second": second }, {"result": first * second })
    return first * second

if __name__ == "__main__":
    with tracer.start_as_current_span("do-calculations"):
        result = 7
        result = multiply(result, BIRTH_DAY)
        result = subtract(result,1)
        result = multiply(result,13)
        result = add(result,BIRTH_MONTH)
        result = add(result,3)
        result = multiply(result,11)
        result = subtract(result, BIRTH_DAY)
        result = subtract(result, BIRTH_MONTH)
        result = divide(result, 10)
        result = add(result, 11)
        result = divide(result, 100)
        trace.get_current_span().set_attribute("result", "{:.2f}".format(result))
        print("{:.2f}".format(result)) # 14.11
