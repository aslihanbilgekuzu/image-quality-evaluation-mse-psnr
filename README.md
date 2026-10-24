# Image Quality Evaluation Using MSE and PSNR

## Project Overview

This project evaluates image quality by applying controlled degradation methods to an image and comparing the processed image with the original using Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR).

The project includes an interactive Streamlit dashboard. Users can select one of six sample images or upload their own image, choose a degradation method, adjust its parameters, and view the processed image and quality metrics dynamically.

## Objectives

- Implement common image degradation methods.
- Calculate MSE and PSNR between original and processed images.
- Run repeatable experiments at different degradation levels.
- Display image comparisons, metrics, tables, and charts in an interactive dashboard.

## Image Degradation Methods

The system supports three degradation methods:

1. **Gaussian Noise** — adds adjustable random noise to an image.
2. **Gaussian Blur** — applies adjustable blur to reduce fine details.
3. **JPEG Compression** — compresses an image at a selected quality level.

Each processed image is generated from the original image. Degradation methods are not compounded unless a future project requirement explicitly adds that feature.

## Image Quality Metrics

- **Mean Squared Error (MSE):** Measures the average squared pixel difference between the original and processed images. Lower values generally indicate smaller pixel-level differences.
- **Peak Signal-to-Noise Ratio (PSNR):** Expresses the reconstruction quality in decibels (dB). Higher values generally indicate smaller pixel-level errors. Identical images have MSE = 0 and PSNR = infinity.

These metrics measure pixel-level differences and do not fully represent every aspect of perceived visual quality.

## Interactive Dashboard

The Streamlit dashboard will allow users to:

- Choose from six sample images.
- Upload a personal image in PNG, JPG, or JPEG format.
- Select Gaussian Noise, Gaussian Blur, or JPEG Compression.
- Adjust degradation parameters interactively.
- View original and processed images side by side.
- View MSE and PSNR values.
- Review experiment results and charts that update based on the selected image and settings.

Results are shown dynamically in the application. **CSV export is not part of the current project scope.** The evaluation module will collect experiment results in a Pandas DataFrame for the dashboard to display.

## Project Structure

```text
image-quality-evaluation-mse-psnr/
├── app.py
├── requirements.txt
├── README.md
├── INTERFACE_CONTRACT.md
├── src/
│   ├── __init__.py
│   ├── image_degradation.py
│   ├── metrics.py
│   └── evaluation.py
├── data/
│   └── original/
└── results/
    └── .gitkeep
```

## Technologies

- Python
- Streamlit
- NumPy
- OpenCV
- Pandas
- Matplotlib
- Pillow
- scikit-image (if needed by the implementation)

## Installation and Setup

### macOS / Linux

```bash
git clone https://github.com/YOUR_USERNAME/image-quality-evaluation-mse-psnr.git
cd image-quality-evaluation-mse-psnr
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows — Command Prompt

```bat
git clone https://github.com/YOUR_USERNAME/image-quality-evaluation-mse-psnr.git
cd image-quality-evaluation-mse-psnr
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Windows — PowerShell

```powershell
git clone https://github.com/YOUR_USERNAME/image-quality-evaluation-mse-psnr.git
cd image-quality-evaluation-mse-psnr
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Replace `YOUR_USERNAME` with the GitHub account that owns the repository.

## Running the Dashboard

With the virtual environment activated, run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL to open the dashboard in a browser.

## Experimental Workflow

1. Select a sample image or upload an image.
2. Select a degradation method.
3. Adjust the relevant parameter.
4. Generate a processed image from the original.
5. Calculate MSE and PSNR.
6. Display the image comparison and metric values.
7. Use the evaluation module to compare multiple parameter settings in a Pandas DataFrame and display the results in the dashboard.

## Team Responsibilities

- **Person 1 — Image Degradation:** Implement Gaussian noise, Gaussian blur, and JPEG compression in `src/image_degradation.py`.
- **Person 2 — Metrics:** Implement MSE and PSNR in `src/metrics.py`.
- **Person 3 — Evaluation:** Integrate degradation and metric functions, run experiments across parameter levels, and organize results in a Pandas DataFrame. CSV export is currently out of scope.
- **Person 4 — Dashboard:** Develop the Streamlit interface, sample image gallery, image upload, interactive controls, metric display, tables, and charts.

## Scope and Limitations

The project focuses on controlled image degradation and pixel-based quality evaluation. MSE and PSNR are useful quantitative measures but may not always match human perception. Dashboard results depend on the selected image and degradation parameters. The current version displays results dynamically and does not require CSV export.
