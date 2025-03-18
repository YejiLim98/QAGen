# GitHub의 QAset를 Huggingface로 올리는 코드
## 환경 설정하는 방법! 
### 1. conda env 인 경우 
1. 환경 생성하기 
conda env create -f environment.yml

2. 기존 환경을 업데이트하기(--prune 옵션은 환경파일에 없는 패키지를 제거)
conda env update -f environment.yml --prune

### 2. venv 인 경우
pip install -r requirements.txt

### 3. Global 인 경우 

## src 활용하는 방법! 
1. HuggingFace Token을 입력하기 : TOKEN 잃어버리면 LYJ에게~!~!
2. 올리고자 하는 json file의 raw file을 입력하기
3. json 파일이 깨져있다면 다운 받아진 json file을 수기로 고쳐서 다시 gitHub에서 업데이트하고 코드 다시 돌리기

## 업로드 가능한 QA set 형식
'''
{ "question_id": ,
"chief complaint": ,
"purpose": ,
"question”: ,
“exam”: ,
"options": { "A": "B": "C": "D": "E": },
"answer": ,
"explanation": "
"source": 
“category”:,
}
'''
- cheif_complaint 도 가능함.
- "source: {textbook: }, {content; }" 식으로 된 dictionary 형식도 평탄화 가능함. 이건 코드 확인 필요함. 
