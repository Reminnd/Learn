def execute_tool(tool, tool_call):
    if tool_call["name"] != tool["name"]:
        return {
            "ok": False,
            "action": "fail_fast",
            "error": {
                "code": "unknown_tool",
                "message": f"未知工具: {tool_call['name']}",
            },
        }

    args = tool_call.get("args", {})

    elif "city" not in args or not isinstance(args["city"], str):
        return {
            "ok": False,
            "action": "retry_model",
            "error": {
                "code": "invalid_arguments",
                "message": "参数 city 缺失或不是字符串",
            },
        }

    elif tool_call["name"] == tool["name"]:
        result = tool["handler"](**args)
        return {
            "ok": True,
            "action": "success",
            "tool_call_id": tool_call["id"],
            "output": result,
        }
