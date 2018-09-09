# larxiver
larxiver is a tiny script to compress latex projects by downscaling images. It keeps the original directory structure and is intended to ease the publishing process. Archives generated with this script can be uploaded to [arxiv](https://arxiv.org/) directly.

## Example usage

```Bash
./larxiver.py -i /path/to/paper.tex -o /path/to/output/arxiv
```

## Parameters

* **-i**: Input latex file
* **-o**: Output zip file
* **-r**: Target DPI, *(optional, default 300)*
* **-k**: Keep temporary files *(optional)*
* **-v**: Verbose output *(optional)*
* **-vv**: Very verbose output *(optional)*

## Dependencies

* pdflatex
* python3
* [pillow](https://pypi.org/project/Pillow/)

## Method

larxiver analyzes the log file of pdflatex and records all input files and the used size of image files. Input files are copied to a temporary output directory, which is later zipped; and images are scaled to produce a given DPI in this process.

## Compressing PDF files

larxiver is useful because it keeps your latex structure. If this is not required and the goal is to compress a PDF file, you could use Ghostscript instead:
```Bash
# If your pdf contains uncompressed images, say PNGs, this will convert them to JPG and reduce the file size significantly
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dDownsampleColorImages=false -dNOPAUSE -dBATCH -sOutputFile=paper_web.pdf paper.pdf

# If you want to adjust the resolution too
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dDownsampleColorImages=true -dColorImageResolution=150 -dNOPAUSE -dBATCH -sOutputFile=paper_web.pdf paper.pdf
```

Note, however, that larxiver can produce better results in some cases as it is not converting images to JPG and therefore not introducing compression artifacts.


## Related projects
* https://github.com/jopasserat/prepare-latex-hal-arxiv.sh
* https://github.com/lukeolson/clean-latex-to-arxiv
* https://github.com/floriangeigl/arxiv_converter
* https://github.com/jm-cc/arxivify
