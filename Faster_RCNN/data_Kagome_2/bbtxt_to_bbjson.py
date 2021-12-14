import glob
import os.path


def txttojson_image(txt_file, image_size=512, image_id=0, image_ext=".png"):
    json_text_image = ""
    json_text_image += "{\"file_name\": \""
    [path, name] = os.path.split(txt_file)
    [name, ext] = os.path.splitext(name)
    json_text_image += name
    json_text_image += image_ext
    json_text_image += "\", \"height\": "
    json_text_image += str(image_size)
    json_text_image += ", \"width\": "
    json_text_image += str(image_size)
    json_text_image += ", \"id\": "
    json_text_image += str(image_id)
    json_text_image += "}"

    return json_text_image


def txttojson_instance(txt_file, image_id=0, instance_id=0, image_size=512):
    txttojson_instance = ""

    with open(txt_file) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if i > 0:
            if i > 1:
                txttojson_instance += ", "
            line = line.split(",")
            x_min = int(float(line[2]))
            x_max = int(float(line[3]))
            y_min = int(float(line[4]))
            y_max = int(float(line[5]))
            chir = int(float(line[6]))
            if x_min < 0:
                x_min = 0
            if x_max > image_size:
                x_max = image_size
            if y_min < 0:
                y_min = 0
            if y_max > image_size:
                y_max = image_size
            if chir == -1:
                chir = 0
            txttojson_instance += "{\"area\": "
            txttojson_instance += str((x_max - x_min) * (y_max - y_min))
            txttojson_instance += ", \"iscrowd\": 0, \"image_id\": "
            txttojson_instance += str(image_id)
            txttojson_instance += ", \"bbox\": "
            txttojson_instance += f"[{x_min}, {x_max - x_min}, {y_min}, {y_max - y_min}]"
            txttojson_instance += ", \"category_id\": "
            txttojson_instance += str(chir)
            txttojson_instance += ", \"id\": "
            txttojson_instance += str(instance_id)
            instance_id += 1
            txttojson_instance += ", \"ignore\": 0, \"segmentation\": []}"

    return txttojson_instance, instance_id


def txttojson(txt_list, image_size=512):
    # Images part
    json_text = ""
    json_text += "{\"images\": ["
    for i, txt_file in enumerate(txt_list):
        if i > 0:
            json_text += ", "
        json_text += txttojson_image(txt_file, image_size=512, image_id=i)
    json_text += "]"

    # Instances
    json_text += ", \"type\": \"instances\", \"annotations\": ["
    instance_id = 0
    for i, txt_file in enumerate(txt_list):
        if i > 0:
            json_text += ", "
        [text, instance_id] = txttojson_instance(txt_file, image_id=i, instance_id=instance_id)
        json_text += text
    json_text += "]"

    # Classes
    json_text += ", \"categories\": [{\"supercategory\": \"none\", \"id\": 0, \"name\": \"L\"}, {\"supercategory\": \"none\", \"id\": 1, \"name\": \"R\"}]}"

    print(f"converted {len(txt_list)} files")
    return json_text


if __name__ == "__main__":
    # txt_list = [r"Label_bb_tri1.txt"]
    txt_list = glob.glob(r"F:\pycharm\Chiral-molecule-detection\Faster_RCNN\data_Kagome_2\tri_label\*")
    json_path = "0.json"
    image_size = 512

    json_text = txttojson(txt_list, image_size=image_size)

    # print(json_text)

    f = open(json_path, 'w')
    f.write(json_text)
