class InspectionEngine:

    def __init__(self):

        pass

    def run(
        self,
        image,
        tools
    ):

        final_result = "OK"

        results = []

        for tool in tools:

            result = tool.inspect(
                image
            )

            results.append(
                result
            )

            if result["result"] != "OK":

                final_result = "NG"

        return (
            final_result,
            results
        )