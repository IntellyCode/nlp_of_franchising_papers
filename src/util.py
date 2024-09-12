import numpy as np


def compress_with_ln(values: np.array) -> np.array:
    """
    Compresses an array of integers into the range from 1 to 5 using a logarithmic function.

    Args:
        values (np.array): Array of integers to compress.

    Returns:
        np.array: Array of compressed values scaled from 1 to 5.
    """
    min_value = np.min(values)
    values = values + min_value * 0.1
    log_values = np.log(values)

    log_min = np.min(log_values)
    log_max = np.max(log_values)
    normalized_values = (log_values - log_min) / (log_max - log_min)

    compressed_values = 1 + 10 * normalized_values
    return compressed_values


def compress_linear(values: np.array) -> np.array:
    """
    Compresses an array of integers into the range from 1 to 5 using a linear function.

    Args:
        values (np.array): Array of integers to compress.

    Returns:
        np.array: Array of compressed values scaled from 1 to 5.
    """
    min_value = np.min(values)
    max_value = np.max(values)

    # Avoid division by zero if all values are the same
    if min_value == max_value:
        return np.full_like(values, 3, dtype=np.float64)

    # Linear normalization to the range [0, 1]
    normalized_values = (values - min_value) / (max_value - min_value)

    # Scale to the range [1, 5]
    compressed_values = 3.5 + 4 * normalized_values
    return compressed_values


def compress_quadratic(values: np.array) -> np.array:
    """
    Compresses an array of integers into the range from 1 to 5 using a quadratic function.

    Args:
        values (np.array): Array of integers to compress.

    Returns:
        np.array: Array of compressed values scaled from 1 to 5.
    """
    min_value = np.min(values)
    max_value = np.max(values)

    # Avoid division by zero if all values are the same
    if min_value == max_value:
        return np.full_like(values, 3, dtype=np.float64)

    # Quadratic normalization to the range [0, 1]
    normalized_values = (values - min_value) / (max_value - min_value)
    quadratic_values = normalized_values ** 2

    # Scale to the range [1, 5]
    compressed_values = 1 + 4 * quadratic_values
    return compressed_values


if __name__ == '__main__':
    l = [('nlp', 17), ('language', 12), ('text', 10), ('models', 7), ('human', 6), ('recognition', 6), ('learning', 5), ('tasks', 5), ('such', 5), ('words', 5), ('natural', 4)]
    x = []
    for i in l:
        x.append(i[1])
    print(x)
    print(compress_with_ln(x))