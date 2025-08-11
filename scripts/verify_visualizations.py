#!/usr/bin/env python3
"""
Verify all generated visualizations are valid and meet quality standards.
"""

import os
from pathlib import Path
from PIL import Image
import numpy as np

def verify_image(filepath):
    """Verify a single image file."""
    try:
        # Open and verify image
        img = Image.open(filepath)
        
        # Get image properties
        width, height = img.size
        mode = img.mode
        format = img.format
        
        # Convert to array to check content
        img_array = np.array(img)
        
        # Check if image has content (not all white/black)
        unique_pixels = len(np.unique(img_array))
        
        # Quality checks
        checks = {
            "Valid PNG": format == "PNG",
            "Good resolution": width >= 1000 and height >= 1000,
            "Has content": unique_pixels > 100,  # More than 100 unique pixel values
            "Proper mode": mode in ["RGB", "RGBA"],
            "File size OK": os.path.getsize(filepath) > 10000  # At least 10KB
        }
        
        return {
            "filepath": filepath,
            "width": width,
            "height": height,
            "mode": mode,
            "format": format,
            "unique_pixels": unique_pixels,
            "file_size": os.path.getsize(filepath),
            "checks": checks,
            "all_passed": all(checks.values())
        }
    except Exception as e:
        return {
            "filepath": filepath,
            "error": str(e),
            "all_passed": False
        }

def main():
    """Verify all visualizations."""
    print("=" * 60)
    print("Visualization Quality Verification")
    print("=" * 60)
    
    # Find all PNG files
    results_dir = Path(__file__).parent / "analysis_results"
    png_files = list(results_dir.glob("**/*.png"))
    
    if not png_files:
        print("No PNG files found in analysis_results!")
        return
    
    print(f"\nFound {len(png_files)} visualization files to verify\n")
    
    all_passed = True
    results = []
    
    for png_file in sorted(png_files):
        result = verify_image(png_file)
        results.append(result)
        
        # Print summary for each file
        rel_path = png_file.relative_to(results_dir)
        if result.get("error"):
            print(f"❌ {rel_path}: ERROR - {result['error']}")
            all_passed = False
        elif result["all_passed"]:
            print(f"✅ {rel_path}: {result['width']}x{result['height']}, {result['file_size']/1024:.1f}KB")
        else:
            print(f"⚠️  {rel_path}: Some checks failed")
            for check, passed in result["checks"].items():
                if not passed:
                    print(f"   - {check}: FAILED")
            all_passed = False
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    
    total_size = sum(r.get("file_size", 0) for r in results) / (1024 * 1024)
    valid_count = sum(1 for r in results if r.get("all_passed", False))
    
    print(f"Total files: {len(results)}")
    print(f"Valid files: {valid_count}/{len(results)}")
    print(f"Total size: {total_size:.2f} MB")
    
    # Group by experiment
    experiments = {}
    for result in results:
        if "error" not in result:
            exp_name = str(result["filepath"]).split("/")[-2]
            if exp_name not in experiments:
                experiments[exp_name] = []
            experiments[exp_name].append(result)
    
    print("\nBy Experiment:")
    for exp, exp_results in experiments.items():
        avg_width = np.mean([r["width"] for r in exp_results])
        avg_height = np.mean([r["height"] for r in exp_results])
        total_kb = sum(r["file_size"] for r in exp_results) / 1024
        print(f"  {exp}: {len(exp_results)} files, avg {avg_width:.0f}x{avg_height:.0f}, {total_kb:.1f}KB total")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All visualizations passed quality checks!")
    else:
        print("⚠️  Some visualizations need attention")
    print("=" * 60)

if __name__ == "__main__":
    main()