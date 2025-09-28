#!/usr/bin/env python3
"""
PDFLayoutAI CLI - Command Line Interface
Created by: yxshee
"""

import argparse
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdflayoutai import uni_model
from pdflayoutai.utils import Layer, Document
import fitz


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PDFLayoutAI - AI-powered PDF layout detection and annotation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdflayoutai document.pdf                    # Basic usage
  pdflayoutai document.pdf -o output.pdf      # Specify output
  pdflayoutai document.pdf -m yolov8n_cdla    # Use different model
        """
    )
    
    parser.add_argument(
        "input",
        help="Input PDF file path"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output annotated PDF file path (default: input_annotated.pdf)"
    )
    
    parser.add_argument(
        "-m", "--model",
        default="yolov8m_cdla",
        choices=["yolov8m_cdla", "yolov8n_cdla", "yolov8l_doc", "yolov8s_doc", "yolov8n_doc"],
        help="Model to use for detection (default: yolov8m_cdla)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="PDFLayoutAI 1.0.0 by yxshee"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)
    
    # Generate output filename if not provided
    if args.output is None:
        input_path = Path(args.input)
        args.output = str(input_path.parent / f"{input_path.stem}_annotated{input_path.suffix}")
    
    try:
        print(f"🚀 PDFLayoutAI - Starting processing...")
        print(f"📄 Input: {args.input}")
        print(f"🎯 Model: {args.model}")
        print(f"💾 Output: {args.output}")
        
        # Load model
        if args.verbose:
            print(f"🤖 Loading model: {args.model}")
        model = uni_model(name=args.model)
        
        # Process PDF
        if args.verbose:
            print(f"🔍 Processing PDF...")
        doc_result = model(path=args.input)
        
        # Count detections
        total_detections = 0
        if isinstance(doc_result, Document):
            for layer_name in doc_result.layers:
                layer = getattr(doc_result, layer_name)
                detections_data = layer.to_json()
                total_detections += len(detections_data["boxes"])
        else:
            detections_data = doc_result.to_json()
            total_detections = len(detections_data["boxes"])
        
        print(f"✅ Processing complete!")
        print(f"📊 Total detections: {total_detections}")
        print(f"💾 Annotated PDF saved: {args.output}")
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
