"""
[주의: 덮어쓰기가 되서, 처음에 한번에 업로드할 때만 할 것 !!]
이 코드는 GitHub에서 JSON 데이터를 가져와 Hugging Face 데이터셋으로 업로드하는 과정을 자동화하는 데이터 파이프라인입니다. 

1. 설정 및 초기화
Hugging Face 사용자명, 데이터셋 이름, GitHub 파일 URL을 설정합니다.
Hugging Face API에 접근하기 위한 토큰을 지정합니다.

2. GitHub에서 데이터 다운로드
requests 라이브러리를 사용하여 GitHub의 raw 파일을 다운로드합니다.
응답 내용을 "raw_response.txt" 파일로 저장하여 필요시 수동 확인할 수 있게 합니다. 
수동으로 이 파일을 .json으로 바꾼뒤 오류가 뜨는 부분들을 github에서 수정할 수 있습니다.

3. JSON 데이터 처리
다운로드한 텍스트에서 제어 문자(control characters)를 제거하여 JSON 파싱 오류를 방지합니다.
JSON 데이터를 파싱하고 단일 객체인 경우 리스트로 변환합니다.

4. 데이터 구조 평탄화 및 재구성
중첩된 'exam' 필드를 평탄화하여 'exam_summary'로 변환합니다.
'options' 객체의 내용을 개별 필드로 변환합니다.
'source' 정보를 'source_file_name'과 'source_content'로 분리합니다.
원본 중첩 구조를 제거하고 데이터를 일관된 형식으로 재구성합니다.

5. Hugging Face Dataset 생성 및 업로드
처리된 데이터를 Dataset.from_list()를 사용하여 Hugging Face Dataset 형식으로 변환합니다.
데이터셋을 "train" 스플릿과 함께 DatasetDict로 구성합니다.
push_to_hub() 함수를 사용하여 토큰과 함께 데이터셋을 Hugging Face Hub에 업로드합니다.
"""

import os
import json
import requests
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi

# 설정
HF_USERNAME = "limyehji"  # 본인의 Hugging Face 사용자명
DATASET_NAME = "MedQANew"   # 데이터셋 이름
# GitHub의 raw 파일 URL
GITHUB_RAW_URL = "RAW GIT URL을 입력하세요!!"

# 토큰 직접 지정 - 여기에 새 토큰을, , 입력하세요
token = "Hugging face 토큰을 입력하세요!!"
api = HfApi(token=token)

# GitHub에서 JSON 파일 다운로드
print(f"GitHub에서 JSON 파일 다운로드 중: {GITHUB_RAW_URL}")
response = requests.get(GITHUB_RAW_URL)
if response.status_code != 200:
    raise Exception(f"GitHub에서 파일을 다운로드할 수 없습니다. 상태 코드: {response.status_code}")

# 응답 내용을 파일로 저장
with open("raw_response.txt", "wb") as f:
    f.write(response.content)
    
print("파일 내용이 raw_response.txt에 저장되었습니다.")

# 텍스트 내용에서 JSON 파싱 시도
try:
    # 인코딩 문제나 제어 문자 처리
    content = response.content.decode('utf-8')
    # 제어 문자 제거
    for c in range(0, 32):
        if c not in [9, 10, 13]:  # 탭, 줄바꿈, 캐리지리턴은 유지
            content = content.replace(chr(c), '')
    
    # JSON 파싱
    data = json.loads(content)
    print("JSON 파싱 성공!")
except Exception as e:
    print(f"JSON 파싱 실패: {e}")
    print("파일을 텍스트로 저장했으니 직접 확인하고, 오류를 GITHUB에서 수정하세요!!")
    exit(1)

# 단일 객체인 경우 리스트로 변환
if isinstance(data, dict):
    data = [data]

print(f"총 {len(data)}개의 항목을 로드했습니다.")

# 중첩된 구조 평탄화
for item in data:
    # chief_complaint와 chief complaint 양쪽 모두 처리
    if 'chief complaint' in item and 'chief_complaint' not in item:
        item['chief_complaint'] = item['chief complaint']
        del item['chief complaint']

    # 'options' 항목 평탄화
    if 'options' in item:
        for option_key, option_value in item["options"].items():
            item[f"option_{option_key}"] = option_value
    
    # 'source' 정보 처리
    source_content = ""
    if 'source' in item:
        if isinstance(item['source'], dict):
            # source가 딕셔너리인 경우 (file_name, content 등을 포함)
            source_parts = []
            
            # file_name이 있으면 추가
            if 'file_name' in item['source']:
                source_parts.append(f"출처: {item['source']['file_name']}")
                
            # content가 있으면 추가
            if 'content' in item['source']:
                source_parts.append(item['source']['content'])
                
            # 모든 정보를 하나의 문자열로 합침
            source_content = "\n".join(source_parts) if source_parts else ""
        else:
            # source가 문자열인 경우 그대로 사용
            source_content = item['source']
    
    # 통합된 source 내용 저장
    item['source'] = source_content
    
    # 원본 'options' 항목 삭제
    if 'options' in item:
        del item["options"]
    
    # 원본 source가 딕셔너리인 경우 삭제
    if 'source' in item and isinstance(item['source'], dict):
        pass  # 이미 위에서 처리했으므로 그대로 두기

    # 항목 순서대로 데이터 재배치
    option_keys = ["option_A", "option_B", "option_C", "option_D", "option_E"]
    options_dict = {}
    for key in option_keys:
        if key in item:
            options_dict[key] = item.get(key)
    
    reordered_item = {
        "question_id": item.get("question_id"),
        "chief_complaint": item.get("chief_complaint"),
        "purpose": item.get("purpose"),
        "question": item.get("question"),
        "exam": item.get("exam"),  # exam_summary 대신 exam 사용
        "options": options_dict,
        "answer": item.get("answer"),
        "explanation": item.get("explanation"),
        "source": item.get("source", ""),  # source_content, source_file_name 대신 source 사용
        "category": item.get("category")
    }
    
    # 재정렬된 항목을 item에 다시 할당
    item.clear()
    item.update(reordered_item)

# Dataset 변환
dataset = Dataset.from_list(data)

# 데이터셋을 DatasetDict로 변환 (train split 추가)
dataset_dict = DatasetDict({"train": dataset})

# Hugging Face에 업로드 (토큰 전달)
print(f"데이터셋을 Hugging Face Hub에 업로드 중: {HF_USERNAME}/{DATASET_NAME}")
dataset_dict.push_to_hub(f"{HF_USERNAME}/{DATASET_NAME}", token=token)

print(f"✅ 완료! 데이터셋이 업로드되었습니다: https://huggingface.co/datasets/{HF_USERNAME}/{DATASET_NAME}")
print(f"Python에서 다음과 같이 로드할 수 있습니다:")
print(f"from datasets import load_dataset")
print(f"dataset = load_dataset('{HF_USERNAME}/{DATASET_NAME}')")