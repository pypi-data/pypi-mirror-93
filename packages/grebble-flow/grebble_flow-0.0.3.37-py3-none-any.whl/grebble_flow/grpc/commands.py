import os
from pathlib import Path

import pkg_resources


def install_proto():
    import grpc_tools.protoc

    proto_include = pkg_resources.resource_filename(
        "grebble_flow", "proto/internal/v1/"
    )
    python_out = pkg_resources.resource_filename(
        "grebble_flow", "grpc/generated/internal"
    )
    for file in ["app.proto", "processor.proto"]:
        grpc_tools.protoc.main(
            [
                "grpc_tools.protoc",
                f"--proto_path={proto_include}",
                f"--python_out={python_out}",
                f"--grpc_python_out={python_out}",
                f"{proto_include}/{file}",
            ]
        )
