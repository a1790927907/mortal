set -e

while getopts f:i: flag
do
    case "${flag}" in
        f) filepath=${OPTARG};;
        i) initDataFilePath=${OPTARG};;
    esac
done

if [ -z "$filepath" ]; then
  echo "请输入文件路径!!"
  exit 2
fi

if [ $initDataFilePath ]; then
  python $initDataFilePath
else
  echo "无初始化脚本, 直接运行..."
fi

python $filepath
