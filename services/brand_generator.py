import os
import uuid
import json
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

from google import genai
from google.genai import types

from utils.parser import extract_json
from utils.logger import get_logger, get_tracker

logger = get_logger("NameTag.BrandGenerator")

# 응답 저장 디렉토리 설정
RESPONSES_DIR = Path(__file__).parent.parent / "logs" / "ai_responses"
RESPONSES_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """당신은 전문 브랜드 디렉터입니다.
사용자의 정보를 바탕으로 초기 스타트업/1인 기업의 브랜드 정체성을 설계합니다.
반드시 지정된 JSON 형식만 출력하고, 다른 텍스트는 포함하지 마세요."""


def save_ai_response(response_text: str, response_type: str, session_id: str) -> tuple[str, str]:
    """
    AI 응답을 txt와 JSON 파일로 저장.
    
    Args:
        response_text: AI 응답 텍스트
        response_type: 응답 유형 ('logo_variables' 또는 'brand_identity')
        session_id: 세션 ID
    
    Returns:
        tuple: (txt_file_path, json_file_path)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{response_type}_{timestamp}_{session_id[:8]}"
    
    # TXT 파일 저장 (전체 응답)
    txt_file = RESPONSES_DIR / f"{base_filename}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(response_text)
    
    # JSON 파일 저장 (예쁘게 포맷팅)
    json_file = RESPONSES_DIR / f"{base_filename}.json"
    try:
        parsed = json.loads(response_text)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)
    except:
        # JSON 파싱 실패시 그냥 원본 저장
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(response_text)
    
    logger.info(f"✅ Response saved:")
    logger.info(f"   📄 TXT: {txt_file}")
    logger.info(f"   📋 JSON: {json_file}")
    
    return str(txt_file), str(json_file)


# 무드별 자동 매핑 테이블
MOOD_MAPPING = {
    "모던 & 신뢰": {
        "brand_color": "#333333",
        "font_style": "기하학적 산세리프",
        "symbol_type": "기하학적",
    },
    "따뜻 & 친근": {
        "brand_color": "#C8553D",
        "font_style": "부드러운 산세리프",
        "symbol_type": "유기적",
    },
    "미니멀 & 프리미엄": {
        "brand_color": "#1A1A1A",
        "font_style": "얇은 세리프",
        "symbol_type": "미니멀",
    },
    "자연 & 지속가능": {
        "brand_color": "#2D6A4F",
        "font_style": "유기적 산세리프",
        "symbol_type": "유기적",
    },
    "에너지 & 역동": {
        "brand_color": "#0077B6",
        "font_style": "굵은 산세리프",
        "symbol_type": "기하학적",
    },
    "부드러움 & 케어": {
        "brand_color": "#D4829A",
        "font_style": "라운드 산세리프",
        "symbol_type": "유기적",
    },
    "혁신 & 기술": {
        "brand_color": "#6B4EFF",
        "font_style": "모던 기하학",
        "symbol_type": "추상적",
    },
    "클래식 & 전통": {
        "brand_color": "#003153",
        "font_style": "클래식 세리프",
        "symbol_type": "레터마크",
    },
}


def build_logo_variables_prompt(
    business_type: str, vibes: list[str], target: str, keywords: str
) -> str:
    """로고 생성에 필요한 모든 변수를 추천받는 프롬프트"""
    # f-string 외부에서 문자열 처리 (백슬래시 이스케이프 문제 해결)
    mood_options = "', '".join(MOOD_MAPPING.keys())
    mood_options = f"'{mood_options}'"

    return f"""사용자가 다음 정보를 입력했습니다:

업종/서비스: {business_type}
브랜드 감성: {', '.join(vibes)}
타겟 고객: {target}
추가 키워드: {keywords or '없음'}

이 정보를 바탕으로 로고 생성에 필요한 다음 변수들을 추천해주세요.
반드시 아래 JSON 형식으로만 응답하세요:

