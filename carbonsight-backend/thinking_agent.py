def allocate_thinking_budget(complexity):
    if complexity == "simple":
        return 256
    if complexity == "medium":
        return 1024
    return 4096

