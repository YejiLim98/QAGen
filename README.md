# QAGen

### GitHub 사용 방법
1. 각자 Branch를 생성
2. 각자 Branch에 생성한 json 파일(QASet)과 활용한자료들 업로드 (ex. Prompt, 사용한 모델 기록)
3. 추후에 main branch에 업로드

### 

### HuggingFace 업데이트 
- 데이터셋 완료 후 2_add_dataset.py 코드를 활용하여 HuggingFace에 해당 데이터셋 업로드
- 허깅페이스 데이터셋 링크 : https://huggingface.co/datasets/limyehji/MedQANew 
- 업데이트 코드 : [GitToHug](/src)

### Medical Specialities
Cardiology, Pulmonology (Respiratory Medicine), Gastroenterology, Nephrology, Infectious Diseases, Endocrinology, Allergy and Immunology, Hematology and Oncology, Rheumatology, General Surgery, Obstetrics, Gynecology, Pediatrics, Psychiatry, Dermatology, Neurology / Neurosurgery, Ophthalmology, Plastic Surgery, Otolaryngology, Orthopedic Surgery, Emergency Medicine, Urology, 의료통계, 의료법

### 문제 형식
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
