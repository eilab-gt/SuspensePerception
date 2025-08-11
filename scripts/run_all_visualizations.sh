#!/bin/bash
# Run all visualization scripts for the SuspensePerception project

echo "================================================"
echo "Running All SuspensePerception Visualizations"
echo "================================================"
echo ""

# Clean old results
echo "Cleaning old results..."
rm -rf scripts/analysis_results/*
echo ""

# Run Brewer visualizations
echo "1. Running Brewer experiment visualizations..."
echo "------------------------------------------------"
uv run python scripts/data_processing/brewer_visualizations.py
echo ""

# Run Gerrig visualization
echo "2. Running Gerrig experiment visualization..."
echo "------------------------------------------------"
uv run python scripts/data_processing/gerrig_visualizations.py
echo ""

# Run Lehne visualization
echo "3. Running Lehne experiment visualization..."
echo "------------------------------------------------"
uv run python scripts/data_processing/lehne_delatorre_visualizations.py --experiment lehne
echo ""

# Run Delatorre visualization
echo "4. Running Delatorre experiment visualization..."
echo "------------------------------------------------"
uv run python scripts/data_processing/lehne_delatorre_visualizations.py --experiment delatorre
echo ""

# Summary
echo "================================================"
echo "Visualization Summary"
echo "================================================"
echo ""
echo "Generated files:"
find scripts/analysis_results -name "*.png" -type f | while read file; do
    size=$(ls -lh "$file" | awk '{print $5}')
    echo "  - $file ($size)"
done
echo ""
echo "Total files generated: $(find scripts/analysis_results -name "*.png" -type f | wc -l)"
echo "Total size: $(du -sh scripts/analysis_results | cut -f1)"
echo ""
echo "Visualization generation complete!"