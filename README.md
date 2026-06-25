# LYC 个体识别项目

## 项目概述
这是一个基于深度学习的鱼类个体识别系统，使用 PaddlePaddle 框架实现。项目包含检测模型（PP-YOLOv2）和识别模型，能够对输入图像中的鱼类进行检测和个体识别。

## 项目结构
```
LYC_Individual_recognition_demo/
├── configs/                  # 配置文件目录
│   └── inference.yaml       # 推理配置文件
├── dist/                     # 打包后的可执行文件
│   ├── predict/             # 识别程序
│   └── process_result.exe   # 结果处理程序
├── scripts/                 # 脚本代码
│   ├── predict.py           # 识别核心代码
│   └── process_result.py    # 结果处理代码
├── images/                  # 测试图像目录
│   └── LYC/                # 测试图像
├── models/                  # 模型文件目录
│   ├── FL_100test/         # 排除100尾个体，用剩余个体训练的模型
│   ├── FL_100test_original/# 排除100尾个体，用剩余个体训练的原始模型（未优化）
│   ├── FL_200test/         # 排除200尾个体，用剩余个体训练的模型
│   ├── FL_500test/         # 排除500尾个体，用剩余个体训练的模型
│   └── PP-YOLOv2_LYC/      # 检测模型
├── recognition_gallery/     # 识别图库
│   └── gallery_LYC/       # 鱼类特征索引库
├── output/                  # 输出结果目录
│   ├── FL_100test/         # 排除100尾个体模型输出
│   ├── FL_100test_original/# 排除100尾个体原始模型输出
│   ├── FL_200test/         # 排除200尾个体模型输出
│   └── FL_500test/         # 排除500尾个体模型输出
├── predict_image_exe.bat    # Windows批处理脚本（使用编译后的程序）
├── build_exe.bat            # 编译脚本
├── requirements.txt         # Python依赖列表
├── predict.spec            # predict编译配置
├── process_result.spec     # process_result编译配置
└── README.md                # 项目说明文档
```

## 快速开始

### 方式一：直接运行Python源码（推荐用于开发调试）

**前置条件**：已安装 `uv` 工具

1. **创建虚拟环境**
   ```bash
   uv venv --python 3.10
   ```

2. **激活虚拟环境并安装依赖**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # 安装依赖
   uv pip install -r requirements.txt
   ```

3. **运行识别**
   在命令行中执行：
   ```bash
   bash shell/predict_image_exe.sh
   ```

### 方式二：使用编译后的可执行文件（推荐用于分发）

详见下方"编译"章节，编译完成后双击 `predict_image_exe.bat` 即可运行，无需Python环境！

## 编译

### 为什么需要编译？
编译后生成的可执行文件可以拷贝到**没有安装Python及相关依赖库**的电脑上直接运行！

### 编译步骤

1. **确保虚拟环境已创建并激活**
   ```bash
   uv venv --python 3.10
   .venv\Scripts\activate
   ```

2. **安装依赖**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **开始编译**
   双击运行 `build_exe.bat`

4. **编译输出**
   - `dist/predict/` - 识别程序（文件夹模式）
   - `dist/process_result.exe` - 结果处理程序（单文件模式）

### 编译后使用
直接双击 `predict_image_exe.bat` 即可运行！

## 参数修改说明

### predict_image_exe.bat 参数详解

| 参数 | 默认值 | 说明 | 可修改值 |
|-----|--------|------|---------|
| `model` | `100test` | 使用的识别模型名称 | `100test`, `100test_original`, `200test`, `500test` |
| `path` | `images/LYC/` | 待识别图像的目录路径 | 任意有效路径 |
| `test` | `10test` | 测试标识，用于输出文件命名 | 任意字符串 |
| `saveroot` | `output/FL_${model}/` | 输出结果的根目录 | 任意有效路径 |
| `photosave` | `${saveroot}photos_${test}/` | 识别后图像的保存目录 | 任意有效路径 |
| `result` | `${saveroot}result_${test}.txt` | 识别结果文件路径 | 任意有效路径 |

### predict.exe 参数详解

| 参数 | 默认值 | 说明 | 可修改值 |
|-----|--------|------|---------|
| `-c` | `configs/inference.yaml` | 配置文件路径 | 任意有效配置文件路径 |
| `IndexProcess.index_method` | `Flat` | 索引方法 | `Flat`（精确搜索）、`HNSW32`（近似搜索） |
| `Global.infer_imgs` | `${path}` | 待推理图像路径 | 图像文件或目录路径 |
| `IndexProcess.index_dir` | `recognition_gallery/gallery_LYC/FL_${model}` | 索引库目录 | 对应模型的索引库路径 |
| `Global.det_inference_model_dir` | `models/PP-YOLOv2_LYC/` | 检测模型目录 | 检测模型路径 |
| `Global.rec_inference_model_dir` | `models/FL_${model}/` | 识别模型目录 | 识别模型路径 |
| `IndexProcess.score_thres` | `0.5` | 识别置信度阈值，低于此值会被过滤 | 0.0-1.0之间的数值 |
| `Global.use_gpu` | `False` | 是否使用GPU | `False`（使用CPU）、`True`（使用GPU） |
| `Global.cuda_path` | `null` | CUDA安装路径（GPU模式时需指定） | CUDA安装目录路径，如：`C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8` |
| `Global.output_dir` | `${photosave}` | 输出图像目录 | 任意有效路径 |
| `Global.result_dir` | `${result}` | 结果文件路径 | 任意有效路径 |

### 常用修改示例

**1. 使用未优化的原始模型**
```batch
SET model=100test_original
```

**2. 修改识别置信度阈值**
```batch
-o "IndexProcess.score_thres=0.7"
```

**3. 使用CPU进行推理（无GPU时）**
```batch
-o "Global.use_gpu=False"
```

**4. 修改输入图像路径**
```batch
SET path=images/my_images/
```

**5. 使用排除200尾个体的模型**
```batch
SET test_num=200
SET model=%test_num%test
```

**6. 使用GPU进行推理**
```batch
-o "Global.use_gpu=True"
-o "Global.cuda_path=C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8"
```

## 常见问题

### Q: 如何使用GPU进行推理？
**A**: 使用GPU需要两个步骤：
1. 修改 `Global.use_gpu=True`
2. 指定 `Global.cuda_path` 为您的CUDA安装路径，例如：
   ```batch
   -o "Global.cuda_path=C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8"
   ```

### Q: 使用GPU时报错找不到 `cudnn64_8.dll`？
**A**: 请确认：
1. 已正确安装CUDA和cuDNN
2. `Global.cuda_path` 路径设置正确
3. 路径中使用双反斜杠 `\\`

### Q: CPU推理速度慢怎么办？
**A**: 可以尝试以下优化：
1. 减小输入图像尺寸（修改 `configs/inference.yaml`）
2. 调整 `IndexProcess.index_method` 为 `HNSW32` 以加快检索速度
3. 使用GPU加速（参考上方"使用GPU进行推理"示例）