{{
  "brand_identity": {{
    "brand_name": "추천 브랜드명",
    "brand_name_meaning": "브랜드명의 의미 1-2문장",
    "brand_topic": "구체적인 사업 주제 또는 업종 설명",
    "core_value": "브랜드 핵심 가치 1-2개 (쉼표 구분)",
    "slogan": "핵심 슬로건 (10단어 이내)"
  }},
  "logo_variables": {{
    "target_mood": "다음 중 선택: {mood_options}",
    "brand_color": "컬러 코드 (예: #2D6A4F) 또는 색상 설명",
    "font_style": "선택: 기하학적 산세리프 / 클래식 세리프 / 손글씨 느낌 / 굵고 강한 / 얇고 우아한",
    "symbol_type": "선택: 기하학적 / 유기적 / 아이콘형 / 추상적 / 레터마크",
    "logo_type": "선택: 심볼+텍스트 조합 / 심볼만 / 텍스트만 / 배지형",
    "background": "선택: 흰색 / 검정 / 브랜드 색상 / 투명"
  }},
  "recommendations_reason": "이 변수들을 추천한 이유 2-3문장"
}}"""


def build_user_prompt(business_type: str, vibes: list[str], target: str, keywords: str) -> str:
    return f"""업종/서비스: {business_type}
브랜드 감성: {', '.join(vibes)}
타겟 고객: {target}
추가 키워드: {keywords or '없음'}

아래 JSON 형식으로만 응답하세요:
⚠️ IMPORTANT: 각 브랜드마다 고유한 typography, character, logo_design을 개별적으로 생성해야 합니다!

