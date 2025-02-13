from ultralytics import YOLO
import os


current_path = os.path.abspath("")
model_path = os.path.join(
    current_path, "runs-20250213T014647Z-001/runs/detect/train/weights/best.pt"
)
# load trained model
model = YOLO(model_path)

from PIL import Image, ImageDraw, ImageFont


def draw_boxes_on_image(image_path):
    image = Image.open(image_path)

    results = model(image)
    predictions = results[0].boxes.data.tolist()

    label_names = ["CORD", "PASSPORT COVER"]
    colors = ["orange", "blue"]

    draw = ImageDraw.Draw(image)
    font_path = "Inter_18pt-Medium.ttf"
    font = ImageFont.truetype(font_path, size=16)

    for prediction in predictions:
        x1, y1, x2, y2, confidence, label = prediction
        label = int(label)
        draw.rectangle([(x1, y1), (x2, y2)], outline=colors[label], width=5)

        text = f"{label_names[label]} ({confidence:.3f})"
        text_bbox = draw.textbbox((x1, y1), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = x1 + 5
        text_y = y1 + 5
        draw.rectangle(
            [(text_x, text_y), (text_x + text_width, text_y + text_height)],
            fill=colors[label],
        )
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

    return image


if __name__ == "__main__":
    image_prove_path = os.path.join(current_path, "image_as_prove", "prove1.jpg")
    image_with_boxes = draw_boxes_on_image(image_path=image_prove_path)
    image_with_boxes.show()
