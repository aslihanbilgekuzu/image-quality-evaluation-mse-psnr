# Project Interface Contract and Naming Standard

**Project:** Image Quality Evaluation Using MSE and PSNR\
**Purpose:** Keep the code written by all team members compatible when
modules are integrated.

## 1. General Rules

-   Use the function names and parameter names defined in this document
    when calling functions across modules.
-   Use the same image representation throughout the project: **RGB
    NumPy arrays with `uint8` values in the range 0--255**.
-   Image-processing functions must return a processed image as a NumPy
    array. They must not modify the original input array in place.
-   Metric functions compare the original and processed images and
    return numeric values.
-   `app.py` and `evaluation.py` should call the public functions listed
    below rather than duplicate their implementations.
-   Local helper variables inside a function may have different names.
    They do not need to match variables in other files unless they are
    part of a function's inputs or outputs.
-   Keep function names, parameter names, return types, and image format
    conventions consistent. If the team changes one, update all callers
    and this document.

## 2. Shared Names

  -----------------------------------------------------------------------
  Name                    Meaning                 Used by
  ----------------------- ----------------------- -----------------------
  `original_image`        Original RGB image as a `app.py`,
                          NumPy array             `evaluation.py`

  `processed_image`       Image returned by a     All modules that use
                          degradation function    degradation results

  `mse_value`             Calculated Mean Squared `metrics.py`,
                          Error                   `evaluation.py`,
                                                  `app.py`

  `psnr_value`            Calculated Peak         `metrics.py`,
                          Signal-to-Noise Ratio   `evaluation.py`,
                          in dB                   `app.py`

  `method`                Selected degradation    `app.py`,
                          method                  `evaluation.py`

  `parameters`            Configuration for a     `evaluation.py`
                          particular experiment   

  `results_df`            Pandas DataFrame        `evaluation.py`,
                          containing experiment   `app.py`
                          results                 
  -----------------------------------------------------------------------

Names in this table are recommended shared names. A local variable can
use another name when it stays inside its own function and is not part
of a module interface.

## 3. `src/image_degradation.py`

**Owner:** Person 1 --- Image Degradation Module

### Public functions

``` python
def add_gaussian_noise(image, mean=0, sigma=20):
    """Return a copy of the image with Gaussian noise added."""
    ...

def apply_gaussian_blur(image, kernel_size=5, sigma=1.0):
    """Return a blurred copy of the image."""
    ...

def apply_jpeg_compression(image, quality=75):
    """Return a copy of the image after JPEG compression."""
    ...
```

### Parameter conventions

  -----------------------------------------------------------------------
  Parameter               Meaning                 Convention
  ----------------------- ----------------------- -----------------------
  `image`                 Input image             RGB NumPy array,
                                                  `uint8`, values 0--255

  `mean`                  Mean of the Gaussian    Default `0`
                          noise                   

  `sigma`                 Noise standard          Default depends on
                          deviation or blur sigma function

  `kernel_size`           Gaussian blur kernel    Positive odd integer,
                          width and height        e.g. 3, 5, 7

  `quality`               JPEG quality            Integer from 1 to 100
  -----------------------------------------------------------------------

### Requirements

-   Return a new RGB `uint8` NumPy array.
-   Keep the original input unchanged.
-   Clip or otherwise safely convert output pixel values to the valid
    0--255 range.
-   JPEG compression may require converting RGB to BGR before OpenCV
    encoding and converting back to RGB after decoding.
-   Do not calculate MSE or PSNR in this module.

## 4. `src/metrics.py`

**Owner:** Person 2 --- Image Quality Metrics

### Public functions

``` python
def calculate_mse(original, processed):
    """Return the mean squared pixel error as a float."""
    ...

def calculate_psnr(original, processed):
    """Return PSNR in decibels as a float."""
    ...
```

### Requirements

-   Accept RGB or grayscale images, provided both inputs have matching
    dimensions and channel layouts.
-   Validate that the original and processed images have compatible
    shapes.
-   `calculate_mse` returns `0.0` when the images are identical.
-   `calculate_psnr` returns positive infinity when MSE is zero.
-   For 8-bit images, use a peak pixel value of 255.
-   Do not modify either input image.

**Important:** The function parameter names `original` and `processed`
are the public interface. Callers can pass `original_image` and
`processed_image` as their values; the local variable names do not have
to be identical.

## 5. `src/evaluation.py`

**Owner:** Person 3 --- Evaluation and Experiment Management

### Recommended public function

``` python
def run_experiment(original_image, method, parameters):
    """Run one degradation experiment and return its results."""
    ...
```

The team should agree on the exact return structure before
implementation. Recommended return value:

``` python
{
    "method": method,
    "parameters": parameters,
    "mse_value": mse_value,
    "psnr_value": psnr_value,
}
```

### Requirements

-   Call the public functions from `image_degradation.py` and
    `metrics.py`.
-   Generate every processed image from the original image, not from a
    previously degraded result.
-   Store experiment records in a list and convert them into a Pandas
    DataFrame named `results_df`.
-   Export results to CSV when requested.
-   Use consistent column names, for example: `method`, `parameters`,
    `mse_value`, `psnr_value`.

If the team chooses a different return structure, document it here and
ensure `app.py` uses the same structure.

## 6. `app.py`

**Owner:** Person 4 --- Interactive Dashboard

### Responsibilities

-   Let users choose one of six sample images or upload their own image.
-   Convert loaded images to RGB NumPy arrays with `uint8` values.
-   Let users select a degradation method and adjust its parameters.
-   Call the appropriate degradation function.
-   Call `calculate_mse` and `calculate_psnr`.
-   Display original and processed images, MSE, PSNR, charts, and
    experiment results.
-   Use `original_image`, `processed_image`, `mse_value`, and
    `psnr_value` for the shared result variables.

The dashboard should not reimplement image degradation or metric
formulas already implemented in `src/`.

## 7. Image Format and OpenCV

Use **RGB** as the standard format passed between project modules.

-   Pillow images should be converted with `image.convert("RGB")` before
    being converted to NumPy arrays.
-   OpenCV commonly expects **BGR** for color images in some operations,
    including JPEG encoding. Convert to BGR only where required by
    OpenCV, then convert the result back to RGB before returning it.
-   Grayscale images may be supported by the metric functions, but the
    dashboard's standard input should be RGB.
-   Ensure the original and processed images have matching shapes before
    calculating metrics.

## 8. Example of a Consistent Call

``` python
processed_image = add_gaussian_noise(
    original_image.copy(),
    mean=0,
    sigma=20,
)

mse_value = calculate_mse(
    original_image,
    processed_image,
)

psnr_value = calculate_psnr(
    original_image,
    processed_image,
)
```

The names `original_image`, `processed_image`, `mse_value`, and
`psnr_value` are shared conventions. Names such as `noise`,
`difference`, `encoded_image`, or `max_pixel_value` may be used as local
helper variables inside their respective modules.

## 9. Team Integration Checklist

-   [ ] Public function names match this document.
-   [ ] Function calls use valid parameter names.
-   [ ] Degradation functions return RGB `uint8` NumPy arrays.
-   [ ] Original images are not modified in place.
-   [ ] MSE and PSNR functions accept the outputs from the degradation
    module.
-   [ ] Identical images produce MSE = 0 and PSNR = infinity.
-   [ ] Every experiment starts from the original image.
-   [ ] Evaluation result keys and DataFrame column names match what
    `app.py` expects.
-   [ ] Any agreed interface change is reflected in every caller and in
    this document.

------------------------------------------------------------------------

**Team rule:** Local variable names may differ; module interfaces must
not.
