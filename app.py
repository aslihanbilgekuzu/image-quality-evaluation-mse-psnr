# Implements an interactive Streamlit dashboard for image quality evaluation.
# Displays original and processed images side by side.
# Provides sliders to select degradation methods and adjust their intensity.
# Displays MSE and PSNR metric cards and comparison charts.
# Integrates the image degradation, metrics, and evaluation modules.
# Updates images and metrics dynamically based on user inputs.

import streamlit as st
import numpy as np

from skimage import data
from skimage.color import gray2rgb
from skimage.util import img_as_ubyte

from src.image_degradation import (
    add_gaussian_noise,
    apply_gaussian_blur,
    apply_jpeg_compression,
)
from src.metrics import calculate_mse, calculate_psnr
from src.evaluation import run_evaluation


st.set_page_config(
    page_title="Image Quality Evaluation",
    page_icon="🖼️",
    layout="wide",
)

st.title("Image Quality Evaluation")
st.write(
    "Evaluate image degradation using MSE and PSNR metrics."
)

st.divider()


# Image preparation

def prepare_image(image):
    image = np.asarray(image)

    if image.ndim == 2:
        image = gray2rgb(image)

    if image.dtype != np.uint8:
        image = img_as_ubyte(image)

    return np.ascontiguousarray(image)


# Sample images from scikit-image

SAMPLE_IMAGES = {
    "Astronaut": data.astronaut,
    "Coffee": data.coffee,
    "Chelsea the Cat": data.chelsea,
    "Rocket": data.rocket,
    "Hubble Deep Field": data.hubble_deep_field,
    "Immunohistochemistry": data.immunohistochemistry,
}


@st.cache_data
def load_sample_image(name):
    return prepare_image(SAMPLE_IMAGES[name]())


# Sidebar controls

st.sidebar.header("Experiment Settings")

image_name = st.sidebar.selectbox(
    "Select a sample image",
    list(SAMPLE_IMAGES.keys()),
)

original_image = load_sample_image(image_name)

method_label = st.sidebar.selectbox(
    "Degradation Method",
    ["Gaussian Noise", "Gaussian Blur", "JPEG Compression"],
)

if method_label == "Gaussian Noise":
    method = "gaussian_noise"

    sigma = st.sidebar.slider(
        "Noise Intensity (Sigma)",
        min_value=0,
        max_value=80,
        value=20,
        step=5,
    )

    mean = st.sidebar.slider(
        "Noise Mean",
        min_value=-20,
        max_value=20,
        value=0,
    )

    parameters = {"mean": mean, "sigma": sigma}

elif method_label == "Gaussian Blur":
    method = "gaussian_blur"

    kernel_size = st.sidebar.select_slider(
        "Blur Kernel Size",
        options=[3, 5, 7, 9, 11, 15, 21],
        value=5,
    )

    sigma = st.sidebar.slider(
        "Blur Sigma",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
    )

    parameters = {
        "kernel_size": kernel_size,
        "sigma": sigma,
    }

else:
    method = "jpeg_compression"

    quality = st.sidebar.slider(
        "JPEG Quality",
        min_value=1,
        max_value=100,
        value=75,
    )

    parameters = {"quality": quality}


# Process the original image and calculate metrics

if method == "gaussian_noise":
    processed_image = add_gaussian_noise(
        original_image.copy(),
        **parameters,
    )

elif method == "gaussian_blur":
    processed_image = apply_gaussian_blur(
        original_image.copy(),
        **parameters,
    )

else:
    processed_image = apply_jpeg_compression(
        original_image.copy(),
        **parameters,
    )

mse_value = calculate_mse(original_image, processed_image)
psnr_value = calculate_psnr(original_image, processed_image)


# Original and processed images

st.subheader("Image Comparison")

original_column, processed_column = st.columns(2)

with original_column:
    st.markdown("**Original Image**")
    st.image(original_image, width="stretch")

with processed_column:
    st.markdown("**Processed Image**")
    st.image(processed_image, width="stretch")

st.caption(f"Selected method: {method_label} | Parameters: {parameters}")


# MSE and PSNR metric cards

st.divider()
st.subheader("Image Quality Metrics")

mse_column, psnr_column = st.columns(2)

with mse_column:
    st.metric("Mean Squared Error (MSE)", f"{mse_value:.2f}")

with psnr_column:
    psnr_display = (
        "∞ dB" if np.isinf(psnr_value) else f"{psnr_value:.2f} dB"
    )
    st.metric("Peak Signal-to-Noise Ratio (PSNR)", psnr_display)


# Comparison experiments and charts

st.divider()
st.subheader("Degradation Intensity Analysis")

if method == "gaussian_noise":
    experiments = [
        {"method": method, "parameters": {"mean": 0, "sigma": level}}
        for level in [5, 15, 30, 50]
    ]
    experiments.append({"method": method, "parameters": parameters.copy()})

elif method == "gaussian_blur":
    experiments = [
        {
            "method": method,
            "parameters": {"kernel_size": level, "sigma": 1.0},
        }
        for level in [3, 5, 7, 9]
    ]
    experiments.append({"method": method, "parameters": parameters.copy()})

else:
    experiments = [
        {"method": method, "parameters": {"quality": level}}
        for level in [90, 70, 40, 10]
    ]
    experiments.append({"method": method, "parameters": parameters.copy()})

results_df = run_evaluation(original_image, experiments)


def get_intensity_label(row):
    params = row["parameters"]

    if row["method"] == "gaussian_noise":
        return f"Sigma {params['sigma']}"

    if row["method"] == "gaussian_blur":
        return f"Kernel {params['kernel_size']}"

    return f"Quality {params['quality']}"


results_df["Intensity"] = results_df.apply(get_intensity_label, axis=1)

# Keep the table focused on metric results.
display_df = results_df[
    ["Intensity", "mse_value", "psnr_value"]
].rename(
    columns={
        "mse_value": "MSE",
        "psnr_value": "PSNR (dB)",
    }
)

st.dataframe(display_df, hide_index=True, width="stretch")

chart_column_1, chart_column_2 = st.columns(2)

with chart_column_1:
    st.markdown("**MSE Comparison**")
    st.line_chart(
        results_df.set_index("Intensity")[["mse_value"]].rename(
            columns={"mse_value": "MSE"}
        )
    )

with chart_column_2:
    st.markdown("**PSNR Comparison**")
    st.line_chart(
        results_df.set_index("Intensity")[["psnr_value"]].rename(
            columns={"psnr_value": "PSNR (dB)"}
        )
    )

st.caption(
    "Results update automatically when the image, degradation method, "
    "or intensity settings change."
)
