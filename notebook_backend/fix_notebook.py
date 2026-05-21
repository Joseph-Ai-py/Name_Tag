import json
import re

# Read the notebook
with open('BACKEND_FLOW_EXPLANATION.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

print(f'Total cells: {len(notebook["cells"])}')

# Process cells
changes = []
for cell_idx, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source_lines = cell['source']
        source_text = ''.join(source_lines) if isinstance(source_lines, list) else source_lines
        
        # Check if this cell contains create_brand_strategy_pdf function
        if 'create_brand_strategy_pdf' in source_text:
            print(f'Found create_brand_strategy_pdf in cell {cell_idx}')
            
        # Check if this cell contains XPos.STANDARD with pdf.cell
        if 'XPos.STANDARD' in source_text and 'pdf.cell' in source_text:
            print(f'Found XPos.STANDARD with pdf.cell in cell {cell_idx}')
            lines = source_text.split('\n')
            
            for i, line in enumerate(lines):
                if 'XPos.STANDARD' in line:
                    print(f'  Line {i}: {line.strip()[:100]}')
                    # Look for the specific pattern
                    if 'pdf.cell(5, 5, "' in line:
                        original_line = line
                        # Replace the pattern
                        new_line = re.sub(
                            r'pdf\.cell\(5, 5, "•", new_x=XPos\.STANDARD, new_y=YPos\.TOP\)',
                            'pdf.cell(5, 5, "•")',
                            line
                        )
                        
                        if new_line != original_line:
                            lines[i] = new_line
                            changes.append({
                                'cell': cell_idx,
                                'line': i,
                                'original': original_line.strip(),
                                'modified': new_line.strip()
                            })
                            print(f'    -> REPLACED')
            
            if len(changes) > 0:
                # Update the cell source
                cell['source'] = '\n'.join(lines)

print(f'\nFound and replaced {len(changes)} occurrence(s):\n')
for i, change in enumerate(changes, 1):
    print(f'Change {i} (Cell {change["cell"]}, Line {change["line"]}):')
    print(f'  FROM: {change["original"]}')
    print(f'  TO:   {change["modified"]}')
    print()

# Write back the notebook
if len(changes) > 0:
    with open('BACKEND_FLOW_EXPLANATION.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    print('Notebook updated.')
else:
    print('No changes made.')
