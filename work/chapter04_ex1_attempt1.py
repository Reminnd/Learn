def get_weather(city: str) -> str:
    return f"{city}: sunny"


def search_city(city: str) -> str:
    return f"找到城市：{city}"


weather_tool = {
    "name": "get_weather",
    "description": "查询城市天气",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
        },
        "required": ["city"],
        "additionalProperties": False,
    },
    "handler": get_weather,
}


search_tool = {
    "name": "search_city",
    "description": "查询城市信息",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
        },
        "required": ["city"],
        "additionalProperties": False,
    },
    "handler": search_city,
}


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool):
        name = tool["name"]
        if name in self._tools:
            raise ValueError(f"工具名称 '{name}' 已存在")
        self._tools[name] = tool

    def get(self, name):
        if name not in self._tools:
            raise LookupError(f"工具名称 '{name}' 不存在")
        return self._tools[name]

    def list_specs(self):
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            }
            for tool in self._tools.values()
        ]


registry = ToolRegistry()
registry.register(weather_tool)
registry.register(search_tool)

tool = registry.get("get_weather")
result = tool["handler"](city="上海")

print(registry.list_specs())

duplicate_weather_tool = {
    **weather_tool,
    "description": "另一个天气工具",
}

try:
    registry.register(duplicate_weather_tool)
except ValueError as exc:
    print("捕获工具冲突：", exc)


# 原理版：ALL_TOOLS dict -> ToolRegistry
# LangChain / LangGraph：
# Tool 对象列表 -> model.bind_tools(tools) -> AIMessage.tool_calls
# -> ToolNode / Executor -> ToolMessage
