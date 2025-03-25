from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as transforms


def figure_cropping(infile, outfile):
    """
    Crops the input image and saves the cropped version to an output file.

    Args:
        infile (str): Path to the input image file.
        outfile (str): Path to save the cropped image.

    Returns:
        PIL.Image: The cropped image.
    """
    # Load the image using PIL
    print(f"Processing {infile}, saving to {outfile}")
    image = Image.open(infile)

    # Convert the image to a NumPy array (RGB or Grayscale based on the input image)
    image_np = np.array(image)
    print(f"Original image shape: {image_np.shape}")

    # Define the crop coordinates (you can adjust these values as needed)
    top = 96
    bottom = 712
    left = 102
    right = 719

    # Crop the image using NumPy slicing
    cropped_image = image_np[top:bottom, left:right]
    print(f"Cropped image shape: {cropped_image.shape}")

    # Convert the cropped NumPy array back to a PIL Image
    cropped_image_pil = Image.fromarray(cropped_image)

    # Save the cropped image to a PNG file
    cropped_image_pil.save(outfile, format="PNG")

    return cropped_image_pil


# Define the transformation pipeline for figure_trans function
img_trans = transforms.Compose(
    [
        transforms.ToTensor(),  # Converts the image to a tensor (C, H, W)
        transforms.Grayscale(
            num_output_channels=1
        ),  # Convert to grayscale with 1 channel
    ]
)


def figure_trans(infile):
    """
    Transforms the input image to tensor, then slices it into smaller patches,
    displays them in a grid, and saves the grid as a PNG file.

    Args:
        infile (str): Path to the input image file.

    Returns:
        list: A list of tensors representing the cropped image patches.
    """
    # Load the image
    image = Image.open(infile)

    # Check if the image has an alpha channel (RGBA)
    if image.mode == "RGBA":
        # Convert RGBA to RGB by removing the alpha channel
        image = image.convert("RGB")

    # Apply the transformation to the image
    img_tensor = img_trans(image)
    print(
        f"Transformed image shape: {img_tensor.shape}"
    )  # Should be (1, height, width)

    # Initialize the grid dimensions for the display
    num_rows, num_cols = 8, 8
    figure_list = []

    # Create a figure to display all cropped images in a grid (8x8)
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 10))

    for i in range(num_rows):
        for j in range(num_cols):
            # Slice the image tensor into smaller patches (77x77)
            cropped_img = img_tensor[:, i * 77 : (i + 1) * 77, j * 77 : (j + 1) * 77]
            figure_list.append(cropped_img)

            # Convert the tensor slice back to a PIL Image for visualization
            cropped_img_pil = transforms.ToPILImage()(cropped_img)

            # Plot the cropped image using Matplotlib
            ax = axes[i, j]
            ax.imshow(cropped_img_pil, cmap="gray")  # Display in grayscale
            ax.axis("off")  # Hide axes for better visualization

    # Adjust layout and save the grid of images as a PNG file
    plt.tight_layout()
    plt.savefig(infile, format="PNG")
    plt.close()  # Close the figure to free memory

    return figure_list
