API_VERSION = (
    "1."
    "10."
    "2"
)  # type: str
"""The semantic version of this API."""

PROTOBUF_VERSION = 2  # type: int
"""The version of Protobuf this API can read and write from.
Attempts to load old Protobuf versions will raise a ``ValueError``.
"""
