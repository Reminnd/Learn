def get_weather(city: str) -> str:
    if city == "超时城市":
        raise TimeoutError("天气服务超时")
    if not city:
        raise ValueError("城市不能为空")
    return f"{city}: sunny"


weather_tool = {
    "name": "get_weather",
    "description": "查询指定城市的当前天气",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
        "additionalProperties": False,
    },
    "handler": get_weather,
}


def execute_tool(tool, tool_call, retry_count=0, max_retries=2):
    requested_name = tool_call.get("name")
    if requested_name != tool["name"]:
        return {
            "ok": False,
            "action": "fail_fast",
            "error": {"code": "unknown_tool", "message": f"未知工具: {requested_name}"},
        }

    args = tool_call.get("args")
    if not isinstance(args, dict):
        return {
            "ok": False,
            "action": "retry_model",
            "error": {"code": "invalid_arguments", "message": "参数 args 不是字典"},
        }

    if "city" not in args or not isinstance(args["city"], str):
        if retry_count >= max_retries:
            return {
                "ok": False,
                "action": "fail_fast",
                "error": {"code": "retry_exhausted", "message": "参数 city 无效且重试耗尽"},
            }
        return {
            "ok": False,
            "action": "retry_model",
            "error": {"code": "invalid_arguments", "message": "参数 city 缺失或不是字符串"},
        }

    extra_fields = set(args) - {"city"}
    if extra_fields:
        return {
            "ok": False,
            "action": "fail_fast",
            "error": {"code": "invalid_arguments", "message": f"不允许额外字段: {extra_fields}"},
        }

    city = args["city"].strip()
    if not city:
        return {
            "ok": False,
            "action": "fail_fast",
            "error": {"code": "invalid_arguments", "message": "参数 city 不能为空"},
        }

    try:
        result = tool["handler"](city=city)
    except TimeoutError as exc:
        return {
            "ok": False,
            "action": "retry_tool",
            "error": {"code": "tool_timeout", "message": str(exc)},
        }
    except ValueError as exc:
        return {
            "ok": False,
            "action": "fail_fast",
            "error": {"code": "business_error", "message": str(exc)},
        }

    return {
        "ok": True,
        "action": "success",
        "tool_call_id": tool_call.get("id"),
        "output": result,
    }


tool_calls = [
    {"name": "get_weather", "args": {"city": " 上海 "}, "id": "call_001"},
    {"name": "get_weather", "args": {"city": 123, "unit": "celsius"}, "id": "call_002"},
    {"name": "get_weather", "args": {"city": "超时城市"}, "id": "call_003"},
]

for tool_call in tool_calls:
    print(execute_tool(weather_tool, tool_call))


# @tool mapping submitted:
# function name: get_weather  (needs review; decorated function is get_weather_tool)
# docstring: 查询指定城市的当前天气。
# annotations: city: str -> str
# body: return get_weather(city)
