import os
import PIL
import torch
from torchvision import transforms


def Image_transformer(img_path):
    data_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = PIL.Image.open(img_path)
    img = data_transforms(img)
    img = img.to('cpu')
    img = img.reshape(1, 3, 224, 224)
    return img


def Diagnosis(model_path, img_path):
    model_list = os.listdir(model_path)
    img = Image_transformer(img_path)
    pred_dic = {}
    for model in model_list:
        class_name = model.split("_")[0]
        model_fit = torch.load(model_path + '/' + model, map_location=torch.device('cpu'))
        _, pred = torch.max(model_fit(img), dim=1)
        if pred[0] == 0:
            pred_dic[class_name] = 0
        else:
            pred_dic[class_name] = 1
    result = []
    if 1 in pred_dic.values():
        if pred_dic["keratin"] == 1 and pred_dic["sebum"] == 1:
            result.append("지성")
            if pred_dic["sebum"] == 1 and pred_dic["erythema"] == 1:
                result.append("민감성")
                result.append("지루성")
                if pred_dic["pustule"] == 1:
                    result.append("염증성")
                if pred_dic["dandruff"] == 1:
                    result.append("비듬성")
                if pred_dic["alopecia"] == 1:
                    result.append("탈모성")
            else:
                if pred_dic["pustule"] == 1:
                    result.append("염증성")
                if pred_dic["dandruff"] == 1:
                    result.append("비듬성")
                if pred_dic["alopecia"] == 1:
                    result.append("탈모성")
        else:
            if pred_dic["sebum"] == 1 and pred_dic["erythema"] == 1:
                result.append("지성")
                result.append("민감성")
                result.append("지루성")
                if pred_dic["pustule"] == 1:
                    result.append("염증성")
                if pred_dic["dandruff"] == 1:
                    result.append("비듬성")
                if pred_dic["alopecia"] == 1:
                    result.append("탈모성")
            else:
                if pred_dic["keratin"] == 1:
                    result.append("건성")
                if pred_dic["sebum"] == 1:
                    result.append("지성")
                if pred_dic["erythema"] == 1:
                    result.append("민감성")
                if pred_dic["pustule"] == 1:
                    result.append("염증성")
                if pred_dic["dandruff"] == 1:
                    result.append("비듬성")
                if pred_dic["alopecia"] == 1:
                    result.append("탈모성")

    else:
        result.append("양호")
    return result