class ToolManager:

    def __init__(self):

        self.roi_tools = {}

    def add_tool(
        self,
        roi_index,
        tool_name
    ):

        if roi_index not in self.roi_tools:

            self.roi_tools[roi_index] = []

        if tool_name not in self.roi_tools[roi_index]:

            self.roi_tools[roi_index].append(
                tool_name
            )

    def get_tools(
        self,
        roi_index
    ):

        return self.roi_tools.get(
            roi_index,
            []
        )

    def clear(self):

        self.roi_tools.clear()