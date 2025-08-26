# PDFLayoutAI

> **AI-powered PDF layout detection and annotation tool**

Created by: **yxshee**

## 🚀 Overview

PDFLayoutAI is a state-of-the-art tool that uses artificial intelligence to automatically detect and annotate layout elements in PDF documents. It can identify various document components like headers, tables, figures, text blocks, and more with high accuracy.

![PDFLayoutAI Demo](https://img.shields.io/badge/PDF-Layout%20Detection-blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **🎯 High Accuracy**: Uses YOLOv8 models with 94%+ precision
- **📄 Multi-page Support**: Process entire PDF documents at once
- **🏷️ Rich Annotations**: Color-coded bounding boxes with confidence scores
- **🔧 Easy to Use**: Simple command-line interface
- **⚡ Fast Processing**: Efficient AI models for quick results
- **🎨 Visual Output**: Annotated PDFs with clear layout detection

## 🔍 Detected Elements

PDFLayoutAI can identify the following layout elements:

| Element | Description | Color |
|---------|-------------|-------|
| **Header** | Page headers | Deep Pink |
| **Text** | Main text content | Dark Green |
| **Title** | Section titles and headings | Deep Pink |
| **Table** | Data tables | Gray |
| **Figure** | Images, charts, diagrams | Purple |
| **Reference** | Bibliography sections | Orange |
| **Footer** | Page footers | Magenta |
| **Equation** | Mathematical equations | Blue |
| **Figure caption** | Captions for figures | Red |
| **Table caption** | Captions for tables | Green |

## 🛠️ Installation

### Requirements
- Python 3.8 or higher
- PyTorch
- OpenCV

### Install from source

```bash
git clone https://github.com/yxshee/pdflayoutai.git
cd pdflayoutai
pip install -r requirements.txt
pip install .
```

## 📖 Usage

### Command Line Interface

```bash
# Basic usage
python generate_annotated_pdf.py --input document.pdf

# Specify output file
python generate_annotated_pdf.py --input document.pdf --output annotated_document.pdf

# Choose different model
python generate_annotated_pdf.py --input document.pdf --model yolov8m_cdla
```

### Python API

```python
from pdflayoutai import uni_model

# Load model
model = uni_model(name='yolov8m_cdla')

# Process PDF
doc = model(path="document.pdf")

# Get results
layers = sorted(doc.layers, key=lambda x: int(x))
for layer_name in layers:
    layer = getattr(doc, layer_name)
    detections = layer.to_json()
    print(f"Page {int(layer_name)+1}: {len(detections['boxes'])} detections")
```

## 🎯 Model Performance

| Model | MAP50 | MAP50:95 | Precision | Recall |
|-------|-------|----------|-----------|--------|
| **yolov8m_cdla** | 94.36% | 80.86% | 94.49% | 89.80% |
| **yolov8n_cdla** | - | - | - | - |

## 🔧 Configuration

### Available Models

- `yolov8m_cdla`: Medium model trained on CDLA dataset (recommended)
- `yolov8n_cdla`: Nano model for faster processing
- `yolov8l_doc`: Large model for DocLayNet dataset
- `yolov8s_doc`: Small model for DocLayNet dataset
- `yolov8n_doc`: Nano model for DocLayNet dataset

### Output Formats

The tool generates:
- **Annotated PDF**: Original PDF with colored bounding boxes and labels
- **JSON data**: Structured detection results with coordinates and confidence scores
- **Processing summary**: Detailed report of detection results

## 📊 Examples

### Input vs Output

Before processing:
- Standard PDF document

After processing:
- ✅ All layout elements detected and annotated
- ✅ Color-coded bounding boxes
- ✅ Confidence scores for each detection
- ✅ Clickable annotations with detailed information

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**yxshee**
- GitHub: [@yxshee](https://github.com/yxshee)

## 🙏 Acknowledgments

- Built with [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- Inspired by advances in computer vision and document AI
- Thanks to the open-source community for their contributions

## 📈 Roadmap

- [ ] Add support for more document formats
- [ ] Implement real-time processing
- [ ] Add web interface
- [ ] Mobile app development
- [ ] Custom model training interface

---

⭐ **Star this repository if you find it helpful!**
