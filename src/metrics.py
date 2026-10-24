# Implements calculating methods of Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR).
# Handles identical images, where MSE is zero and PSNR is infinite.
# Supports both grayscale and RGB images.
# Provides reliable image quality metrics and example calculations.

import numpy as np
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio

# Peak pixel value for 8-bit images.
MAX_PIXEL_VALUE = 255


def _validate_images(original, processed):
    """İki görüntünün metrik hesabı için uygun olduğunu doğrular.

    Hatalar:
        TypeError: Girdilerden biri NumPy dizisi değilse.
        ValueError: Şekiller farklıysa veya görüntü (H, W) ya da (H, W, 3) değilse.
    """

    for name, image in (("original", original), ("processed", processed)):
        if not isinstance(image, np.ndarray):
            raise TypeError(
                f"{name} must be a NumPy array, got {type(image).__name__}."
            )

        is_grayscale = image.ndim == 2
        is_rgb = image.ndim == 3 and image.shape[2] == 3

        if not (is_grayscale or is_rgb):
            raise ValueError(
                f"{name} must have shape (H, W) or (H, W, 3), got {image.shape}."
            )

    if original.shape != processed.shape:
        raise ValueError(
            "original and processed must have the same shape, "
            f"got {original.shape} and {processed.shape}."
        )


def calculate_mse(original, processed):
    """İki görüntü arasındaki Ortalama Kare Hatayı (MSE) hesaplar.

    Parametreler:
        original: Orijinal görüntü, (H, W) veya (H, W, 3) NumPy dizisi.
        processed: İşlenmiş görüntü, original ile aynı şekilde NumPy dizisi.

    Dönüş:
        float: MSE değeri. Özdeş görüntülerde 0.0.

    Hatalar:
        TypeError: Girdilerden biri NumPy dizisi değilse.
        ValueError: Şekiller farklıysa veya desteklenmeyen boyuttaysa.
    """

    _validate_images(original, processed)

    mse_value = mean_squared_error(original, processed)

    return float(mse_value)


def calculate_psnr(original, processed):
    """İki görüntü arasındaki Tepe Sinyal-Gürültü Oranını (PSNR) dB cinsinden hesaplar.

    Parametreler:
        original: Orijinal görüntü, (H, W) veya (H, W, 3) NumPy dizisi.
        processed: İşlenmiş görüntü, original ile aynı şekilde NumPy dizisi.

    Dönüş:
        float: PSNR değeri (dB). Özdeş görüntülerde (MSE == 0) float("inf").

    Hatalar:
        TypeError: Girdilerden biri NumPy dizisi değilse.
        ValueError: Şekiller farklıysa veya desteklenmeyen boyuttaysa.
    """

    mse_value = calculate_mse(original, processed)

    # Return infinity directly to avoid scikit-image's divide-by-zero warning.
    if mse_value == 0:
        return float("inf")

    psnr_value = peak_signal_noise_ratio(
        original,
        processed,
        data_range=MAX_PIXEL_VALUE,
    )

    return float(psnr_value)
