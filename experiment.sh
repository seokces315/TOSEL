#!/bin/bash

# 경로 설정
EXAMPLE_DIR="./bank/example"
OUTPUT_DIR="./output"

# 실험 기본 설정
MODEL_ID="gpt-4o"
GEN_TEMPLATE="xml"
PARSE_TEMPLATE="seokc"

# 파일 루프
for file_path in "$EXAMPLE_DIR"/*_example.txt; do
    filename=$(basename "$file_path")

    # 정규식 기반 파싱
    comprehension_type=$(echo "$filename" | cut -d"_" -f1)
    problem_type=$(echo "$filename" | cut -d"_" -f2)
    level=$(echo "$filename" | cut -d"_" -f3)

    # 결과 파일명 지정
    OUTFILE="${OUTPUT_DIR}/${comprehension_type}_${problem_type}_${level}.txt"

    # 실행
    python ./src/main.py \
        --comprehension_type "$comprehension_type" \
        --problem_type "$problem_type" \
        --level "$level" \
        --model_id "$MODEL_ID" \
        --generation_template_type "$GEN_TEMPLATE" \
        --parsing_template_type "$PARSE_TEMPLATE" \
        > "$OUTFILE" 2>&1

    echo "결과 저장됨: $OUTFILE"
    echo
done

echo "모든 결과 저장됨!"
