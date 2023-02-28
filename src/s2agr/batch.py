
def batch(values, batch_size):
    result = []
    while len(values) > 0:
        next_block_end = min(batch_size, len(values))
        result.append(values[:next_block_end])
        values = values[next_block_end:]
    return result