{{
  "brands": [
    {{
      "name": "브랜드명 1",
      "meaning": "이름의 의미와 어원 1-2문장",
      "story": "고객 감성을 자극하는 스토리 2-3문장",
      "slogan": "핵심 슬로건 10단어 이내",
      "typography": {{
        "korean": "추천 한글 폰트명 (나눔명조, 프리텐다드, 고도체 등)",
        "english": "추천 영문 폰트명 (Playfair Display, DM Sans 등)",
        "reason": "이 브랜드명에 어울리는 폰트 선택 이유 2문장"
      }},
      "character": {{
        "name": "캐릭터 이름",
        "concept": "이 브랜드의 컨셉을 담은 캐릭터 한 줄",
        "personality": "성격 특징 3가지, 쉼표로 구분",
        "visual": "외형 묘사 2-3문장"
      }},
      "logo_design": {{
        "brand_name": "브랜드명 1",
        "brand_topic": "사업 주제 또는 업종",
        "core_value": "이 브랜드의 핵심 가치 1~2개",
        "target_mood": "이 브랜드에 어울리는 감성",
        "symbol_type": "심볼 스타일 선호도",
        "font_style": "서체 느낌 선호도",
        "font_reference": "참고할 폰트 레퍼런스",
        "font_weight": "폰트 굵기",
        "brand_color": "로고/브랜드 메인 색상",
        "logo_type": "로고 구성 방식",
        "background": "로고 배경 색상"
      }}
    }},
    {{
      "name": "브랜드명 2",
      "meaning": "...",
      "story": "...",
      "slogan": "...",
      "typography": {{ "korean": "...", "english": "...", "reason": "..." }},
      "character": {{ "name": "...", "concept": "...", "personality": "...", "visual": "..." }},
      "logo_design": {{ "brand_name": "...", "brand_topic": "...", "core_value": "...", "target_mood": "...", "symbol_type": "...", "font_style": "...", "font_reference": "...", "font_weight": "...", "brand_color": "...", "logo_type": "...", "background": "..." }}
    }},
    {{
      "name": "브랜드명 3",
      "meaning": "...",
      "story": "...",
      "slogan": "...",
      "typography": {{ "korean": "...", "english": "...", "reason": "..." }},
      "character": {{ "name": "...", "concept": "...", "personality": "...", "visual": "..." }},
      "logo_design": {{ "brand_name": "...", "brand_topic": "...", "core_value": "...", "target_mood": "...", "symbol_type": "...", "font_style": "...", "font_reference": "...", "font_weight": "...", "brand_color": "...", "logo_type": "...", "background": "..." }}
    }}
  ]
}}"""


def _get_model() -> tuple[genai.Client, str]:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()
    client = genai.Client(api_key=api_key)
    return client, model_name


def generate_logo_variables(
    business_type: str,
    vibes: list[str],
    target: str,
    keywords: str = "",
    session_id: Optional[str] = None,
) -> dict[str, Any]:
    """
    로고 생성에 필요한 모든 변수를 AI로부터 추천받기.
    
    Returns:
        dict with brand_identity, logo_variables, recommendations_reason
    """
    session_id = session_id or str(uuid.uuid4())
    tracker = get_tracker(session_id)

    logger.info(f"🚀 Starting logo variable generation (session: {session_id})")
    tracker.log_step("init_logo_variables", {
        "business_type": business_type,
        "vibes": vibes,
        "target": target,
    })

    try:
        client, model_name = _get_model()

        # Step 1: AI에 변수 추천 요청
        logger.info("📝 Requesting logo variables from AI...")
        tracker.log_step("ai_request", {"model": model_name})

        response = client.models.generate_content(
            model=model_name,
            contents=build_logo_variables_prompt(business_type, vibes, target, keywords),
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        
        raw_ai_response = response.text or ""
        
        # ✨ AI 응답 저장 (txt + JSON)
        try:
            txt_path, json_path = save_ai_response(raw_ai_response, "logo_variables", session_id)
        except Exception as e:
            logger.warning(f"⚠️ Failed to save response files: {e}")
        
        # 로그에 전체 응답 출력 (여러 줄로 분할)
        logger.info("=" * 100)
        logger.info("📨 AI FULL RESPONSE (AI 전체 응답)")
        logger.info("=" * 100)
        try:
            parsed = json.loads(raw_ai_response)
            pretty_json = json.dumps(parsed, indent=2, ensure_ascii=False)
            for line in pretty_json.split('\n'):
                logger.info(line)
        except:
            # JSON이 아닐 경우 그냥 출력
            for line in raw_ai_response.split('\n'):
                logger.info(line)
        logger.info("=" * 100)

        # Step 2: 응답 파싱
        result = extract_json(raw_ai_response)
        if result is None:
            raise ValueError(f"JSON 파싱 실패. 원본 응답:\n{raw_ai_response[:500]}")

        # Step 3: 필수 키 확인
        required_keys = {"brand_identity", "logo_variables"}
        if not required_keys.issubset(result.keys()):
            missing = required_keys - set(result.keys())
            raise ValueError(f"응답에 필수 키가 없습니다: {missing}")

        # Step 4: 변수 추적
        brand_identity = result.get("brand_identity", {})
        logo_variables = result.get("logo_variables", {})

        # 브랜드 정체성 변수 기록
        for key, value in brand_identity.items():
            tracker.set_variable(
                f"BRAND_{key.upper()}",
                value,
                source="ai_response",
            )

        # 로고 변수 기록
        for key, value in logo_variables.items():
            tracker.set_variable(
                f"LOGO_{key.upper()}",
                value,
                source="ai_response",
            )

        # Step 5: TARGET_MOOD에 따른 자동 매핑 값 설정
        target_mood = logo_variables.get("target_mood", "")
        if target_mood in MOOD_MAPPING:
            mood_defaults = MOOD_MAPPING[target_mood]
            
            # 사용자가 지정하지 않은 값은 자동 추천값으로 설정
            if not logo_variables.get("brand_color") or logo_variables.get("brand_color") == "":
                logo_variables["brand_color"] = mood_defaults["brand_color"]
                tracker.set_variable("LOGO_BRAND_COLOR", mood_defaults["brand_color"], source="auto_inferred")
            
            if not logo_variables.get("font_style") or logo_variables.get("font_style") == "":
                logo_variables["font_style"] = mood_defaults["font_style"]
                tracker.set_variable("LOGO_FONT_STYLE", mood_defaults["font_style"], source="auto_inferred")
            
            if not logo_variables.get("symbol_type") or logo_variables.get("symbol_type") == "":
                logo_variables["symbol_type"] = mood_defaults["symbol_type"]
                tracker.set_variable("LOGO_SYMBOL_TYPE", mood_defaults["symbol_type"], source="auto_inferred")

            logger.info(f"✅ Mood-based defaults applied for: {target_mood}")

        tracker.log_step("variables_compiled", {
            "brand_variables": len(brand_identity),
            "logo_variables": len(logo_variables),
        })

        logger.info(f"✅ Logo variables generated successfully")
        logger.info(f"📊 Tracked Variables: {tracker.get_all_variables()}")

        return {
            "session_id": session_id,
            "brand_identity": brand_identity,
            "logo_variables": logo_variables,
            "recommendations_reason": result.get("recommendations_reason", ""),
            "variables_summary": tracker.get_all_variables(),
        }

    except Exception as e:
        logger.error(f"❌ Error in generate_logo_variables: {str(e)}", exc_info=True)
        raise


def generate_brand_identity(
    business_type: str,
    vibes: list[str],
    target: str,
    keywords: str = "",
    session_id: Optional[str] = None,
) -> dict[str, Any]:
    session_id = session_id or str(uuid.uuid4())
    tracker = get_tracker(session_id)

    logger.info(f"🚀 Starting brand identity generation (session: {session_id})")
    
    client, model_name = _get_model()
    response = client.models.generate_content(
        model=model_name,
        contents=build_user_prompt(business_type, vibes, target, keywords),
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    raw_text = response.text or ""

    # ✨ AI 응답 저장 (txt + JSON)
    try:
        txt_path, json_path = save_ai_response(raw_text, "brand_identity", session_id)
    except Exception as e:
        logger.warning(f"⚠️ Failed to save response files: {e}")
    
    # 로그에 전체 응답 출력 (여러 줄로 분할)
    logger.info("=" * 100)
    logger.info("📨 AI FULL RESPONSE (AI 전체 응답)")
    logger.info("=" * 100)
    try:
        parsed = json.loads(raw_text)
        pretty_json = json.dumps(parsed, indent=2, ensure_ascii=False)
        for line in pretty_json.split('\n'):
            logger.info(line)
    except:
        # JSON이 아닐 경우 그냥 출력
        for line in raw_text.split('\n'):
            logger.info(line)
    logger.info("=" * 100)

    result = extract_json(raw_text)
    if result is None:
        raise ValueError(f"JSON 파싱 실패. 원본 응답:\n{raw_text[:500]}")

    required_keys = {"brands"}
    if not required_keys.issubset(result.keys()):
        missing = required_keys - set(result.keys())
        raise ValueError(f"응답에 필수 키가 없습니다: {missing}")

    # Validate each brand has required fields
    brands = result.get("brands", [])
    if not brands:
        raise ValueError("브랜드 데이터가 없습니다")
    
    for idx, brand in enumerate(brands):
        brand_required = {"name", "meaning", "story", "slogan", "typography", "character", "logo_design"}
        if not brand_required.issubset(set(brand.keys())):
            missing = brand_required - set(brand.keys())
            raise ValueError(f"브랜드 {idx+1}에 필수 필드가 없습니다: {missing}")

    # Track brand identity results - 각 브랜드별로 추적
    for idx, brand in enumerate(brands, 1):
        prefix = f"BRAND_{idx}"
        
        # 기본 정보
        tracker.set_variable(f"{prefix}_NAME", brand.get("name"), source="ai_response")
        tracker.set_variable(f"{prefix}_MEANING", brand.get("meaning"), source="ai_response")
        tracker.set_variable(f"{prefix}_STORY", brand.get("story"), source="ai_response")
        tracker.set_variable(f"{prefix}_SLOGAN", brand.get("slogan"), source="ai_response")
        
        # Typography 정보
        if "typography" in brand:
            typography = brand["typography"]
            tracker.set_variable(f"{prefix}_TYPOGRAPHY_KOREAN", typography.get("korean"), source="ai_response")
            tracker.set_variable(f"{prefix}_TYPOGRAPHY_ENGLISH", typography.get("english"), source="ai_response")
            tracker.set_variable(f"{prefix}_TYPOGRAPHY_REASON", typography.get("reason"), source="ai_response")
        
        # Character 정보
        if "character" in brand:
            character = brand["character"]
            tracker.set_variable(f"{prefix}_CHARACTER_NAME", character.get("name"), source="ai_response")
            tracker.set_variable(f"{prefix}_CHARACTER_CONCEPT", character.get("concept"), source="ai_response")
            tracker.set_variable(f"{prefix}_CHARACTER_PERSONALITY", character.get("personality"), source="ai_response")
            tracker.set_variable(f"{prefix}_CHARACTER_VISUAL", character.get("visual"), source="ai_response")
        
        # Logo Design 정보
        if "logo_design" in brand:
            logo_design = brand["logo_design"]
            for key, value in logo_design.items():
                tracker.set_variable(f"{prefix}_LOGO_DESIGN_{key.upper()}", value, source="ai_response")

    # 상세 로깅: 모든 섹션 출력
    logger.info("=" * 80)
    logger.info("✅ PARSED RESULT (파싱된 결과)")
    logger.info("=" * 80)
    
    for idx, brand in enumerate(brands, 1):
        logger.info(f"\n📝 BRAND {idx}: {brand.get('name')}")
        logger.info(f"  Meaning: {brand.get('meaning')}")
        logger.info(f"  Story: {brand.get('story')}")
        logger.info(f"  Slogan: {brand.get('slogan')}")
        
        if "typography" in brand:
            typography = brand["typography"]
            logger.info(f"  🔤 Typography:")
            logger.info(f"     Korean: {typography.get('korean')}")
            logger.info(f"     English: {typography.get('english')}")
            logger.info(f"     Reason: {typography.get('reason')}")
        
        if "character" in brand:
            character = brand["character"]
            logger.info(f"  🎭 Character:")
            logger.info(f"     Name: {character.get('name')}")
            logger.info(f"     Concept: {character.get('concept')}")
            logger.info(f"     Personality: {character.get('personality')}")
            logger.info(f"     Visual: {character.get('visual')}")
        
        if "logo_design" in brand:
            logger.info(f"  🎨 Logo Design:")
            logo = brand["logo_design"]
            for key, value in logo.items():
                logger.info(f"     {key}: {value}")
    
    logger.info("=" * 80)

    logger.info(f"✅ Brand identity generated successfully")

    return result


def create_logo_prompt(
    brand_name: str,
    brand_topic: str,
    core_value: str,
    target_mood: str,
    symbol_type: str,
    font_style: str,
    font_reference: str,
    font_weight: str,
    brand_color: str,
    logo_type: str,
    background: str
) -> str:
    """로고 디자인 프롬프트 생성"""
    
    prompt = f"""You are a professional logo designer specializing in brand identity 
