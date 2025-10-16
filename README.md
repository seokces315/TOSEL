```plaintext
TOSEL
│
├── bank/
│   ├── example/                    # 문제 영역/난이도/유형별 Prompt
│   └── prompt/                     # 문제 영역/난이도/유형별 Example
│
├── config/
│   └── config.yaml                 # 모델 설정, API Key, temperature 등 설정
│
├── log/                            # 실행 로그 저장 디렉토리
├── output/                         # 결과 JSON/Excel 저장 디렉토리
│
├── src/
│   ├── loaders/                    # Prompt / Example 파일 로더
│   │   ├── __init__.py
│   │   ├── config_loader.py        # Config 로더
│   │   └── example_loader.py       # Example 로더
│   │   └── prompt_loader.py        # Prompt 로더
│   │ 
│   ├── pipeline/                   # LLM 기반 처리 파이프라인
│   │   ├── __init__.py
│   │   ├── base_chain.py           # Generator-Parser 체인 실행 제어
│   │   └── components/
│   │       ├── __init__.py
│   │       ├── llm_generator.py    # GPT 기반 문제 생성기 (LangChain LLMChain)
│   │       └── llm_parser.py       # GPT 기반 JSON 파서 (LangChain + JsonOutputParser)
│   │
│   ├── utils/                      # 유틸리티 함수
│   │   ├── __init__.py
│   │   ├── logger.py               # 로깅 유틸 함수
│   │   └── result_manager.py       # 결과 저장 및 Json(Excel) 관리 모듈
│   │ 
│   ├── main.py                     # 진입점 : 전체 파이프라인 실행 스크립트
│   └── parser.py                   # 명령줄 인자 정의 및 파싱 로직
│
├── .gitignore                      # Git이 추적하지 않을 파일과 폴더를 지정
└── requirements.txt                # 실행에 필요한 패키지 목록