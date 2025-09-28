# https://huggingface.co/egis-group/LayoutDetection

import numpy as np
import os
from pathlib import Path
try:
    from ultralytics import YOLO
except:
    os.system('pip install ultralytics')
    from ultralytics import YOLO

from .baseModel import base_module
from pdflayoutai.utils.utils import safe_download


def attempt_download(weight):
    name = Path(weight).stem
    if name in ["yolov8l_doc","yolov8s_doc","yolov8n_doc"] :
        url = f"https://github.com/pleb631/PdfDet/releases/download/v0.0.1/{name}.onnx"
    elif name in ["yolov8m_cdla","yolov8n_cdla"]:
        url = f"https://github.com/pleb631/PdfDet/releases/download/v0.0.1/{name}.pt"
    else:
        raise ValueError()
    safe_download(file=weight, url=url)


class yolov8(base_module):
    def __init__(self, model_type="yolov8l_doc",*args,**kwargs) -> None:
        if model_type in ["yolov8l_doc","yolov8s_doc","yolov8n_doc"] :
            weight = os.path.join(os.path.dirname(__file__), "weights",model_type+'.onnx')
        else:
            weight = os.path.join(os.path.dirname(__file__), "weights",model_type+'.pt')
        attempt_download(weight)
        
        # Initialize YOLO model
        self.model = YOLO(weight)
        
        if model_type.split('_')[-1]=='doc':
            self.labels = {
                0: "Caption",
                1: "Footnote",
                2: "Formula",
                3: "List-item",
                4: "Page-footer",
                5: "Page-header",
                6: "Picture",
                7: "Section-header",
                8: "Table",
                9: "Text",
                10: "Title",
            }
        else:
            self.labels = {0: 'Header', 1: 'Text', 2: 'Reference', 3: 'Figure caption', 4: 'Figure', 5: 'Table caption', 6: 'Table', 7: 'Title', 8: 'Footer', 9: 'Equation'}

    def predict(self, image=None, path=None, *args, **kwargs):
        assert path is not None or image is not None
        if path is not None:
            image = self.imread(path)
        elif not isinstance(image, np.ndarray):
            raise NotImplementedError

        # Use YOLO predict
        results = self.model.predict(image, verbose=False)
        
        result = []
        if results and len(results) > 0:
            # Get the first result (since we're processing one image)
            pred = results[0]
            
            if pred.boxes is not None and len(pred.boxes) > 0:
                boxes = pred.boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
                scores = pred.boxes.conf.cpu().numpy()  # confidence scores
                classes = pred.boxes.cls.cpu().numpy()  # class indices
                
                for i, (box, score, cls) in enumerate(zip(boxes, scores, classes)):
                    b = {
                        "type": self.labels[int(cls)],
                        "box": box.tolist(),
                        "score": float(score),
                    }
                    result.append(b)

        return (result, image)
