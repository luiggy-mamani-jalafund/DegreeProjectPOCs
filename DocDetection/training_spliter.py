import os
import random
import shutil


asb_path = os.path.abspath("")
data_path = os.path.join(asb_path, "data")


def split_dataset(images_folder, labels_folder, train_ratio=0.8):
    """
    Split the data into train and validation sets supporting multiple image extensions.

    Args:
    - images_folder: Path to the folder containing image files
    - labels_folder: Path to the folder containing corresponding label files
    - train_ratio: Proportion of data to use for training (default 0.8 or 80%)
    """
    # Supported image extensions
    image_extensions = [".png", ".jpg", ".jpeg"]

    train_images_folder = os.path.join(data_path, "train/images")
    train_labels_folder = os.path.join(data_path, "train/labels")
    val_images_folder = os.path.join(data_path, "val/images")
    val_labels_folder = os.path.join(data_path, "val/labels")

    # Create directories
    os.makedirs(train_images_folder, exist_ok=True)
    os.makedirs(train_labels_folder, exist_ok=True)
    os.makedirs(val_images_folder, exist_ok=True)
    os.makedirs(val_labels_folder, exist_ok=True)

    # Collect all image files with supported extensions
    image_files = []
    for filename in os.listdir(images_folder):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            image_files.append(filename)

    # Shuffle the image files
    random.shuffle(image_files)

    # Split the list
    num_images = len(image_files)
    num_train = int(num_images * train_ratio)
    train_image_files = image_files[:num_train]
    val_image_files = image_files[num_train:]

    # Move training files
    for image_file in train_image_files:
        # Find the corresponding label file (works with different image extensions)
        base_name = os.path.splitext(image_file)[0]
        label_file = base_name + ".txt"

        # Move image
        shutil.move(
            os.path.join(images_folder, image_file),
            os.path.join(train_images_folder, image_file),
        )

        # Move label (if it exists)
        if os.path.exists(os.path.join(labels_folder, label_file)):
            shutil.move(
                os.path.join(labels_folder, label_file),
                os.path.join(train_labels_folder, label_file),
            )
        else:
            print(f"Warning: No label found for {image_file}")

    # Move validation files
    for image_file in val_image_files:
        # Find the corresponding label file
        base_name = os.path.splitext(image_file)[0]
        label_file = base_name + ".txt"

        # Move image
        shutil.move(
            os.path.join(images_folder, image_file),
            os.path.join(val_images_folder, image_file),
        )

        # Move label (if it exists)
        if os.path.exists(os.path.join(labels_folder, label_file)):
            shutil.move(
                os.path.join(labels_folder, label_file),
                os.path.join(val_labels_folder, label_file),
            )
        else:
            print(f"Warning: No label found for {image_file}")

    print(f"Dataset split completed. Total images: {num_images}")
    print(f"Training images: {len(train_image_files)}")
    print(f"Validation images: {len(val_image_files)}")


if __name__ == "__main__":
    images_path = os.path.join(data_path, "/images")
    labels_path = os.path.join(data_path, "/labels")
    split_dataset(images_folder=images_path, labels_folder=labels_path, train_ratio=0.9)
