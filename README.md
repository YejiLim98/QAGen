# QAGen

### Prompt 
last update : 250228 3P -> 250307 11A

### Model & GPT functions
다음 과정을 순서대로 거쳐서 Raw QA를 생성함. 
- ChatGPT 4o, <MCQ Generator>, MCQ를 만들도록 하는 GPT Projects, Ask Following Questions if the results are not sufficient: In most cases, follow up questions were about providing more MCQs.
- ChatGPT o1, <Json 파일 다듬기>, 그동안 만든 문제들을 Purpose에 따라서 정렬하고 하나의 Json 파일로 다듬도록하는 GPT Projects 
- ChatGPT o1, <MCQ Refiner>, 필요시 만들어진 MCQ의 퀄리티 개선 (Lab data의 수치화, 문제의 어색한 표현, 문항의 다양성)

### Documents
1. Raw QA set : 10+ Questions about each "Assessment Objective". <MCQ Generator>, <Json 파일 다듬기>, <MCQ refiner>
   [RawQA 폴더 열기](./RawQA)
2. Revised QA set : 5-10 Questions reviewed and curated by a clincian from th4e original QA set. 
   - QA set assessing similar contents were reviewed
   - Difficulty level was reviewed and QA sets containing obvious answers were removed.

### Update Notes
1_가려움증, 97_황달 : 둘의 프롬프트는 이전 버전 프롬프트여서 다시 돌려야함.
