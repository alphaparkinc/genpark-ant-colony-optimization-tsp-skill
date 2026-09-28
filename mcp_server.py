import sys
import json
from client import AntColonyOptimizer

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-ant-colony-optimization-tsp-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "solve_tsp",
                    "description": "Find shortest closed tour visiting all nodes using Ant Colony Optimization",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "distance_matrix": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                            "iterations": {"type": "integer", "default": 30}
                        },
                        "required": ["distance_matrix"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "solve_tsp":
            dist = args.get("distance_matrix", [])
            it = args.get("iterations", 30)
            aco = AntColonyOptimizer()
            data = aco.solve_tsp(dist, iterations=it)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
