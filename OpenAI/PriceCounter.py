import tiktoken

PRICING = {
    "gpt-4o-mini":{"input": 0.150 / 1_000_000, "output": 0.600 / 1_000_000}
}


def count_tokens(text, model="gpt-4"):
    # Get the correct encoding based on the model
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def calculate_cost(input_tokens, output_tokens, model="gpt-4"):
    input_cost = input_tokens * PRICING[model]["input"]
    output_cost = output_tokens * PRICING[model]["input"]

    # Total cost
    total_cost = input_cost + output_cost
    return total_cost
