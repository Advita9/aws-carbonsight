from bedrock_client import invoke_nova

def generate_plan(prompt: str):
    system_prompt = (
        "You are an execution planner for an AI system.\n"
        "Your task is to generate a step-by-step execution plan.\n\n"
        "STRICT RULES:\n"
        "- Steps must be ACTIONS, not explanations\n"
        "- Each step must start with a VERB (analyze, fetch, compute, generate, etc.)\n"
        "- NO definitions\n"
        "- NO examples\n"
        "- NO summaries\n"
        "- NO numbering\n"
        "- 3 to 6 steps ONLY\n"
        "- Each step on a new line\n\n"
        "User query:\n"
        f"{prompt}\n\n"
        "Execution plan:"
    )


    plan_text = invoke_nova(
        "amazon.nova-micro-v1:0",
        prompt=system_prompt,
        max_tokens=120   # very small
    )

    if not plan_text:
        return []

    steps = [
        line.strip()
        for line in plan_text.split("\n")
        if line.strip()
    ]

    return steps
