# Image Quality Evaluation Using MSE and PSNR

## 1. Project Overview

This project aims to evaluate image quality by applying different image degradation methods and measuring their effects using Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR).

The project focuses on three degradation methods: Gaussian noise, Gaussian blur, and JPEG compression. By adjusting the parameters of these methods, users will be able to observe how different levels of degradation affect image quality.

An interactive dashboard built with Streamlit will allow users to compare original and processed images, adjust degradation parameters dynamically, and observe the corresponding MSE and PSNR values.

## 2. Project Objectives

The main objectives of this project are to:

- Implement different image degradation methods using Python.
- Calculate MSE and PSNR to evaluate differences between original and processed images.
- Investigate the relationship between degradation intensity and image quality.
- Develop an interactive dashboard for visual and numerical comparison.
- Present experimental results through metrics, tables, and visualizations.

## 3. Image Degradation Methods

The project will investigate the following methods:

### Gaussian Noise

Adds random noise to an image to simulate visual disturbances. The noise intensity can be adjusted to investigate its effect on image quality.

### Gaussian Blur

Applies a Gaussian filter to smooth an image and reduce fine details. Different kernel sizes will be used to examine the effects of increasing blur.

### JPEG Compression

Compresses an image at different JPEG quality levels to investigate compression-related distortion and information loss.

## 4. Image Quality Metrics

### Mean Squared Error (MSE)

MSE measures the average squared difference between corresponding pixel values in the original and processed images.

A lower MSE indicates smaller pixel-level differences. An MSE of zero means that the compared images are identical at the pixel level.

### Peak Signal-to-Noise Ratio (PSNR)

PSNR expresses image reconstruction error in decibels (dB) using the MSE value.

A higher PSNR generally indicates lower pixel-level error relative to the maximum possible pixel value.

Both metrics will be used to compare the effects of different degradation methods and parameter settings.

## 5. Interactive Dashboard

The Streamlit dashboard will provide a user interface for exploring image degradation and quality evaluation.

Planned features include:

- Selecting an original image.
- Choosing a degradation method.
- Adjusting degradation intensity using sliders.
- Viewing original and processed images side by side.
- Calculating and displaying MSE and PSNR dynamically.
- Visualizing relationships between degradation parameters and quality metrics.
- Exporting experimental results to CSV.

The dashboard will use the original image as the reference for each experiment. Changing a parameter will generate a new processed image and recalculate the metrics.

## 6. Project Structure

```text
image-quality-evaluation-mse-psnr/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── image_degradation.py
│   ├── metrics.py
│   └── evaluation.py
│
├── data/
│   └── original/
│
└── results/
    └── .gitkeep
```

### File and Directory Descriptions

| File or Directory | Description |
|---|---|
| `app.py` | Implements the Streamlit dashboard, interactive controls, image comparisons, and metric displays. |
| `requirements.txt` | Lists the Python libraries required by the project. |
| `src/image_degradation.py` | Implements Gaussian noise, Gaussian blur, and JPEG compression functions. |
| `src/metrics.py` | Implements MSE and PSNR calculations. |
| `src/evaluation.py` | Coordinates image degradation, metric calculations, and experimental result collection. |
| `src/__init__.py` | Marks the `src` directory as a Python package. |
| `data/original/` | Stores the original images used as reference inputs. |
| `results/` | Stores generated experimental outputs, such as CSV files and figures. |

Processed images will normally be generated in memory rather than stored permanently. They can be saved when needed for further analysis.

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version.
- Git.
- A local copy of this repository.

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/image-quality-evaluation-mse-psnr.git
cd image-quality-evaluation-mse-psnr
```

Replace `YOUR_USERNAME` with the GitHub account that owns the repository.

### Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt)**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use Command Prompt or follow your system's approved PowerShell execution policy.

### Install Dependencies

After activating the virtual environment, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 8. Running the Dashboard

After implementing the dashboard and its supporting modules, run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL that can be opened in a web browser.

## 9. Experimental Workflow

The planned experimental workflow is:

1. Load an original image.
2. Select a degradation method.
3. Adjust the method's parameters.
4. Generate the processed image.
5. Calculate MSE and PSNR against the original image.
6. Compare the images and numerical results.
7. Repeat the experiment with different parameter values.
8. Analyze and export the results.

## 10. Expected Outcomes

The project is expected to produce:

- A set of reusable Python functions for image degradation.
- MSE and PSNR calculations for image quality evaluation.
- An interactive dashboard for visual and numerical comparison.
- Experimental tables and plots showing how degradation parameters affect the metrics.
- Findings that explain the strengths and limitations of MSE and PSNR when evaluating image quality.

## 11. Project Scope and Limitations

MSE and PSNR measure pixel-level differences and do not always correspond perfectly to perceived visual quality. Two images with similar metric values may appear different to a human observer.

The project will therefore consider both numerical measurements and visual comparisons when interpreting results. The experiments will focus on the selected degradation methods and will not attempt to cover every possible image distortion or perceptual quality metric.

## 12. Team Development

The project is organized into separate modules to support parallel development and integration:

- **Image Degradation:** Implements the degradation algorithms and their adjustable parameters.
- **Image Quality Metrics:** Implements MSE and PSNR.
- **Evaluation and Experiment Management:** Coordinates experiments and collects results.
- **Dashboard Development:** Integrates the modules into an interactive Streamlit interface.

The modules will be integrated and evaluated together to ensure consistent inputs, outputs, and experimental results.

---

*This project is developed as an academic study of image degradation and quantitative image quality evaluation.*