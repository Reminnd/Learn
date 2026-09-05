def get_weather(city: str) -> str:
    return f"{city}: sunny"


weather_tool = {
    "name": "get_weather",
    "description": "查询指定城市的当前天气",
    "handler": get_weather,
}


def execute_tool(tool, tool_call):
    if tool_call.get("name") != tool["name"]:
        return {
            "ok": False,
            "action": "fail_fast",
            "error": {
                "code": "unknown_tool",
                "message": f"未知工具: {tool_call['name']}",
            },
        }

    args = tool_call.get("args", {})

    if "city" not in args or not isinstance(args["city"], str):
        return {
            "ok": False,
            "action": "retry_model",
            "error": {
                "code": "invalid_arguments",
                "message": "参数 city 缺失或不是字符串",
            },
        }

    result = tool["handler"](**args)
    return {
        "ok": True,
        "action": "success",
        "tool_call_id": tool_call["id"],
        "output": result,
    }


tool_calls = [
    {"name": "get_weather", "args": {"city": "上海"}, "id": "call_001"},
    {"name": "search_database", "args": {"city": "上海"}, "id": "call_002"},
    {"name": "get_weather", "args": {}, "id": "call_003"},
]

for tool_call in tool_calls:
    print(execute_tool(weather_tool, tool_call))