for early-stage startups. Create a clean, vector-style logo with 
the following precise specifications:

**BRAND CONTEXT**
Brand Name: {brand_name}
Industry/Topic: {brand_topic}
Core Values: {core_value}
Brand Mood: {target_mood}

**SYMBOL DESIGN**
Style: {symbol_type} — design a symbol that visually represents 
{brand_topic} through {symbol_type} shapes and forms.
The symbol must feel original, not generic or stock-image-like.
It should communicate {core_value} at first glance.
Avoid literal representations — use abstraction to elevate meaning.

**TYPOGRAPHY**
Font style: {font_style} typeface (similar to {font_reference})
Brand name "{brand_name}" centered below the symbol.
Letter spacing: slightly wide for modern feel.
Weight: {font_weight} — balanced with symbol weight.
Text size ratio to symbol: approximately 1:2 (text:symbol height).

**COLOR**
Primary: {brand_color}
Background: {background}
Use a maximum of 2 colors total. 
No gradients unless specified.
High contrast for print and digital readability.

**COMPOSITION**
Logo type: {logo_type}
Alignment: centered, perfectly symmetrical.
Padding: equal whitespace on all sides.
The symbol and text must feel like one unified system, not two 
separate elements placed together.

**QUALITY REQUIREMENTS**
- Vector-style sharp edges, no blur or soft shadows
- Matte finish texture (no gloss or metallic shine)
- High contrast, legible at both 16px and 500px sizes
- Clean, minimal — no decorative elements beyond the core concept
- White space is intentional and generous
- Final output should feel like a professional brand identity, 
  not a generic AI-generated logo

