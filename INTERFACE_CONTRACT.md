# Project Interface Contract and Naming Standard

**Project:** Image Quality Evaluation Using MSE and PSNR  
**Purpose:** Keep the modules developed by different team members compatible during integration.

## 1. General Rules

- Use the public function names and parameter names defined in this document when calling functions across modules.
- Use **RGB NumPy arrays with `uint8` values in the range 0–255** as the standard image representation passed between modules.
- Image degradation functions must return a processed image and must not modify the original input array in place.
- Metric functions compare original and processed images and return numeric values.
- `app.py` and `evaluation.py` should call the public functions listed below instead of duplicating their implementations.
- Local helper variables inside a function may have different names. They do not need to match names in other files unless they are part of a public function's inputs or outputs.
- If the team changes a function interface or return structure, update all callers and this document.

## 2. Shared Names

| Name | Meaning | Used by |
|---|---|---|
| `original_image` | Original RGB image as a NumPy array | `app.py`, `evaluation.py` |
| `processed_image` | Image returned by a degradation function | `app.py`, `evaluation.py` |
| `mse_value` | Calculated Mean Squared Error | `metrics.py`, `evaluation.py`, `app.py` |
| `psnr_value` | Calculated PSNR in dB | `metrics.py`, `evaluation.py`, `app.py` |
| `method` | Selected degradation method | `app.py`, `evaluation.py` |
| `parameters` | Parameters for an experiment | `evaluation.py` |
| `results_df` | Pandas DataFrame containing experiment results | `evaluation.py`, `app.py` |

These are recommended shared names, not a requirement that every local variable in every module use the same name.

## 3. `src/image_degradation.py`

**Owner:** Person 1 — Image Degradation

### Public functions

```python
def add_gaussian_noise(image, mean=0, sigma=20):
    ...

def apply_gaussian_blur(image, kernel_size=5, sigma=1.0):
    ...

def apply_jpeg_compression(image, quality=75):
    ...
```

### Parameter conventions

| Parameter | Meaning | Convention |
|---|---|---|
| `image` | Input image | RGB NumPy array, `uint8`, values 0–255 |
| `mean` | Mean of Gaussian noise | Default `0` |
| `sigma` | Noise standard deviation or blur sigma | Function-specific default |
| `kernel_size` | Gaussian blur kernel width and height | Positive odd integer, e.g. 3, 5, 7 |
| `quality` | JPEG quality | Integer from 1 to 100 |

### Requirements

- Return a new RGB `uint8` NumPy array.
- Keep the original input unchanged.
- Keep output pixel values in the 0–255 range.
- When using OpenCV JPEG encoding, convert RGB to BGR as required and convert the decoded result back to RGB.
- Do not calculate MSE or PSNR in this module.

## 4. `src/metrics.py`

**Owner:** Person 2 — Metrics

### Public functions

```python
def calculate_mse(original, processed):
    ...

def calculate_psnr(original, processed):
    ...
```

### Requirements

- Accept grayscale or RGB images when both inputs have compatible shapes and channel layouts.
- Validate input dimensions and shapes.
- Return `0.0` for MSE when images are identical.
- Return positive infinity for PSNR when MSE is zero.
- For 8-bit images, use 255 as the peak pixel value.
- Do not modify input images.

The public parameter names are `original` and `processed`. A caller can pass variables named `original_image` and `processed_image`; the caller's variable names do not need to match the function's local parameter names.


- Use `scikit-image` (`skimage.metrics`) to calculate MSE and PSNR.
- Use `mean_squared_error()` for MSE calculation.
- Use `peak_signal_noise_ratio()` for PSNR calculation with `data_range=255`.


## 5. `src/evaluation.py`

**Owner:** Person 3 — Evaluation and Experiment Management

### Recommended public function

```python
def run_experiment(original_image, method, parameters):
    ...
```

The team should agree on the exact return structure before implementation. Recommended result structure for one experiment:

```python
{
    "method": method,
    "parameters": parameters,
    "mse_value": mse_value,
    "psnr_value": psnr_value,
}
```

### Responsibilities

- Call the public functions in `image_degradation.py` and `metrics.py`.
- Run experiments at multiple degradation parameter levels.
- Generate every processed image from the original image, not from a previously degraded result.
- Collect experiment records and convert them into a Pandas DataFrame named `results_df`.
- Provide the results DataFrame to the dashboard for dynamic tables and charts.

**CSV export is out of scope for the current version.** Do not add CSV file-writing functionality unless the team later agrees to expand the project scope.

Example column names:

- `method`
- `parameters`
- `mse_value`
- `psnr_value`

If the team chooses a different return structure or column naming, update this contract and ensure `app.py` uses the same structure.

## 6. `app.py`

**Owner:** Person 4 — Dashboard

### Responsibilities

- Let users choose one of six sample images or upload their own image.
- Convert loaded images to RGB NumPy arrays with `uint8` values.
- Let users select a degradation method and adjust parameters.
- Call the appropriate degradation function.
- Call `calculate_mse` and `calculate_psnr`.
- Display original and processed images, MSE, PSNR, and experiment tables/charts.
- Use `original_image`, `processed_image`, `mse_value`, and `psnr_value` as shared result variable names.
- Display evaluation results dynamically from a Pandas DataFrame.

The dashboard must not reimplement degradation algorithms or metric formulas already implemented in `src/`.

## 7. Image Format and OpenCV

Use **RGB** as the standard format passed between project modules.

- Convert Pillow images to RGB before converting them to NumPy arrays.
- OpenCV may require BGR for certain operations, including JPEG encoding. Convert only at the OpenCV boundary, then convert back to RGB before returning the result.
- The dashboard's standard image input should be RGB.
- Ensure original and processed images have matching shapes before calculating metrics.

## 8. Example of a Consistent Call

```python
processed_image = add_gaussian_noise(
    original_image.copy(),
    mean=0,
    sigma=20,
)

mse_value = calculate_mse(original_image, processed_image)
psnr_value = calculate_psnr(original_image, processed_image)
```

Local helper names such as `noise`, `difference`, `encoded_image`, and `max_pixel_value` may differ by module. Shared module interfaces must remain consistent.

## 9. Team Integration Checklist

- [ ] Public function names match this document.
- [ ] Function calls use valid parameter names.
- [ ] Degradation functions return RGB `uint8` NumPy arrays.
- [ ] Original images are not modified in place.
- [ ] MSE and PSNR functions accept outputs from the degradation module.
- [ ] Identical images produce MSE = 0 and PSNR = infinity.
- [ ] Every experiment starts from the original image.
- [ ] Evaluation result keys and DataFrame columns match what `app.py` expects.
- [ ] Evaluation results are shown dynamically in the dashboard.
- [ ] CSV export is not added unless the team explicitly expands the scope.
- [ ] Any interface changes are reflected in every caller and this document.

---
**Team rule:** Local variable names may differ; module interfaces must not.
