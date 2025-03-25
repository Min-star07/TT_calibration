import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from model import NET  # Assuming NET is your model class


def num_dis(figure):
    """
    Classifies a digit from the input figure (either a tensor or image file path).

    Args:
        figure (torch.Tensor or str): The input can be a tensor (shape [C, H, W] or [B, C, H, W]) or
                                      a string representing the file path to an image.

    Returns:
        tuple: (predicted_class_item, predicted_class_idx) where:
            - predicted_class_item: the digit label (e.g., '0', '1', ..., '9')
            - predicted_class_idx: the index of the predicted class (0-9)
    """
    # Class names corresponding to digits 0-9
    class_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # Load the pre-trained model
    load_model = NET()
    load_model.load_state_dict(torch.load("./model_minist/model_minist_99.pth"))
    load_model.eval()  # Set model to evaluation mode

    # Prepare the input image
    if isinstance(figure, torch.Tensor):
        # Ensure tensor is of shape [B, C, H, W] for batch size 1
        if figure.ndimension() == 3:  # If shape is [C, H, W]
            figure = figure.unsqueeze(0)  # Add batch dimension (1, C, H, W)
        elif figure.ndimension() != 4:  # Not a valid shape
            raise ValueError("Tensor must have 3 or 4 dimensions.")
        # Convert tensor to PIL image for further processing
        input_image = transforms.ToPILImage()(figure.squeeze(0))  # Convert to PIL image

    elif isinstance(figure, str):
        # If it's a file path, load the image
        try:
            input_image = Image.open(figure).convert("L")  # Convert to grayscale
        except FileNotFoundError:
            raise ValueError(f"Image file {figure} not found.")
    else:
        raise TypeError(
            "Input must be a tensor or a string representing an image file path."
        )

    # Define the transform to resize the image to 28x28
    resize_transform = transforms.Resize((28, 28))

    # Apply the transformation
    resized_image = resize_transform(input_image)

    # Convert back to tensor and add batch dimension
    img_tensor = transforms.ToTensor()(resized_image).unsqueeze(0)

    # Move model and image tensor to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    load_model.to(device)
    img_tensor = img_tensor.to(device)

    # Inference: Disable gradient computation during evaluation
    with torch.no_grad():
        output = load_model(img_tensor)  # Forward pass

        # Get the predicted class (index of max logit)
        _, predicted = torch.max(output, 1)
        predicted_class_idx = predicted.item()
        predicted_class_item = class_names[predicted_class_idx]

    return predicted_class_item, predicted_class_idx


# Example usage:
# tensor_input = torch.rand(1, 28, 28)  # Example tensor input with shape [1, 28, 28]
# print(num_dis(tensor_input))  # Call with tensor input
# print(num_dis("path_to_image.png"))  # Call with image file path
