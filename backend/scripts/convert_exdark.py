import os
import shutil
from sklearn.model_selection import train_test_split

# class mapping
CLASSES = ["Bicycle", "Boat", "Bottle", "Bus", "Car", "Cat",
           "Chair", "Cup", "Dog", "Motorbike", "People", "Table"]

def convert_annotation(label_path, img_width, img_height):
    # ExDark form -> YOLO form
    yolo_labels = []

    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("%") or not line:
            continue
        
        parts = line.split()
        class_name = parts[0]

        if class_name not in CLASSES:
            continue

        class_id = CLASSES.index(class_name)
        x = int(parts[1])
        y = int(parts[2])
        w = int(parts[3])
        h = int(parts[4])

        # YOLO form (regularization)
        x_center = (x + w / 2) / img_width
        y_center = (y + h / 2) / img_height
        width = w / img_width
        height = h / img_height

        yolo_labels.append(f"{class_id} {x_center} {y_center} {width} {height}")

    return yolo_labels

def get_image_size(img_path):
    # 이미지 크기 가져옴
    from PIL import Image
    with Image.open(img_path) as img:
        return img.size # (width, height)
    
def main():
    base_dir = "datasets/exdark"
    images_dir = f"{base_dir}/images"
    labels_dir = f"{base_dir}/labels"

    # output directory
    output_dir = f"{base_dir}/yolo"
    os.makedirs(f"{output_dir}/images/train", exist_ok=True)
    os.makedirs(f"{output_dir}/images/val", exist_ok=True)
    os.makedirs(f"{output_dir}/labels/train", exist_ok=True)
    os.makedirs(f"{output_dir}/labels/val", exist_ok=True)

    # 모든 이미지 수집
    all_images = []
    for class_name in CLASSES:
        class_img_dir = f"{images_dir}/{class_name}"
        if os.path.exists(class_img_dir):
            for img_file in os.listdir(class_img_dir):
                if img_file.lower().endswith((".jpg", ".png", ".jpeg")):
                    all_images.append((class_name, img_file))

    # Train/val split (80/20)
    train_images, val_images = train_test_split(all_images, test_size=0.2, random_state=42)
    
    print(f"Train: {len(train_images)}, Val: {len(val_images)}")

    # 변환 및 복사
    for split, images in [("train", train_images), ("val", val_images)]:
        for class_name, img_file in images:
            img_path = f"{images_dir}/{class_name}/{img_file}"
            label_path = f"{labels_dir}/{class_name}/{img_file}.txt"

            if not os.path.exists(label_path):
                continue
            
            # 이미지 크기
            try:
                img_width, img_height = get_image_size(img_path)
            except:
                continue

            # label 변환
            yolo_labels = convert_annotation(label_path, img_width, img_height)

            if not yolo_labels:
                continue

            # 파일명 (중복 방지용)
            new_name = f"{class_name}_{img_file}"

            # 이미지 복사
            shutil.copy(img_path, f"{output_dir}/images/{split}/{new_name}")

            # 라벨 저장
            label_name = new_name.rsplit(".", 1)[0] + ".txt"
            with open(f"{output_dir}/labels/{split}/{label_name}", "w") as f:
                f.write("\n".join(yolo_labels))

        # YAML 파일 생성
    yaml_content = f"""path: {os.path.abspath(output_dir)}
train: images/train
val: images/val

names:
  0: Bicycle
  1: Boat
  2: Bottle
  3: Bus
  4: Car
  5: Cat
  6: Chair
  7: Cup
  8: Dog
  9: Motorbike
  10: People
  11: Table
"""

    with open(f"{output_dir}/exdark.yaml", "w") as f:
        f.write(yaml_content)
    
    print("변환 완료")

if __name__ == "__main__":
    main()
