#!/usr/bin/env python3
"""
PDFLayoutAI - AI-powered PDF layout detection and annotation tool
Created by: yxshee
Description: Script to generate an annotated PDF with layout detection results using state-of-the-art AI models.
"""

import os
import cv2
import numpy as np
import fitz  # PyMuPDF
from pathlib import Path
import argparse

from pdflayoutai import uni_model
from pdflayoutai.utils import Layer, Document


def get_color_for_label(label_name):
    """Generate a consistent color for each label type (normalized to 0-1 for PyMuPDF)."""
    color_map = {
        # DocLayNet labels (yolov8l_doc)
        "Caption": (1.0, 0.0, 0.0),      # Red
        "Footnote": (0.0, 1.0, 0.0),    # Green  
        "Formula": (0.0, 0.0, 1.0),     # Blue
        "List-item": (1.0, 1.0, 0.0), # Yellow
        "Page-footer": (1.0, 0.0, 1.0), # Magenta
        "Page-header": (0.0, 1.0, 1.0), # Cyan
        "Picture": (0.5, 0.0, 0.5),   # Purple
        "Section-header": (1.0, 0.65, 0.0), # Orange
        "Table": (0.5, 0.5, 0.5),   # Gray
        "Text": (0.0, 0.5, 0.0),        # Dark Green
        "Title": (1.0, 0.08, 0.58),    # Deep Pink
        
        # CDLA labels (yolov8m_cdla)
        "Header": (1.0, 0.08, 0.58),   # Deep Pink
        "Reference": (1.0, 0.65, 0.0), # Orange
        "Figure caption": (1.0, 0.0, 0.0), # Red
        "Figure": (0.5, 0.0, 0.5),    # Purple
        "Table caption": (0.0, 1.0, 0.0), # Green
        "Footer": (1.0, 0.0, 1.0),    # Magenta
        "Equation": (0.0, 0.0, 1.0),    # Blue
    }
    return color_map.get(label_name, (0.0, 0.0, 0.0))  # Default to black


def draw_detections_on_page(page, detections, scale_factor=1.0):
    """Draw detection boxes and labels on a PDF page."""
    
    for detection in detections:
        box = detection["box"]
        # Handle both 'type' and 'label' keys
        label = detection.get("type", detection.get("label", "Unknown"))
        score = detection["score"]
        
        # Scale coordinates if needed
        x1, y1, x2, y2 = [int(coord * scale_factor) for coord in box]
        
        # Get color for this label type
        color = get_color_for_label(label)
        
        # Create annotation rectangle
        rect = fitz.Rect(x1, y1, x2, y2)
        
        # Add rectangle annotation
        annot = page.add_rect_annot(rect)
        annot.set_colors(stroke=color)
        annot.set_border(width=2)
        annot.update()
        
        # Add text annotation for label
        text_point = fitz.Point(x1, y1 - 5)
        text_rect = fitz.Rect(x1, y1 - 20, x1 + 150, y1)
        text_annot = page.add_text_annot(text_point, f"{label} ({score:.2f})")
        text_annot.set_info(title=label, content=f"Confidence: {score:.3f}")
        text_annot.update()


def process_pdf_with_annotations(pdf_path, output_path, model_name="yolov8l_doc"):
    """Process PDF with layout detection and create annotated output."""
    
    print(f"Loading model: {model_name}")
    model = uni_model(name=model_name)
    
    print(f"Processing PDF: {pdf_path}")
    doc_result = model(path=pdf_path)
    
    # Open the original PDF
    pdf_doc = fitz.open(pdf_path)
    
    if isinstance(doc_result, Layer):
        # Single page/image
        print("Processing single layer...")
        detections_data = doc_result.to_json()
        
        # Get the first (and only) page
        page = pdf_doc[0]
        draw_detections_on_page(page, detections_data["boxes"])
        
    elif isinstance(doc_result, Document):
        # Multi-page document
        print(f"Processing {len(doc_result.layers)} pages...")
        layers = sorted(doc_result.layers, key=lambda x: int(x))
        
        for i, layer_name in enumerate(layers):
            print(f"Processing page {i+1}/{len(layers)}")
            layer = getattr(doc_result, layer_name)
            detections_data = layer.to_json()
            
            # Get corresponding PDF page
            if i < len(pdf_doc):
                page = pdf_doc[i]
                draw_detections_on_page(page, detections_data["boxes"])
    
    # Save the annotated PDF
    print(f"Saving annotated PDF to: {output_path}")
    pdf_doc.save(output_path)
    pdf_doc.close()
    
    print("Done! Annotated PDF created successfully.")
    
    # Print summary
    if isinstance(doc_result, Document):
        total_detections = 0
        for layer_name in doc_result.layers:
            layer = getattr(doc_result, layer_name)
            detections_data = layer.to_json()
            page_detections = len(detections_data["boxes"])
            total_detections += page_detections
            print(f"Page {int(layer_name)+1}: {page_detections} detections")
        print(f"Total detections across all pages: {total_detections}")
    else:
        detections_data = doc_result.to_json()
        print(f"Total detections: {len(detections_data['boxes'])}")


def main():
    parser = argparse.ArgumentParser(description="Generate annotated PDF with layout detection")
    parser.add_argument(
        "--input", 
        type=str, 
        default="/Users/venom/Downloads/pdfLayoutDet-main/Workbook.pdf",
        help="Input PDF file path"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        help="Output annotated PDF file path (default: input_annotated.pdf)"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="yolov8l_doc",
        choices=["yolov8l_doc", "yolov8s_doc", "yolov8n_doc", "yolov8m_cdla", "yolov8n_cdla"],
        help="Model to use for detection"
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return
    
    # Generate output filename if not provided
    if args.output is None:
        input_path = Path(args.input)
        args.output = str(input_path.parent / f"{input_path.stem}_annotated{input_path.suffix}")
    
    # Process the PDF
    try:
        process_pdf_with_annotations(args.input, args.output, args.model)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
