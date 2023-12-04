

class NancyHttpServer:
    host: str = "localhost"
    port: int = 1006

    @staticmethod
    def getServerUrl():
        return f"http://{NancyHttpServer.host}:{NancyHttpServer.port}"

    @staticmethod
    def getCurveApiUrl():
        return f"{NancyHttpServer.getServerUrl()}/curve"

    @staticmethod
    def getOperationUrl(operation: str):
        return f"{NancyHttpServer.getCurveApiUrl()}/{operation}"

    @staticmethod
    def getCurveOperationUrl(curveId: str, operation: str):
        return f"{NancyHttpServer.getCurveApiUrl()}/{curveId}/{operation}"
