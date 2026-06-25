@echo off
SET test_num=100
SET model=%test_num%test
SET path=images/LYC/
SET test=10test
SET saveroot=output/FL_%model%/
SET photosave=%saveroot%photos_%test%/
if not exist "%saveroot%" md "%saveroot%"
if not exist "%photosave%" md "%photosave%"
SET result=%saveroot%result_%test%.txt
cd.> "%result%"
dist\predict\predict.exe ^
-c "configs/inference.yaml" ^
-o "IndexProcess.index_method=Flat" ^
-o "Global.infer_imgs=%path%" ^
-o "IndexProcess.index_dir=recognition_gallery/gallery_LYC/FL_%model%" ^
-o "Global.det_inference_model_dir=models/PP-YOLOv2_LYC/" ^
-o "Global.rec_inference_model_dir=models/FL_%model%/" ^
-o "IndexProcess.score_thres=0.5" ^
-o "Global.use_gpu=True" ^
-o "Global.cuda_path=C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.6" ^
-o "Global.output_dir=%photosave%" ^
-o "Global.result_dir=%result%"

echo %result%
dist\process_result.exe "--result_txt="%result%"" "--mode=image"
echo test finish
pause
