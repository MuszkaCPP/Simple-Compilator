INPUT_FILE_PATH="$1"
OUTPUT_FILE_NAME="$2"
OUTPUT_FILE_PATH="./maszyna_wirtualna/$OUTPUT_FILE_NAME"

#Compilation
python3 compiler.py "$INPUT_FILE_PATH" "$OUTPUT_FILE_PATH"

#Running code on machine
if test -f "$OUTPUT_FILE_PATH"; then
    ./maszyna_wirtualna/maszyna-wirtualna-cln "$OUTPUT_FILE_PATH"
    echo "[ Compilation completed! ]"
else
    echo "[ Compilation Error ]"
fi
