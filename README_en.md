# LYC Individual Recognition Project

## Project Overview
This is a deep learning-based fish individual recognition system implemented using the PaddlePaddle framework. The project includes a detection model (PP-YOLOv2) and a recognition model, capable of detecting and identifying individual fish in input images.

## Project Structure
```
LYC_Individual_recognition_demo/
├── configs/                  # Configuration files directory
│   └── inference.yaml       # Inference configuration file
├── dist/                     # Packaged executable files
│   ├── predict/             # Recognition program
│   └── process_result.exe   # Result processing program
├── scripts/                 # Script code
│   ├── predict.py           # Core recognition code
│   └── process_result.py    # Result processing code
├── images/                  # Test images directory
│   └── LYC/                # Test images
├── models/                  # Model files directory
│   ├── FL_100test/         # Model trained by excluding 100 individuals, using remaining data
│   ├── FL_100test_original/# Original model trained by excluding 100 individuals (unoptimized)
│   ├── FL_200test/         # Model trained by excluding 200 individuals, using remaining data
│   ├── FL_500test/         # Model trained by excluding 500 individuals, using remaining data
│   └── PP-YOLOv2_LYC/      # Detection model
├── recognition_gallery/     # Recognition gallery
│   └── gallery_LYC/       # Fish feature index library
├── output/                  # Output results directory
│   ├── FL_100test/         # Model output excluding 100 individuals
│   ├── FL_100test_original/# Original model output excluding 100 individuals
│   ├── FL_200test/         # Model output excluding 200 individuals
│   └── FL_500test/         # Model output excluding 500 individuals
├── predict_image_exe.bat    # Windows batch script (uses compiled program)
├── build_exe.bat            # Compilation script
├── requirements.txt         # Python dependencies list
├── predict.spec            # predict compilation config
├── process_result.spec     # process_result compilation config
└── README_en.md             # Project documentation (English)
```

## Quick Start

### Option 1: Run Python source code directly (recommended for development)

**Prerequisites**: `uv` tool installed

1. **Create virtual environment**
   ```bash
   uv venv --python 3.10
   ```

2. **Activate virtual environment and install dependencies**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Install dependencies
   uv pip install -r requirements.txt
   ```

3. **Run recognition**
   Run in command line:
   ```bash
   bash shell/predict_image_exe.sh
   ```

### Option 2: Use compiled executable (recommended for distribution)

See "Compilation" section below. After compilation, double-click `predict_image_exe.bat` to run without Python environment!

## Compilation

### Why compile?
Compiled executables can be copied to computers **without Python or any dependencies installed** and run directly!

### Compilation Steps

1. **Ensure virtual environment is created and activated**
   ```bash
   uv venv --python 3.10
   .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Start compilation**
   Double-click `build_exe.bat`

4. **Compilation Output**
   - `dist/predict/` - Recognition program (folder mode)
   - `dist/process_result.exe` - Result processing program (single-file mode)

### Usage after compilation
Simply double-click `predict_image_exe.bat` to run!

## Parameter Configuration Guide

### predict_image_exe.bat Parameters Explained

| Parameter | Default Value | Description | Possible Values |
|-----------|---------------|-------------|-----------------|
| `model` | `100test` | Name of the recognition model to use | `100test`, `100test_original`, `200test`, `500test` |
| `path` | `images/LYC/` | Directory path of images to be recognized | Any valid path |
| `test` | `10test` | Test identifier for output file naming | Any string |
| `saveroot` | `output/FL_${model}/` | Root directory for output results | Any valid path |
| `photosave` | `${saveroot}photos_${test}/` | Directory to save recognized images | Any valid path |
| `result` | `${saveroot}result_${test}.txt` | Path for recognition result file | Any valid path |

### predict.exe Parameters Explained

| Parameter | Default Value | Description | Possible Values |
|-----------|---------------|-------------|-----------------|
| `-c` | `configs/inference.yaml` | Configuration file path | Any valid config file path |
| `IndexProcess.index_method` | `Flat` | Indexing method | `Flat` (exact search), `HNSW32` (approximate search) |
| `Global.infer_imgs` | `${path}` | Path to images for inference | Image file or directory path |
| `IndexProcess.index_dir` | `recognition_gallery/gallery_LYC/FL_${model}` | Index library directory | Corresponding model's index path |
| `Global.det_inference_model_dir` | `models/PP-YOLOv2_LYC/` | Detection model directory | Detection model path |
| `Global.rec_inference_model_dir` | `models/FL_${model}/` | Recognition model directory | Recognition model path |
| `IndexProcess.score_thres` | `0.5` | Recognition confidence threshold, values below this are filtered | Values between 0.0-1.0 |
| `Global.use_gpu` | `False` | Whether to use GPU | `False` (use CPU), `True` (use GPU) |
| `Global.cuda_path` | `null` | CUDA installation path (required for GPU mode) | CUDA installation directory, e.g., `C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8` |
| `Global.output_dir` | `${photosave}` | Output image directory | Any valid path |
| `Global.result_dir` | `${result}` | Result file path | Any valid path |

### Common Modification Examples

**1. Use unoptimized original model**
```batch
SET model=100test_original
```

**2. Modify recognition confidence threshold**
```batch
-o "IndexProcess.score_thres=0.7"
```

**3. Use CPU for inference (when no GPU)**
```batch
-o "Global.use_gpu=False"
```

**4. Modify input image path**
```batch
SET path=images/my_images/
```

**5. Use model that excluded 200 individuals**
```batch
SET test_num=200
SET model=%test_num%test
```

**6. Use GPU for inference**
```batch
-o "Global.use_gpu=True"
-o "Global.cuda_path=C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8"
```

## FAQ

### Q: How to use GPU for inference?
**A**: Using GPU requires two steps:
1. Set `Global.use_gpu=True`
2. Specify `Global.cuda_path` to your CUDA installation directory, e.g.:
   ```batch
   -o "Global.cuda_path=C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8"
   ```

### Q: Error "cudnn64_8.dll not found" when using GPU?
**A**: Please verify:
1. CUDA and cuDNN are installed correctly
2. `Global.cuda_path` is set correctly
3. Use double backslashes `\\` in the path

### Q: What if CPU inference is too slow?
**A**: You can try these optimizations:
1. Reduce input image size (modify `configs/inference.yaml`)
2. Change `IndexProcess.index_method` to `HNSW32` for faster retrieval
3. Use GPU acceleration (see "Use GPU for inference" example above)

