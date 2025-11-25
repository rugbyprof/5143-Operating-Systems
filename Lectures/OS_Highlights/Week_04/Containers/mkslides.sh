#!/usr/bin/env bash
set -euo pipefail

# Optional: extra Marp options (theme, style, allow local files, etc.)
# Example: M      ARP_OPTS='--allow-local-files --theme ./themes/msu-theme.css'
MARP_OPTS=${MARP_OPTS:-}

# 1) Ensure output directories exist
mkdir -p slides pdfs

echo "Using marp options: ${MARP_OPTS}"
echo "Output directories: slides/ and pdfs/"
echo

# 2) Loop over markdown files starting with three digits
shopt -s nullglob
files=([0-9][0-9][0-9]*.md)

if [ ${#files[@]} -eq 0 ]; then
    echo "No files starting with three digits found (e.g., 001-intro.md)."
    exit 0
fi

for f in "${files[@]}"; do
    # Strip directory and extension: 001-intro.md -> 001-intro
    filename="$(basename -- "$f")"
    base="${filename%.*}"

    echo "Processing: $f"
    
    # 3a) Generate HTML slides
    marp $MARP_OPTS "$f" -o "slides/${base}.html"

    # 3b) Generate PDF slides
    marp $MARP_OPTS "$f" -o "pdfs/${base}.pdf"

    echo "  -> slides/${base}.html"
    echo "  -> pdfs/${base}.pdf"
    echo
done

echo "Done."