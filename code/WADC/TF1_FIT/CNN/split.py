import matplotlib.pyplot as plt
import torchvision.transforms as transforms


def Figure_Split(figure):
    """
    Splits the input figure into two parts (left and right).

    Args:
        figure (tensor): The input image tensor with shape [C, H, W].

    Returns:
        Tuple: Two tensors representing the left and right halves of the input image.
    """
    # Get the height and width of the image
    height, width = figure.shape[1], figure.shape[2]

    # Split the image into two halves: left and right
    gain_left = figure[:, :, 0:37]  # Left part
    gain_right = figure[:, :, 39:77]  # Right part

    return gain_left, gain_right


def crop_image(image_tensor, crop_coords):
    """
    Crops a tensor image given crop coordinates.

    Args:
        image_tensor (tensor): The image tensor to crop.
        crop_coords (tuple): A tuple containing the top, bottom, left, and right cropping coordinates.

    Returns:
        tensor: The cropped image tensor.
    """
    top, bottom, left, right = crop_coords
    return image_tensor[:, top:bottom, left:right]


def read_data(figure):
    """
    Processes a batch of images, splits them, and applies cropping.

    Args:
        figure (tensor): A batch of images with shape [B, C, H, W], where B is the batch size,
                         C is the number of channels, H is height, and W is width.

    Returns:
        dict: A dictionary where keys are 'channel_<index>' and values are lists of cropped tensors.
    """
    gain_dict = {}

    # Process each image in the batch
    for i, item in enumerate(figure):
        gain_list = []

        # Split the image into left and right parts
        gain = Figure_Split(item)

        # Apply cropping to both left and right parts
        for j, gain_part in enumerate(gain):
            if j == 0:
                crop_coords = (25, 50, 20, 38)  # Coordinates for the left part
            else:
                crop_coords = (25, 45, 0, 15)  # Coordinates for the right part

            # Crop the image using the specified coordinates
            cropped_tensor = crop_image(gain_part, crop_coords)
            gain_list.append(cropped_tensor)

        # Store the cropped images in the dictionary
        gain_dict[f"channel_{i}"] = gain_list

    return gain_dict


# Example usage:
# Assume `figure` is a tensor with shape [B, C, H, W] where B is the batch size
# figure = torch.rand(10, 3, 100, 100)  # Example tensor with shape [B, C, H, W]
# gain_dict = read_data(figure)
