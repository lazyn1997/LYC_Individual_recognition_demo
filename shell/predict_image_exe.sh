predict(){
  test_num="$1"
  model="${test_num}"test
  path=./images/LYC/
  test=10test
  saveroot=./output/FL_"${model}"/
  photosave="${saveroot}"photos_"${test}"/
  if [ ! -d "${saveroot}" ]
  then
    mkdir "${saveroot}"
  fi
  if [ ! -d "${photosave}" ]
  then
    mkdir "${photosave}"
  fi
  result="${saveroot}"result_"${test}".txt
  > "${result}"
  python scripts/predict.py \
  -c configs/inference.yaml \
  -o IndexProcess.index_method=Flat \
  -o Global.infer_imgs="${path}" \
  -o IndexProcess.index_dir="./recognition_gallery/gallery_LYC/FL_${model}" \
  -o Global.det_inference_model_dir="./models/PP-YOLOv2_LYC/" \
  -o Global.rec_inference_model_dir="./models/FL_${model}/" \
  -o IndexProcess.score_thres=0.5 \
  -o Global.use_gpu=True \
  -o Global.output_dir="${photosave}" \
  -o Global.result_dir="${result}"

  echo "${result}"
  python scripts/process_result.py --result_txt="${result}" --mode="image"
}

source ./.venv/Scripts/activate
test_num=100
predict "${test_num}"
printf "test finish\n\n"
