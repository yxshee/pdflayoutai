import importlib

name2func = {
    "cnstd_yolov7": "pdflayoutai.models.cnstdModel",
    "paddle_pub": "pdflayoutai.models.Paddle",
    "paddle_cdla": "pdflayoutai.models.Paddle",
    "yolov8": "pdflayoutai.models.yolov8",
}


def uni_model(name=None, *args, **kwargs):
    name = name.lower()
    if 'yolov8' in name:
        kwargs["model_type"]=name
        name = 'yolov8'
        
    module = importlib.import_module(name2func[name])
    model = getattr(module, name)(*args, **kwargs)

    return model
