# Scientific Heatmap Visualization Design System

## Executive Summary

This design system addresses the identified issues in current heatmap visualizations and establishes consistent, professional standards for academic publication quality. Based on analysis of existing implementations and scientific visualization best practices, this system provides comprehensive guidelines for color palettes, typography, grid specifications, and visual hierarchy.

## Current Issues Identified

1. **Grid Issues**: Thick white gridlines (1.2px) create visual distraction
2. **Cell Geometry**: Rectangular cells instead of square reduce readability  
3. **Color Inconsistency**: Mixed diverging (red-blue) and sequential (green-red) schemes
4. **Visual Noise**: Random colored borders around cells
5. **Typography Problems**: Oversized text (size 11) creates crowding
6. **Hierarchy Issues**: No clear visual distinction between baselines and models
7. **Design Fragmentation**: Different visual languages across experiments

## Design System Principles

### Core Philosophy
- **Clarity over decoration**: Minimize visual noise to highlight data patterns
- **Consistency**: Uniform visual language across all experiments
- **Accessibility**: Colorblind-friendly palettes ensuring 8%+ population inclusion
- **Professional standards**: Academic publication quality for Nature/Science/IEEE

### Visual Hierarchy
1. **Primary**: Data patterns and values
2. **Secondary**: Model/condition labels
3. **Tertiary**: Grid structure and annotations
4. **Quaternary**: Metadata and timestamps

## Color Palette Specifications

### Primary Palette: Sequential Data
**Recommended**: `viridis` (matplotlib) or `rocket` (seaborn)
- **Rationale**: Perceptually uniform, colorblind-safe, high contrast range
- **Usage**: Agreement scores, correlation matrices, performance metrics
- **Range**: 0.0 to 1.0 normalized values

```python
# Primary sequential palette
primary_cmap = "viridis"  # or sns.color_palette("rocket", as_cmap=True)
```

### Secondary Palette: Diverging Data
**Recommended**: `RdBu_r` (matplotlib) or `icefire` (seaborn)
- **Rationale**: Clear midpoint distinction, balanced contrast
- **Usage**: Deviation from baseline, difference scores
- **Center**: 0.5 or neutral reference point

```python
# Diverging palette for deviations
diverging_cmap = sns.diverging_palette(250, 10, s=80, l=55, as_cmap=True)
```

### Baseline Distinction Palette
**Human/Control baselines**: Distinct from model data
- **Baseline rows**: Custom colormap with separate visual treatment
- **Implementation**: Use mask or custom annotation styling

### Accent Colors
- **High Performance** (≥0.8): `#2ECC71` (green) - 2px border
- **Low Performance** (≤0.3): `#E74C3C` (red) - 2px border  
- **Separator Lines**: `#34495E` (dark blue-gray) - 3px width

## Typography Specifications

### Font System
**Primary**: Helvetica (Nature/Science standard)
**Fallback**: Arial, sans-serif
**Monospace**: Consolas (for data values)

### Size Hierarchy
- **Title**: 16pt, bold, 20px padding
- **Axis Labels**: 12pt, semibold
- **Tick Labels**: 9pt, regular
- **Annotations**: 8pt, semibold
- **Colorbar Labels**: 10pt, regular
- **Watermark**: 7pt, italic, 50% opacity

### Annotation Strategy
- **Value Display**: 2 decimal places maximum
- **Alignment**: Center both horizontally and vertically
- **Color**: High contrast against cell background
- **Weight**: Semibold for readability

## Grid and Layout Specifications

### Cell Specifications
- **Shape**: Perfect squares (`square=True`)
- **Size**: Consistent across all heatmaps
- **Aspect Ratio**: 1:1 maintained

### Grid System
- **Line Width**: 0.5px (subtle structure)
- **Line Color**: `white` (neutral separator)
- **Style**: Solid lines only

### Spacing and Padding
- **Cell Padding**: 0px (full utilization)
- **External Margins**: 15px minimum
- **Title Padding**: 20px top
- **Colorbar Shrink**: 0.8 (proportional sizing)

### Figure Dimensions
- **Standard**: 12×8 inches (landscape)
- **Compact**: 10×6 inches (presentations)
- **DPI**: 300 (publication quality)

## Visual Hierarchy Implementation

### Baseline Separation
- **Separator Line**: 3px dark line above baseline rows
- **Visual Weight**: Distinct treatment to emphasize reference data
- **Color Mapping**: Different colormap or masking for baseline rows

### Model Grouping
- **Consistent Ordering**: Alphabetical or performance-based
- **Label Shortening**: Standardized abbreviations (e.g., "GPT-4o" → "G-4o")
- **Vertical Alignment**: Consistent label positioning

### Experiment Labeling
- **Hierarchical**: Primary condition / Secondary variation
- **Multi-line**: Break long labels at logical points
- **Rotation**: 45° for readability when needed

## Colorbar and Legend Specifications

### Colorbar Design
- **Position**: Right side, shrink=0.8
- **Label**: Descriptive with units
- **Ticks**: 5-7 major ticks maximum
- **Font**: 10pt labels, 11pt title

### Legend Integration
- **Custom Elements**: Performance indicators, baseline markers
- **Positioning**: Non-overlapping with data
- **Styling**: Consistent with overall design

## Implementation Templates

### Matplotlib Configuration
```python
# Global style settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial'],
    'font.size': 9,
    'axes.labelsize': 12,
    'axes.titlesize': 16,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.facecolor': 'white'
})
```

### Seaborn Heatmap Template
```python
# Standard heatmap configuration
sns.heatmap(
    data,
    cmap='viridis',           # Primary colormap
    square=True,              # Perfect squares
    linewidths=0.5,           # Subtle grid
    linecolor='white',        # Neutral separators
    annot=True,              # Show values
    fmt='.2f',               # 2 decimal places
    annot_kws={
        'size': 8,
        'weight': 'semibold',
        'ha': 'center',
        'va': 'center'
    },
    cbar_kws={
        'shrink': 0.8,
        'label': 'Agreement Score'
    }
)
```

## Quality Assurance Checklist

### Pre-Publication Review
- [ ] Colorblind accessibility tested (Coblis/Color Oracle)
- [ ] Consistent color palette across all heatmaps
- [ ] Square cells maintained
- [ ] Readable typography at publication size
- [ ] Proper baseline visual separation
- [ ] Grid lines subtle and non-distracting
- [ ] High contrast annotations
- [ ] Professional axis labeling
- [ ] Appropriate figure dimensions
- [ ] DPI suitable for publication (300+)

### Cross-Experiment Consistency
- [ ] Same color palettes used
- [ ] Identical typography specifications
- [ ] Consistent model naming/abbreviations
- [ ] Uniform grid styling
- [ ] Standardized colorbar design

## Migration Strategy

### Phase 1: Template Implementation
1. Create standardized heatmap function
2. Define color palette constants
3. Implement typography settings

### Phase 2: Script Updates
1. Update Gerrig visualization script
2. Update Brewer visualization script  
3. Update Lehne-Delatorre visualization script

### Phase 3: Validation
1. Generate test visualizations
2. Colorblind accessibility testing
3. Publication format validation

## Technical Specifications

### File Output Standards
- **Format**: PNG (primary), SVG (vector backup)
- **Resolution**: 300 DPI minimum
- **Color Space**: sRGB
- **Compression**: Lossless

### Performance Considerations
- **Rendering Speed**: <5 seconds per heatmap
- **Memory Usage**: <500MB per visualization
- **Batch Processing**: Support for multiple experiments

This design system provides the foundation for professional, accessible, and consistent scientific heatmap visualizations that meet academic publication standards while addressing all identified usability issues.