# QAGen

### Prompt 
last update : 250228 3P

### Model & GPT functions
ChatGPT 4o, Projects <MCQ Generator>

### Documents
1. Original QA set : minimum of 15 Questions about each "Assessment Objective" (./RawQA)
3. Revised QA set : 10 Questions reviewed and curated from the original QA set. QA set was removed adhering the following rules : 
   - QA set assessing similar contents were reviewed and only ONE QA set was selected.
   - Difficulty level was reviewed and QA set containing obvious answers.

### Rules 
1. Generate 15 Questions using ChatGPT web UI.
   - Ask Following Questions if the results are not sufficient
        : In most cases, follow up questions were about providing more MCQs.
   - Refine the format using ChatGPT Project (Json Refiner, model o1)
2. Review the QA set and select 10 out of each "Assessment Objective". (Performed by 1 Clinician)  

### Update Notes
1_가려움증, 97_황달 : 둘의 프롬프트는 이전 버전 프롬프트여서 다시 돌려야함.
