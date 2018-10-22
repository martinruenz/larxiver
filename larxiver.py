#!/usr/bin/env python3
import argparse
import tempfile
import subprocess
import os
import re
import shutil
from PIL import Image

image_extensions = ['.png', '.jpg']
ignore_extensions = ['.out', '.aux']

parser = argparse.ArgumentParser()
parser.add_argument("-i", required=True, help="Input latex file")
parser.add_argument("-o", required=True, help="Output zip file")
parser.add_argument("-r", required=False, default=300, type=int, help="Target DPI")
parser.add_argument("-v", required=False, help="Verbose output", action='store_true')
parser.add_argument("-vv", required=False, help="Very verbose output", action='store_true')
parser.add_argument("-k", required=False, help="Keep temporary files", action='store_true')
args = parser.parse_args()
verbose = args.v or args.vv

input_file = os.path.abspath(os.path.expanduser(args.i))
input_dir = os.path.dirname(input_file)
basename_root, basename_ext = os.path.splitext(os.path.basename(input_file))
tmp_dir = tempfile.mkdtemp()
tmp_filepath = os.path.join(tmp_dir, basename_root)
output_dir = os.path.join(tmp_dir, "structure")
os.mkdir(output_dir)
output_file = os.path.abspath(os.path.expanduser(args.o))
print("Using temporary directory:", tmp_dir)

print("Generating fls file...")
subprocess.run(args=['pdflatex', '-interaction', 'nonstopmode', '-recorder', '-output-directory', tmp_dir, input_file],
               cwd=input_dir,
               stdout=None if args.vv else subprocess.DEVNULL,
               check=True)

print("Parsing fls...")
with open(os.path.join(tmp_dir, basename_root + ".fls"), 'r') as fls_file:
    fls_lines = fls_file.readlines()
    fls_lines = [l.split() for l in fls_lines]
    fls_lines = [l[1] for l in fls_lines if l[0]=='INPUT']
    input_files = [f for f in fls_lines if os.path.exists(os.path.abspath(os.path.join(input_dir, f)))]

print("Parsing log...")
image_use_re = re.compile('<use (?P<file>.*)>\n(.*\n)?.*\n.*Requested size: [+-]?(?P<x>(\d+\.?\d*)|(\.\d+))pt x [+-]?(?P<y>(\d+\.?\d*)|(\.\d+))pt.')
with open(os.path.join(tmp_dir, basename_root + ".log"), 'r', encoding="latin-1") as log_file:
    log = log_file.read()
    image_infos = []
    for m in image_use_re.finditer(log):
        if m is not None and os.path.splitext(m.group('file'))[1].lower() in image_extensions:
            image_infos.append({'file': m.group('file'),
                                'pt_x': float(m.group('x')),
                                'pt_y': float(m.group('y'))
                                })

# Scale and store images
print("Scaling images...")
for ii in image_infos:
    img_path_in = os.path.abspath(os.path.join(input_dir, ii['file']))
    img_path_out = os.path.abspath(os.path.join(output_dir, ii['file']))

    out_dir = os.path.dirname(img_path_out)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    if verbose:
        print("Scaling", img_path_in, "to", img_path_out)

    img = Image.open(img_path_in)
    w, h = img.size
    s = max(ii['pt_x'] / w, ii['pt_y'] / h)
    s = min(s * args.r / 72, 1)
    img.resize((int(s*w),int(s*h)), Image.LANCZOS).save(img_path_out)

    if args.vv:
        print("file:", ii['file'],
              "pt_x:", ii['pt_x'], "pt_y:", ii['pt_y'],
              "w:", w, "h:", h, "scale:", s)

print("Copy remaining files...")
for f in input_files:
    path_in = os.path.abspath(os.path.join(input_dir, f))
    path_out = os.path.abspath(os.path.join(output_dir, f))

    out_dir = os.path.dirname(path_out)
    ext = os.path.splitext(path_in)[1]
    if not os.path.exists(path_out) and not ext in ignore_extensions:
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        if verbose:
            print("Copying", path_in, "to", path_out)

        if ext in image_extensions:
            print("WARNING: Copying image file {} (without scaling). The regular expression probably failed!".format(path_in))

        shutil.copyfile(path_in, path_out)
    shutil.copyfile(input_file, os.path.join(output_dir, os.path.basename(input_file)))

print("Zipping files...")
if output_file.endswith('.zip'):
    # Remove extension .zip, as it will be added automatically
    output_file = output_file[:-4]
shutil.make_archive(output_file, 'zip', output_dir)

if not args.k:
    print("Cleanup temporary files...")
    shutil.rmtree(tmp_dir)
