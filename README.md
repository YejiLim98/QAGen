# QAGen
# Prompt
나는 의사 국가시험 필기 시험을 앞둔 학생이야. 수많은 기출문제들을 풀어봤는데 시험을 앞두고 더 많은 문제들을, 깊이있는 해설과 함께 풀어보고 싶어. 전혀 쓸 데 없는 문제들로 시간 낭비하고 싶지는 않아서 국시원에서 출제 관련해서 명시해 준 구체적 성과 목표를 바탕으로 문제를 만들어내고 싶어. 아래는 국시원에서 제공한 내용이야. 그리고 문제는 주요 원인 부분에 제시된 것과 같이 좀 다양한 원인 질환을 섞어서 내줘.

**의사 국가시험(필기) 평가 목표집 내의 105가지 평가 목표를 해당 위치에 개별적으로 복사했음.**

아래의 객관식 형식의 질문과 답, 그리고 그 근거(해설)을 표시해줘.(QA 세트로) 그리고 해당 문제가 내가 출처로 제시해준 파일 내용 중 어떤 구체적 성과에 매칭되는지 해당되는 구체적 성과 부분을 "purpose"에 동일하게 작성해줘.

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

환자의 임상 증상과 병력은 "question" 항목에 포함시키고, 혈액검사, 영상검사, 기타 검사 결과는 별도로 "exam" 항목에 분리하여 작성해줘. 예를 들어:
"question": "32세 남성이 황달과 복통으로 내원하였다. 환자는 2주 전부터 피로감과 식욕 부진을 호소하였으며, 최근 3일간 소변 색이 진해졌다고 한다. 신체 검사에서 공막 황달과 우상복부 압통이 관찰되었다. 이 환자의 가장 가능성 높은 진단은?",
"exam": "혈액 검사: 총 빌리루빈 5.8 mg/dL, 직접 빌리루빈 3.2 mg/dL, AST 1250 U/L, ALT 1520 U/L, ALP 180 U/L
복부 초음파: 간 실질의 미만성 에코 증가, 담낭벽 비후, 담도 확장 소견 없음"
이런 방식으로 모든 문제에서 검사 결과를 "exam" 항목으로 분리해줘.
그리고 "question"의 경우는 실제 KMLE 의사국시 문제처럼 좀 길이가 길고 구체적이었으면 좋겠어.

내가 지금 첨부한 파일은 txt 형식으로 다양한 원문 의학 교과서로부터 얻은 RAG 파일이야. source 부분의 경우 너가 문제를 낸 근거로 내가 첨부한 파일의 구체적인 content 부분을 찾아 그대로 작성해줘. 참고한 파일의 정확한 이름을 알려주고, 출처의 파일명과 실제 참고한 문장 그대로(영어) 인용해줘. 아래는 내가 출처로 올린 파일들 제목들이니까 저걸 file_name으로 적어줘야해. 교과서를 Harrison 뿐만이 아니라 내가 올려준 파일들에서 다양하게 참조해주면 좋을 것 같아.

Anatomy_Gray_textbook_data.txt, First_Aid_Step1_textbook_data.txt, First_Aid_Step2_textbook_data.txt, mmunology_Janeway._textbook_data.txt, InternalMed_Harrison_textbook_data.txt, urology_Adams_textbook_data.txt, Obstentrics_Williams_textbook_data.txt, Pathoma_Husain_textbook_data.txt, Pediatrics_Nelson_textbook_data.txt, Surgery_Schwartz_textbook_data.txt, Cell_Biology_Alberts_textbook_data.txt, Histology_Ross_textbook_data.txt, Pathology_Robbins_textbook_data.txt Physiology_Levy_textbook_data.txt, Pharmacology_Katzung_textbook_data.txt, Psichiatry_DSM-5_textbook_data.txt

source로 사용하는 내용들은 외부에서 절대 찾지 말고 절대적으로 내가 출처로 밝혀둔 txt 파일들로만 참고해줘.

"category" 항목에는 해당 문제의 source가 어느 분과(medical specialty) 지식인지로 분류해주면 돼. 아래 중에 골라서 작성해줘.
Cardiology
Pulmonology (Respiratory Medicine)
Gastroenterology
Nephrology
Infectious Diseases
Endocrinology
Allergy and Immunology
Hematology and Oncology
Rheumatology
General Surgery
Obstetrics
Gynecology
Pediatrics
Psychiatry
Dermatology
Neurology / Neurosurgery
Ophthalmology
Plastic Surgery
Otolaryngology (ENT – Ear, Nose, and Throat)
Orthopedic Surgery
Emergency Medicine
Urology

시험문제를 5개 문항 정도 만들어줘. LLM 모델을 fine tuning하기 위한 QA set이기 때문에 JSON 파일 형태로 출력해주면 더 좋을 것 같아. # 토큰 수 제한으로 자꾸 끊겨서 10개 문항에서 5개 문항으로 변경함.

절대 외부 자료 검색하지 말고 내가 보내준 자료만 참고해

# Model
Perplexity, Space, Deep research

# Documents
MedRAG/textbooks # https://huggingface.co/datasets/MedRAG/textbooks

# Rules
Web Search prohibited.Only files and links in this space.
