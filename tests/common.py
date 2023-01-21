"""Provide common pytest fixtures."""
import os

TEST_PACKETS = [
    # Discovery packet 1
    """
    NWQ3NjcyYTI4YTAyMzA2M2ZiNjcyZjA3YmM3MDdkYzY0MjJiYTJmNWQ3MzBhZWVkNTA4ZjA1YTJjMj
    AyOTA5YTViMTI4MWNkNzM2NjA2NjUwZWU4NzA4ZmY0MDU2OTI0NWI3MTQ3N2UzMzYzYzgzMDA5MjQ0
    ZTU4MzZlMWYyOTg1NDI4ZTUxYTRjNTllODYyOGMyMjRjMWYxNjBmMWE5ZTk4YTZhZWQxYjc3ZTk1ZT
    BiNGIzYWVhYzhjYmJjZTdmMzZmMDdjMTc5NzgwYTVlOTAyZDJlNWY5Y2M4MDhhNWQxMmNlZjQ4NDJi
    OThlN2MwYjc5MjQxOTlhNmMyZmQyMGUxZjg4ZjVmYTE1MDJhYWMyMmY3YWMyYjkwMTBhYjE5MjIzMD
    ZmZjA0MGYxN2M3Y2I2NzBiNzA4OTIwNmEy
    """,
    # Discovery packet 2
    """
    NWQ3NjFhNGIyYTM3ZDFkOGZiNjcyZjA3YmM3MDdkYzY0MjJiYTJmNWQ3MzVhZWVkNTA4ZjA1YTJjMj
    AyOTA5YTViMTI4MWNjNzM2NjA2NjUwZWU4NzA4MmUxNDA2OTI2NTk3OTNmNWQxNjNhZjgxZjBmMTQ3
    NjBiNzNlNzgyZDQwM2E3OWNkNmJiZTI2OGFjYmQwYjdjMmUxNzAxNjhjNWMzZWE4ODg0ZWMyMmMwZj
    ZiNmI0YWVhZjljZGM5OTI1Mzg5MTIxNGQ4OTg2OTFkZjMyZTZlYmFkODhhZGQ2NGU2ZmQzOTI4NjNh
    OWJmMWEwZjJiMjc5Yjc5N2MyZmQyZGUxZmQ0ZmY3YTQzZDJlNjk4YWYyNTBkNDZhMTBhZmUwZGRjYm
    FmNTg0N2Y1ODc4M2I2NzA=
    """,
    # Stats packet
    """
    NWQ3NjFhNGIyYTM3ZDFkOGU3NzAwYjI2ODUzMTdlNWM0MjJiYTJmNWQ3MzhhZWVkNTA4ZjAyYThjMj
    AyOTA5YTFiMTM4MWQ1MjYyYjJkMzZkMDNjYzJiN2E0NDA2OTI0NDk0NGQzMmE3ZjRlOWIzNzM4MTQ2
    NTBhNzJlMWYyOWI1NDJlZmRiY2JiZTU2OGIzOGMyNTRjMDAyNzIxNmFiMGFhOTVlZmE1ZDgxMzkxMj
    RiZDgzOWY5YWJjOGU3ZGNlNmJhMjE5N2JiOWYzOTFkZjI5ZTJlNGY5YzQ4MDg1MDk1ZWUzYTdjMzFh
    YThkZjkwZjJiMjcwYjdkNmMyZmQzYWU0Zjg4OTVmMzE2ZTg3NmM4YWY2YWYyYWU4OWJhM2U2ZGRjZj
    c2MGZiOWYxNzg=
    """,
    # VLAN packet
    """
    NWQ3NjFhNGIyYTM3ZDFkOGU3NzAwYjI2ODUzMTdlYzY0MjJiYTJmNWQ3ZjFhZWVkNTA4Zjc2YjBjMj
    AyOTA5YTc5MTM4MWM3MjYwODJhMzY1ZWQ5NDFiN2E0NDA3NjI0NTk3MTRjNmUxYTI4ZmEwMjU0NjAy
    OTVlM2ZhMGJjOWI3NjJmZmRhZGJiZDc2OGIzOGMzNDRjMDAyNzIxNmRmMWU3Y2ZhMmUzZGUzMGYyYz
    A4N2EzNjA2NWJjOGU=
    """,
    # Ports packet
    """
    NWQ3NjFhNGIyYTM3ZDFkOGU3NzAwYjI2ODUzMTdjMTM0MjJiYTJmNWQ3ZjRhZWVkNTA4ZjE3M2VjMj
    AyOTA5YTRiMTM4MWMxMjYyYjJiMzc0ZmQ5NDBhN2E0NDA2ZTI2NTg3MTRkMmE3ZjRlOGI3NzM4MTM3
    NTA5NzNlMGY0OWI1NDNlZmRiY2JjZTE2OWIzOGQyNTRjMDAzNzIxMmFiN2FmODdlY2E1ZDgxMmYxM2
    Y3OTgzOWY=
    """,
    # Trunk packet
    """
    NWQ3NjFhNGIyYTM3ZDFkOGU3NzAwYjI2ODUzMTdjYjg0MjJiYTJmNWQ3ODJhZWVkNTA4ZjU2ZGVjMj
    AyOTA5YTQ5MTM4MWMzMjYyYTJiMzY0OTI2YmZiN2E0
    """,
    # Login packet 1
    """
    NWQ3NjFhNGIyYTM3ZDFkOGU3NzAwYjI2ODUzMTdjYmU0MjJiYTJmNWQ3OGJhZWVkNTA4ZjU2ZGVjMj
    AyOTA5YWE0ZWM4MWM2
    """,
    # Login packet 2
    """
    NWQ3MDFhNGIyYTM3ZDFkOGU3NzAwYjI2ODUzMTdjYjk0MjJiYTJmNWQ3OGJhZWVkNTA4ZjU2ZGVjMj
    AyOTA5YWE0ZWM4MWM2
    """
]


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
