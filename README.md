```plaintext
AI_Module
│
├── main.py                     # 진입점 : 전체 파이프라인 실행 스크립트
│
├── loaders/                    # Prompt / Example 파일 로더
│   ├── __init__.py
│   ├── prompt_loader.py        # 문제 영역/난이도/유형별 Prompt 로드
│   └── example_loader.py       # 문제 영역/난이도/유형별 Example 로드
│
├── pipeline/                   # LLM 기반 처리 파이프라인
│   ├── __init__.py
│   ├── base_chain.py           # Generator-Parser 체인 실행 제어
│   └── components/
│       ├── __init__.py
│       ├── llm_generator.py    # GPT 기반 문제 생성기 (LangChain LLMChain)
│       └── llm_parser.py       # GPT 기반 JSON 파서 (LangChain + JsonOutputParser)
│
├── utils/                      # 유틸리티 함수
│   ├── __init__.py
│   ├── logger.py               # 로깅 유틸 함수
│   └── result_manager.py       # 결과 저장 및 Json(Excel) 관리 모듈
│
├── config/
│   └── config.yaml             # 모델 설정, API Key, 저장 경로, temperature 등 설정
│
├── log/                        # 실행 로그 저장 디렉토리
├── output/                     # 결과 JSON/Excel 저장 디렉토리
└── requirements.txt            # 실행에 필요한 패키지 목록