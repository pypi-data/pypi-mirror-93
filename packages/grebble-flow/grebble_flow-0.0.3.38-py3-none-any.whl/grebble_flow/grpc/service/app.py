import json

from grebble_flow.protobuf.protobuf import app_pb2_grpc
from grebble_flow.managment.info import generate_package_info


class AppService(app_pb2_grpc.ExternalAppServicer):
    def __init__(self, *args, **kwargs):
        pass

    def AppInfo(self, request, context):
        info = generate_package_info()

        result = app_pb2_grpc.AppInfoExternalResponse()
        result.processors.extend(
            [
                app_pb2_grpc.ProcessorExternalInfo(
                    name=processor["name"],
                    attributeSchema=json.dumps(processor["attributes_schema"])
                    if processor.get("attributes_schema")
                    else "",
                )
                for processor in info["processors"]
            ]
        )
        return result
