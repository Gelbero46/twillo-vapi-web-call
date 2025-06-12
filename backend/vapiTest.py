from vapi import Vapi
import os
vapi = Vapi(token="c616c8e0-6934-4a0a-b225-3231c40c1274")

# Create an outbound call
call = vapi.calls.create(
    phone_number_id="a0c30b9c-7f90-44b7-89f5-f1f0efa050c9",
    customer={"number": "+2347026735445"},
    assistant_id="d8196039-cdb2-47f1-ae77-7f41d819712b"
)

print(f"Call created: {call.id}")
