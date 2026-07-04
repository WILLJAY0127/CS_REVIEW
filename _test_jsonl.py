import json

PATH = r'C:/Users/Administrator/.claude/projects/D--myfile-CS-REVIEW/8d7b0866-8476-4af7-9558-e0c21b698d4c.jsonl'

n = 0
types = {}
samples = {'user': None, 'assistant': None}
with open(PATH, encoding='utf-8') as f:
    for line in f:
        n += 1
        try:
            obj = json.loads(line)
        except:
            continue
        t = obj.get('type', '?')
        types[t] = types.get(t, 0) + 1
        # capture first user/assistant message sample
        if t in ('user', 'assistant') and samples.get(t) is None:
            msg = obj.get('message', {})
            content = msg.get('content', '')
            if isinstance(content, list):
                parts = []
                for c in content:
                    if isinstance(c, dict):
                        if c.get('type') == 'text':
                            parts.append(c.get('text', ''))
                        elif c.get('type') == 'tool_use':
                            parts.append(f"[tool_use: {c.get('name')}]")
                        elif c.get('type') == 'tool_result':
                            parts.append("[tool_result]")
                content = ' | '.join(parts)
            samples[t] = str(content)[:200]

print(f"total lines: {n}")
print(f"types: {types}")
print(f"\n--- sample user msg ---\n{samples.get('user')}")
print(f"\n--- sample assistant msg ---\n{samples.get('assistant')}")