**BACKGROUND**
{background} — completely flat, no texture or noise."""

    return prompt


def generate_logo_image(
    brand_name: str,
    brand_topic: str,
    core_value: str,
    target_mood: str,
    symbol_type: str,
    font_style: str,
    font_reference: str,
    font_weight: str,
    brand_color: str,
    logo_type: str,
    background: str,
    session_id: Optional[str] = None,
) -> tuple[bytes, str]:
    """
    로고 이미지 생성.
    
    Args:
        brand_name: 브랜드 이름
        brand_topic: 사업 주제
        core_value: 핵심 가치
        target_mood: 타겟 감성
        symbol_type: 심볼 스타일
        font_style: 서체 스타일
        font_reference: 참고 폰트
        font_weight: 폰트 굵기
        brand_color: 브랜드 색상
        logo_type: 로고 타입
        background: 배경 색상
        session_id: 세션 ID
    
    Returns:
        tuple: (이미지 바이트, 파일명)
    """
    session_id = session_id or str(uuid.uuid4())
    logger.info(f"🎨 Generating logo image for brand: {brand_name} (session: {session_id})")
    
    try:
        client, model_name = _get_model()
        
        # 로고 프롬프트 생성
        prompt = create_logo_prompt(
            brand_name=brand_name,
            brand_topic=brand_topic,
            core_value=core_value,
            target_mood=target_mood,
            symbol_type=symbol_type,
            font_style=font_style,
            font_reference=font_reference,
            font_weight=font_weight,
            brand_color=brand_color,
            logo_type=logo_type,
            background=background,
        )
        
        logger.info("📝 Calling Gemini API for logo generation...")
        
        # 이미지 생성 (gemini-3.1-flash-image-preview 모델)
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[prompt],
        )
        
        # 응답에서 이미지 추출
        image_data = None
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                # 이미지 바이트 데이터 추출
                image_data = image.data
                break
        
        if not image_data:
            raise ValueError("이미지 생성에 실패했습니다: 응답에 이미지가 없습니다")
        
        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logo_{brand_name}_{timestamp}_{session_id[:8]}.png"
        
        # 로그 저장
        logo_dir = Path(__file__).parent.parent / "logs" / "generated_logos"
        logo_dir.mkdir(parents=True, exist_ok=True)
        logo_path = logo_dir / filename
        
        with open(logo_path, 'wb') as f:
            f.write(image_data)
        
        logger.info(f"✅ Logo image saved: {logo_path}")
        
        return image_data, filename
    
    except Exception as e:
        logger.error(f"❌ Logo generation error: {str(e)}", exc_info=True)
        raise
