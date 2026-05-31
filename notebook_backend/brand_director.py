# 환경변수 로드 및 시스템 경로 설정을 담당하는 함수
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
import base64
import io
import json
from datetime import datetime
import uuid
import time
import re

def setup_environment():
    """시스템 경로를 추가하고 .env 파일을 로드하는 함수"""
    # 1. 시스템 경로 추가
    backend_path = Path(".").resolve().parent / "backend"
    parent_path = str(Path(".").resolve().parent)
    
    # 중복 추가 방지
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    if parent_path not in sys.path:
        sys.path.insert(0, parent_path)

    # 2. 환경 변수 로드
    load_dotenv()
    # (선택 사항) 로드 완료 메시지를 띄우고 싶다면 추가
    # print("✅ 환경 설정 및 .env 로드 완료")

# Gemini API 키 로드 및 검증 함수
def load_gemini_keys():
    """환경 변수에서 Gemini API 키를 불러오고 검증하는 함수"""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_image_api_key = os.getenv("GEMINI_IMAGE_API_KEY")

    # API 키 검증
    if not gemini_api_key:
        print("❌ GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        sys.exit()
    else:
        print("✅ Gemini API 키 로드 완료")

    if not gemini_image_api_key:
        print("❌ GEMINI_IMAGE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        sys.exit()
    else:
        print("✅ Gemini Image API 키 로드 완료")
        
    # 성공적으로 로드된 키 반환
    return gemini_api_key, gemini_image_api_key

# 사용자 입력 처리용 헬퍼 함수
def get_valid_text(prompt, error_msg, min_length=3):
    """일반 텍스트를 입력받고 최소 길이를 검증하는 함수"""
    value = input(prompt).strip()
    while len(value) < min_length:
        value = input(error_msg).strip()
    return value

# 리스트 입력 처리용 헬퍼 함수
def get_valid_list(prompt, error_msg, min_items=1, max_items=4):
    """콤마로 구분된 리스트를 입력받고 개수를 검증하는 함수"""
    val_input = input(prompt).strip()
    values = [v.strip() for v in val_input.split(",") if v.strip()]
    
    while len(values) < min_items or len(values) > max_items:
        val_input = input(error_msg).strip()
        values = [v.strip() for v in val_input.split(",") if v.strip()]
    return values

# 브랜드 정보 수집 함수
def get_brand_info():
    """위의 헬퍼 함수들을 이용해 브랜드 정보를 수집하는 함수"""
    print("\n" + "=" * 100)
    print("🎯 NameTag 브랜드 가이드 생성")
    print("=" * 100)
    print("\n📝 브랜드 정보를 입력해주세요:\n")

    # 헬퍼 함수를 호출해서 아주 깔끔하게 입력받음
    business_type = get_valid_text(
        prompt="🏢 업종/서비스를 입력하세요 (예: 온라인 친환경 쇼핑몰): ",
        error_msg="❌ 최소 3글자 이상 입력해주세요: "
    )

    vibes = get_valid_list(
        prompt="✨ 브랜드 감성을 선택하세요 (4개까지 입력해주세요. 쉼표로 구분, 예: 모던, 신뢰): ",
        error_msg="❌ 1~4개의 감성을 선택해주세요: "
    )

    target = get_valid_text(
        prompt="👥 타겟 고객을 입력하세요 (예: 20-40대 환경 의식 있는 소비자): ",
        error_msg="❌ 최소 3글자 이상 입력해주세요: "
    )

    # 선택사항은 검증 없이 바로 입력받음
    keywords = input("🔑 추가 키워드 (선택사항): ").strip()

    # 결과 출력
    print("\n" + "=" * 100)
    print("✅ 입력된 브랜드 정보:")
    print(f"업종/서비스: {business_type}")
    print(f"브랜드 감성: {', '.join(vibes)}")
    print(f"타겟 고객: {target}")
    print(f"추가 키워드: {keywords}")
    print("=" * 100)

    return {
        "business_type": business_type,
        "vibes": vibes,
        "target": target,
        "keywords": keywords
    }

# Gemini API에 보낼 프롬프트 생성 함수
def get_prompt(prompt, brand_data, selected_brand_name="브랜드명 미정"):
    # 2️⃣ Gemini API에 보낼 프롬프트 생성
    print("\n📨 Gemini API에 요청할 프롬프트:")
    prompt = f"""
[기본 입력 정보]
- 업종/서비스: {brand_data['business_type']}
- 브랜드 감성: {', '.join(brand_data['vibes'])}
- 타겟 고객: {brand_data['target']}
- 확정된 브랜드명: {selected_brand_name}
""" + prompt
    print(prompt)
    print("\n" + "-" * 100)

    return prompt

# Gemini API에 요청하는 함수
def request_gemini_api(prompt, SYSTEM_PROMPT, max_retries=10, GEMINI_API_KEY=None):
    print("\n" + "-" * 100)
    print("💬 AI에 요청 중입니다... 잠시만 기다려주세요.")
    print("-" * 100)
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    retries = 0
    while retries <= max_retries:
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            raw_text = response.text or ""
            print("\n✅ AI 응답 수신 완료!")
            print(f"응답 텍스트: {raw_text[:100]}...") # 너무 길 수 있어 100자만 자름
            return raw_text
        
        except Exception as e:
            error_str = str(e)
            # 발생한 에러 메시지 안에 429, 500, 502, 503이 포함되어 있는지 확인
            if any(code in error_str for code in ["429", "500", "502", "503"]):
                retries += 1
                print(f"\n⚠️ 서버 과부하 또는 할당량 초과 에러 발생: {error_str.split('.')[0]}")
                
                if retries <= max_retries:
                    print(f"⏳ 1분 30초 대기 후 재요청합니다... (재시도 횟수: {retries}/{max_retries})")
                    time.sleep(90) # 90초(1분 30초) 대기
                    continue # while 루프의 처음으로 돌아가서 다시 try 시도
                else:
                    print("\n❌ 최대 재시도 횟수를 초과했습니다. 잠시 후 다시 프로그램을 실행해주세요.")
                    sys.exit()
            else:
                # 429, 500, 503 외의 알 수 없는 다른 에러인 경우 즉시 종료
                print(f"\n❌ 처리할 수 없는 AI 응답 오류: {e}")
                sys.exit()

# Gemini Image API를 호출하여 이미지를 생성하고, 결과 데이터를 반환하는 공통 함수.
def request_gemini_image_api(prompt, max_retries=3, GEMINI_API_KEY=None):
    print("\n" + "-" * 100)
    print("🎨 AI 이미지 생성 요청 중입니다... 잠시만 기다려주세요.")
    print("-" * 100)
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY가 제공되지 않았습니다.")
        return None

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    retries = 0
    while retries <= max_retries:
        try:
            result = client.models.generate_content(
                model='gemini-3.1-flash-image-preview',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                )
            )
            
            image_data = None
            if hasattr(result, 'parts') and len(result.parts) > 0:
                part = result.parts[0]
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                elif hasattr(part, 'image') and part.image:
                    image_data = part.image.image_bytes
            
            if image_data:
                print("\n✅ AI 이미지 생성 완료!")
                return image_data
            else:
                print("\n❌ 이미지 데이터 추출 실패.")
                return None
                
        except Exception as e:
            error_str = str(e)
            if any(code in error_str for code in ["429", "500", "502", "503"]):
                retries += 1
                print(f"\n⚠️ 이미지 서버 과부하 또는 할당량 초과 에러 발생: {error_str.split('.')[0]}")
                
                if retries <= max_retries:
                    print(f"⏳ 30초 대기 후 재요청합니다... (재시도 횟수: {retries}/{max_retries})")
                    time.sleep(30) # 이미지 생성은 텍스트보다 부하가 클 수 있어 대기 시간 조절
                    continue
                else:
                    print("\n❌ 최대 재시도 횟수를 초과했습니다.")
                    return None
            else:
                print(f"\n❌ 처리할 수 없는 AI 이미지 응답 오류: {e}")
                return None
            
# 로고 이미지 생성 함수
def generate_logo_image(brand_name, de_section_data, api_key):
    # 1. 새 JSON 스키마에 맞춘 데이터 추출
    concept = de_section_data.get('logo_identity', {}).get('concept', {})
    direction_text = concept.get('direction_text', '모던하고 심플한 워드마크 또는 심볼 형태')
    
    # 2. 로고 전용 고해상도 프롬프트 조합 (안전장치 추가)
    prompt = f"""당신은 세계적인 수준의 브랜드 아이덴티티(BI) 전문 디자이너입니다.
다음 지시사항에 따라 브랜드 로고를 완벽하게 디자인해 주세요.

[브랜드명]: {brand_name}
[디자인 핵심 방향성]: {direction_text}

[엄격한 품질 및 스타일 요구사항]
- 스타일: 3D 효과, 그림자, 그라데이션, 광택이 전혀 없는 완벽하게 플랫(Flat)한 2D 벡터 스타일.
- 배경: 완벽한 순백색(Solid White, #FFFFFF) 배경. 투명도나 다른 배경 요소 절대 금지.
- 디테일: 복잡한 스케치나 스머지(번짐) 효과 없이, 선명하고 또렷한 가장자리(Crisp edges) 유지.
- 텍스트 제어: '{brand_name}' 외에 의미를 알 수 없는 이상한 AI 문자나 기호가 절대 포함되지 않도록 할 것.
- 목적: 전문 브랜딩 에이전시의 포트폴리오에 들어갈 법한 세련되고 미니멀한 마스터 로고.
"""
    
    image_data = request_gemini_image_api(prompt, GEMINI_API_KEY=api_key)
    
    if image_data:
        logo_dir = Path("assets/logos")
        logo_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logo_filename = f"logo_{brand_name.replace(' ', '_')}_{timestamp}.png"
        logo_path = logo_dir / logo_filename
        
        with open(logo_path, 'wb') as f:
            f.write(image_data)
        
        abs_path = os.path.abspath(logo_path)
        print(f"📁 로고 저장 위치: {abs_path}")
        return abs_path
    return None

# 캐릭터 이미지 생성 함수
def generate_character_image(brand_name, de_section_data, api_key):
    # 1. 새 JSON 스키마에 맞춘 데이터 추출
    char_intro = de_section_data.get('character_guide', {}).get('intro', {})
    char_name = char_intro.get('name', '마스코트')
    char_appearance = char_intro.get('appearance', '브랜드 무드에 맞는 귀여운 마스코트')
    
    # 2. 캐릭터 전용 고해상도 프롬프트 조합
    prompt = f"""당신은 세계적인 수준의 브랜드 캐릭터(마스코트) 전문 일러스트레이터입니다.
다음 지시사항에 따라 브랜드를 대변할 매력적인 캐릭터를 디자인해 주세요.

[브랜드명]: {brand_name}
[캐릭터 이름]: {char_name}
[캐릭터 외형 묘사]: {char_appearance}

[엄격한 품질 및 스타일 요구사항]
- 스타일: 브랜드 로고와 시각적 일관성을 갖춘 깔끔한 2D 벡터 일러스트레이션 또는 매우 정제된 캐릭터 아트.
- 구도: 캐릭터의 전신이나 상반신이 중앙에 명확하게 배치된 프로필 샷. (배경에 복잡한 풍경 금지)
- 배경: 완벽한 순백색(Solid White, #FFFFFF) 배경.
- 표현: 타겟 고객이 호감을 느낄 수 있는 친근하고 호소력 있는 표정과 동세.
- 텍스트 제어: 이미지 안에 어떤 텍스트나 글자도 포함하지 말 것. 오직 캐릭터 형태에만 집중할 것.
"""
    
    image_data = request_gemini_image_api(prompt, GEMINI_API_KEY=api_key)
    
    if image_data:
        char_dir = Path("assets/characters")
        char_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        char_filename = f"char_{brand_name.replace(' ', '_')}_{timestamp}.png"
        char_path = char_dir / char_filename
        
        with open(char_path, 'wb') as f:
            f.write(image_data)
        
        abs_path = os.path.abspath(char_path)
        print(f"📁 캐릭터 저장 위치: {abs_path}")
        return abs_path
    return None

# 4AI 응답 파싱
def parse_ai_response(raw_text):
    try:
        # JSON 추출
        import re
        json_match = re.search(r'\{[\s\S]*\}', raw_text)
        if json_match:
            ai_response = json.loads(json_match.group())
        else:
            ai_response = json.loads(raw_text)
        
        print("✅ JSON 파싱 완료!")
        print(f"파싱된 JSON: {json.dumps(ai_response)}")
        return ai_response
        
    except Exception as e:
        print(f"❌ JSON 파싱 오류: {e}")
        print(f"원본 응답: {raw_text}")
        ai_response = {}
        sys.exit()

# 사용자 입력 처리용 헬퍼 함수
def get_user_choice(prompt_text, max_num):
    while True:
        choice = input(prompt_text).strip()
        try:
            index = int(choice) - 1
            if 0 <= index < max_num:
                return index
            else:
                print(f"⚠️ 1~{max_num} 사이의 숫자를 입력해주세요. 기본값(1)을 선택합니다.")
                return 0
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. 1~{max_num} 사이의 '숫자'만 입력해주세요.")
            return 0

# 아이템 선택용 헬퍼 함수
def select_item(step_title, items, format_func, prompt_text):
    print(f"\n[{step_title}]")
    for i, item in enumerate(items):
        # format_func(lambda)를 통해 원하는 출력 형태로 포매팅
        print(f"  {i+1}. {format_func(item)}")
    return get_user_choice(prompt_text, len(items))

# AI 인터뷰 진행 함수
def conduct_ai_interview(parsed_response, title="🤖 AI 브랜드 디렉터의 심층 인터뷰"):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)
    
    # AI 분석 결과가 있을 경우 출력
    if 'reasoning' in parsed_response:
        print(f"💡 AI 분석: {parsed_response['reasoning']}\n")

    collected_answers = []
    
    # 안전장치: AI가 명시한 개수와 실제 배열 길이가 다를 수 있으므로 실제 배열 길이 사용
    total_q = len(parsed_response['questions'])

    # AI가 생성한 질문 개수만큼 반복
    for idx, q in enumerate(parsed_response['questions']):
        
        # 정규표현식을 사용해 앞부분의 '숫자. ' 형태 제거
        clean_text_func = lambda x: re.sub(r"^\d+\.\s*", "", x)
        
        step_title = f"질문 {idx + 1}/{total_q}. {q['question_text']}"
        prompt_text = "🎯 가장 마음에 드는 선택지의 번호를 입력하세요: "
        
        # 미리 만들어둔 select_item 함수 호출
        choice_num = select_item(
            step_title=step_title,
            items=q['options'],
            format_func=clean_text_func,
            prompt_text=prompt_text
        )
        
        selected_option = clean_text_func(q['options'][choice_num - 1])
        
        collected_answers.append({
            "question": q['question_text'],
            "answer": selected_option
        })

    # 최종 결과 확인 출력
    print("\n" + "=" * 100)
    print(f"✅ [{title}] 완료! 다음 단계로 넘어갈 준비가 되었습니다.")
    for i, item in enumerate(collected_answers):
        print(f"\nQ{i+1}. {item['question']}")
        print(f"👉 A: {item['answer']}")
        
    # 수집된 답변 리스트를 반환
    return collected_answers

# 인터뷰 답변 리스트를 프롬프트에 삽입하기 좋은 텍스트 형태로 변환하는 함수
def format_interview_responses(answers_list):
    interview_text = ""
    for i, qa in enumerate(answers_list):
        interview_text += f"Q{i+1}. {qa['question']}\nA: {qa['answer']}\n\n"
        
    # 마지막에 추가된 불필요한 줄바꿈(\n\n)을 깔끔하게 제거하고 반환합니다.
    return interview_text.strip()