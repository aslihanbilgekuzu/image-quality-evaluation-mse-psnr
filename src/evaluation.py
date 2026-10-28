# Integrates image degradation functions with MSE and PSNR metrics.
# Runs experiments across selected methods and parameter levels.
# Collects experiment results in a Pandas DataFrame.

import pandas as pd

from src.image_degradation import (
    add_gaussian_noise,
    apply_gaussian_blur,
    apply_jpeg_compression,
)

from src.metrics import calculate_mse, calculate_psnr


def run_experiment(original_image, method, parameters):
    """
    Run one degradation experiment and calculate MSE and PSNR.

    Args:
        original_image: Original RGB uint8 NumPy image.
        method: Name of the degradation method.
        parameters: Dictionary containing degradation parameters.

    Returns:
        Dictionary containing method, parameters, MSE, and PSNR.
    """

    degradation_methods = {
        "gaussian_noise": add_gaussian_noise,
        "gaussian_blur": apply_gaussian_blur,
        "jpeg_compression": apply_jpeg_compression,
    }

    if method not in degradation_methods:
        raise ValueError(
            f"Unsupported method: {method}. "
            f"Available methods: {list(degradation_methods.keys())}"
        )

    # Always start from the original image.
    processed_image = degradation_methods[method](
        original_image.copy(),
        **parameters,
    )

    # Calculate image quality metrics.
    mse_value = calculate_mse(original_image, processed_image)
    psnr_value = calculate_psnr(original_image, processed_image)

    return {
        "method": method,
        "parameters": parameters.copy(),
        "mse_value": mse_value,
        "psnr_value": psnr_value,
        "processed_image": processed_image
    }


def run_evaluation(original_image, experiments):
    """
    Run multiple experiments and collect their results.

    Args:
        original_image: Original RGB uint8 NumPy image.
        experiments: List of experiment dictionaries.

    Returns:
        Pandas DataFrame containing all experiment results.
    """

    results = []

    for experiment in experiments:
        result = run_experiment(
            original_image=original_image,
            method=experiment["method"],
            parameters=experiment["parameters"],
        )

        results.append(result)

    results_df = pd.DataFrame(results)

    return results_df

