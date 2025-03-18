"""
[기존 데이터셋에 추가하는 코드]
기존 데이터셋에 새로운 GitHub 데이터를 중복 없이 추가하고 question_id를 재설정하는 코드
1. 기존 Hugging Face 데이터셋을 로드합니다.
2. 새 GitHub raw 파일을 다운로드하고 로컬에 저장합니다.
3. JSON 데이터를 파싱하고 제어 문자 문제를 처리합니다.
4. 새 데이터를 전처리하여 필요한 구조로 변환합니다.
5. 질문 내용을 기준으로 중복을 제거하고 기존 데이터와 새 데이터를 합칩니다.
6. 항목들에 1부터 시작하는 새로운 question_id를 부여합니다.
7. 최종 데이터를 Hugging Face Dataset으로 변환하여 업로드합니다.

사용하기 전에 NEW_GITHUB_RAW_URL 변수를 새 GitHub 파일의 실제 URL로 바꿔야 합니다.
"""
import os
import json
import requests
from datasets import Dataset, DatasetDict, load_dataset
from huggingface_hub import HfApi

# 설정
HF_USERNAME = "limyehji"  # 본인의 Hugging Face 사용자명
DATASET_NAME = "MedQANew"   # 데이터셋 이름
# 새로운 GitHub의 raw 파일 URL
NEW_GITHUB_RAW_URL = "RAW GIT URL을 입력하세요!!"

# 토큰 직접 지정
token = "허깅페이스 토큰을 입력하세요!!"
api = HfApi(token=token)

# 1. 기존 데이터셋 로드
print(f"기존 데이터셋 로드 중: {HF_USERNAME}/{DATASET_NAME}")
try:
    existing_dataset = load_dataset(f"{HF_USERNAME}/{DATASET_NAME}")
    existing_data = existing_dataset["train"].to_list()
    print(f"기존 데이터셋에서 {len(existing_data)}개 항목을 로드했습니다.")
except Exception as e:
    print(f"기존 데이터셋 로드 실패: {e}")
    existing_data = []
    print("새 데이터셋을 생성합니다.")

# 2. 새 GitHub 파일 다운로드
print(f"GitHub에서 새 JSON 파일 다운로드 중: {NEW_GITHUB_RAW_URL}")
response = requests.get(NEW_GITHUB_RAW_URL)
if response.status_code != 200:
    raise Exception(f"GitHub에서 파일을 다운로드할 수 없습니다. 상태 코드: {response.status_code}")

# 응답 내용을 파일로 저장
with open("raw_response.txt", "wb") as f:
    f.write(response.content)
    
print("파일 내용이 raw_response.txt에 저장되었습니다.")

# 3. JSON 파싱
try:
    # 인코딩 문제나 제어 문자 처리
    content = response.content.decode('utf-8')
    # 제어 문자 제거
    for c in range(0, 32):
        if c not in [9, 10, 13]:  # 탭, 줄바꿈, 캐리지리턴은 유지
            content = content.replace(chr(c), '')
    
    # JSON 파싱
    new_data = json.loads(content)
    print("JSON 파싱 성공!")
except Exception as e:
    print(f"JSON 파싱 실패: {e}")
    print("파일을 텍스트로 저장했으니 직접 확인하고, 오류를 GITHUB에서 수정하세요!!")
    exit(1)

# 단일 객체인 경우 리스트로 변환
if isinstance(new_data, dict):
    new_data = [new_data]

print(f"새 데이터에서 {len(new_data)}개 항목을 로드했습니다.")

# 4. 새 데이터 처리
for item in new_data:
    
    # chief_complaint와 chief complaint 양쪽 모두 처리
    if 'chief complaint' in item and 'chief_complaint' not in item:
        item['chief_complaint'] = item['chief complaint']
        del item['chief complaint']

    # 'options' 항목 평탄화
    if 'options' in item:
        for option_key, option_value in item["options"].items():
            item[f"option_{option_key}"] = option_value
    
    # 'source' 정보 처리 - 수정된 부분
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
    
    # 통합된 source 내용을 source_content에 저장
    item['source'] = source_content
    
    # 원본 'exam'과 'options', 'source' 항목 삭제
    if 'options' in item:
        del item["options"]

    # 항목 순서대로 데이터 재배치
    option_keys = ["option_A", "option_B", "option_C", "option_D", "option_E"]
    options_dict = {}
    for key in option_keys:
        if key in item:
            options_dict[key] = item.get(key)
    
    reordered_item = {
        "question_id": item.get("question_id"),
        "chief_complaint": item.get("chief_complaint", ""),
        "purpose": item.get("purpose"),
        "question": item.get("question"),
        "exam": item.get("exam"),
        "options": options_dict,
        "answer": item.get("answer"),
        "explanation": item.get("explanation"),
        "source": item.get("source", ""),
        "category": item.get("category")
    }
    
    # 재정렬된 항목을 item에 다시 할당
    item.clear()
    item.update(reordered_item)

# 5. 중복 제거 및 데이터 합치기
# 질문 내용을 키로 사용해 중복 확인
unique_questions = {}

# 기존 데이터에서 고유한 질문 추출
for item in existing_data:
    question = item.get("question", "")
    if question:  # 질문이 비어있지 않은 경우만 처리
        unique_questions[question] = item

# 새 데이터에서 고유한 질문 추가 (중복은 덮어쓰기)
for item in new_data:
    question = item.get("question", "")
    if question:  # 질문이 비어있지 않은 경우만 처리
        unique_questions[question] = item

# 사전에서 리스트로 변환
combined_data = list(unique_questions.values())

# Chief_complaint 기준으로 정렬
# None 값이나 빈 문자열은 맨 뒤로 정렬되도록 처리
combined_data.sort(key=lambda x: (x.get("chief_complaint") or "ZZZZ"))

# question_id 재설정
for i, item in enumerate(combined_data, 1):  # 1부터 시작하는 번호
    item["question_id"] = i

print(f"중복 제거 후 총 {len(combined_data)}개의 고유한 항목이 있습니다.")
print(f"모든 question_id가 1부터 {len(combined_data)}까지 Chief_complaint 순서대로 재설정되었습니다.")

# 6. Dataset 변환
dataset = Dataset.from_list(combined_data)

# 7. 데이터셋을 DatasetDict로 변환 (train split 추가)
dataset_dict = DatasetDict({"train": dataset})

# 8. Hugging Face에 업로드 (토큰 전달)
print(f"데이터셋을 Hugging Face Hub에 업로드 중: {HF_USERNAME}/{DATASET_NAME}")
dataset_dict.push_to_hub(f"{HF_USERNAME}/{DATASET_NAME}", token=token)

print(f"✅ 완료! 데이터셋이 업데이트되었습니다: https://huggingface.co/datasets/{HF_USERNAME}/{DATASET_NAME}")
print(f"Python에서 다음과 같이 로드할 수 있습니다:")
print(f"from datasets import load_dataset")
print(f"dataset = load_dataset('{HF_USERNAME}/{DATASET_NAME}')")