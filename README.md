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

## Related projects
* https://github.com/jopasserat/prepare-latex-hal-arxiv.sh
* https://github.com/lukeolson/clean-latex-to-arxiv
* https://github.com/floriangeigl/arxiv_converter
* https://github.com/jm-cc/arxivify
