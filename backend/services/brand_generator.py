"""Brand identity generation service."""
import base64
import io
import json
import logging
import os
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types
from PIL import Image

from utils.parser import extract_json
from utils.prompt_loader import (
    get_logo_prompt_template,
    get_character_prompt_template,
    replace_variables,
    get_mood_mapping_table,
)

# Setup logging
logger = logging.getLogger("NameTag.BrandGenerator")

# Create response logs directory
RESPONSE_LOG_DIR = Path(__file__).parent.parent.parent / "logs" / "ai_responses"
RESPONSE_LOG_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """당신은 전문 브랜드 디렉터입니다.
사용자의 정보를 바탕으로 초기 스타트업/1인 기업의 브랜드 정체성을 설계합니다.
반드시 지정된 JSON 형식만 출력하고, 다른 텍스트는 포함하지 마세요."""


def build_user_prompt(business_type: str, vibes: list[str], target: str, keywords: str) -> str:
    """Build the user prompt for Gemini API."""
    return f"""업종/서비스: {business_type}
브랜드 감성: {', '.join(vibes)}
타겟 고객: {target}
추가 키워드: {keywords or '없음'}

아래 JSON 형식으로만 응답하세요:

{{
  "brands": [
    {{
      "name": "브랜드명",
      "meaning": "이름의 의미와 어원 1-2문장",
      "story": "고객 감성을 자극하는 스토리 2-3문장",
      "slogan": "핵심 슬로건 10단어 이내"
    }},
    {{ "name": "두번째 브랜드명", "meaning": "...", "story": "...", "slogan": "..." }},
    {{ "name": "세번째 브랜드명", "meaning": "...", "story": "...", "slogan": "..." }}
  ],
  "typography": [
    {{
      "korean": "추천 한글 폰트명 (나눔명조, 프리텐다드, 고도체 등)",
      "english": "추천 영문 폰트명 (Playfair Display, DM Sans 등)",
      "reason": "선택 이유 2문장"
    }},
    {{
      "korean": "두번째 한글 폰트명",
      "english": "두번째 영문 폰트명",
      "reason": "두번째 선택 이유 2문장"
    }},
    {{
      "korean": "세번째 한글 폰트명",
      "english": "세번째 영문 폰트명",
      "reason": "세번째 선택 이유 2문장"
    }}
  ],
  "character": [
    {{
      "name": "캐릭터 이름",
      "concept": "컨셉 한 줄",
      "personality": "성격 특징 3가지, 쉼표로 구분",
      "visual": "외형 묘사 2-3문장"
    }},
    {{
      "name": "두번째 캐릭터 이름",
      "concept": "두번째 컨셉 한 줄",
      "personality": "두번째 성격 특징 3가지, 쉼표로 구분",
      "visual": "두번째 외형 묘사 2-3문장"
    }},
    {{
      "name": "세번째 캐릭터 이름",
      "concept": "세번째 컨셉 한 줄",
      "personality": "세번째 성격 특징 3가지, 쉼표로 구분",
      "visual": "세번째 외형 묘사 2-3문장"
    }}
  ],
  "logo_design": [
    {{
      "brand_name": "브랜드/서비스 이름",
      "brand_topic": "사업 주제 또는 업종",
      "core_value": "브랜드가 전달하고 싶은 핵심 가치 1~2개",
      "target_mood": "원하는 브랜드 감성 (예: 모던하고 혁신적인 기술)",
      "symbol_type": "심볼 스타일 선호도 (예: 기하학적 수렴 다이어그램)",
      "font_style": "서체 느낌 선호도 (예: 산세리프)",
      "font_reference": "참고할 폰트 레퍼런스 (예: Helvetica Neue)",
      "font_weight": "폰트 굵기 (예: bold)",
      "brand_color": "로고/브랜드 메인 색상 (예: 흰색)",
      "logo_type": "로고 구성 방식 (예: 심볼+텍스트 조합)",
      "background": "로고 배경 색상 (예: 검은색)"
    }},
    {{
      "brand_name": "두번째 브랜드명",
      "brand_topic": "두번째 사업 주제",
      "core_value": "두번째 핵심 가치",
      "target_mood": "두번째 브랜드 감성",
      "symbol_type": "두번째 심볼 스타일",
      "font_style": "두번째 서체 느낌",
      "font_reference": "두번째 폰트 레퍼런스",
      "font_weight": "두번째 폰트 굵기",
      "brand_color": "두번째 브랜드 색상",
      "logo_type": "두번째 로고 구성",
      "background": "두번째 배경 색상"
    }},
    {{
      "brand_name": "세번째 브랜드명",
      "brand_topic": "세번째 사업 주제",
      "core_value": "세번째 핵심 가치",
      "target_mood": "세번째 브랜드 감성",
      "symbol_type": "세번째 심볼 스타일",
      "font_style": "세번째 서체 느낌",
      "font_reference": "세번째 폰트 레퍼런스",
      "font_weight": "세번째 폰트 굵기",
      "brand_color": "세번째 브랜드 색상",
      "logo_type": "세번째 로고 구성",
      "background": "세번째 배경 색상"
    }}
  ]
}}"""


def _get_model() -> tuple[genai.Client, str]:
    """Get Gemini client and model name."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()
    client = genai.Client(api_key=api_key)
    return client, model_name


def generate_brand_identity(
    business_type: str,
    vibes: list[str],
    target: str,
    keywords: str = "",
) -> dict[str, Any]:
    """
    Generate brand identity using Gemini API.

    Args:
        business_type: Type of business/service
        vibes: List of brand vibes
        target: Target customer description
        keywords: Additional keywords

    Returns:
        Dictionary with brands, typography, and character

    Raises:
        RuntimeError: If API key is not set
        ValueError: If JSON parsing fails
    """
    client, model_name = _get_model()
    response = client.models.generate_content(
        model=model_name,
        contents=build_user_prompt(business_type, vibes, target, keywords),
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    raw_text = response.text or ""

    # Log entire AI response - Pretty printed
    logger.info("=" * 100)
    logger.info("📨 FULL AI RESPONSE (AI 전체 응답)")
    logger.info("=" * 100)
    
    # Try to parse and pretty print JSON
    try:
        parsed_for_display = json.loads(raw_text)
        pretty_json = json.dumps(parsed_for_display, indent=2, ensure_ascii=False)
        # Log each line to preserve formatting
        for line in pretty_json.split('\n'):
            logger.info(line)
    except:
        # If not valid JSON, log as is
        logger.info(raw_text)
    
    logger.info("=" * 100)

    # Save raw response to file
    try:
        import uuid
        from datetime import datetime
        
        response_file = RESPONSE_LOG_DIR / f"brand_identity_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}.json"
        with open(response_file, 'w', encoding='utf-8') as f:
            # Save pretty printed version
            try:
                parsed = json.loads(raw_text)
                f.write(json.dumps(parsed, indent=2, ensure_ascii=False))
            except:
                f.write(raw_text)
        logger.info(f"💾 Raw response saved to: {response_file}")
    except Exception as e:
        logger.warning(f"Failed to save raw response: {e}")

    result = extract_json(raw_text)
    if result is None:
        raise ValueError(f"JSON 파싱 실패. 원본 응답:\n{raw_text[:500]}")

    required_keys = {"brands", "typography", "character", "logo_design"}
    if not required_keys.issubset(result.keys()):
        missing = required_keys - set(result.keys())
        raise ValueError(f"응답에 필수 키가 없습니다: {missing}")

    # Log parsed result with all sections
    logger.info("=" * 80)
    logger.info("✅ PARSED RESULT (파싱된 결과)")
    logger.info("=" * 80)
    
    # Log each section separately
    if result.get("brands"):
        logger.info("📝 BRANDS (브랜드 목록):")
        for i, brand in enumerate(result["brands"], 1):
            logger.info(f"  [{i}] Name: {brand.get('name')}")
            logger.info(f"      Meaning: {brand.get('meaning')}")
            logger.info(f"      Story: {brand.get('story')}")
            logger.info(f"      Slogan: {brand.get('slogan')}")
    
    if result.get("typography"):
        logger.info("🔤 TYPOGRAPHY (타이포그래피):")
        typographies = result["typography"]
        # Handle both array and single object for backward compatibility
        if isinstance(typographies, list):
            for i, typography in enumerate(typographies, 1):
                logger.info(f"  [{i}] Korean Font: {typography.get('korean')}")
                logger.info(f"       English Font: {typography.get('english')}")
                logger.info(f"       Reason: {typography.get('reason')}")
        else:
            logger.info(f"  Korean Font: {typographies.get('korean')}")
            logger.info(f"  English Font: {typographies.get('english')}")
            logger.info(f"  Reason: {typographies.get('reason')}")
    
    if result.get("character"):
        logger.info("🎭 CHARACTER (캐릭터):")
        characters = result["character"]
        # Handle both array and single object for backward compatibility
        if isinstance(characters, list):
            for i, character in enumerate(characters, 1):
                logger.info(f"  [{i}] Name: {character.get('name')}")
                logger.info(f"       Concept: {character.get('concept')}")
                logger.info(f"       Personality: {character.get('personality')}")
                logger.info(f"       Visual: {character.get('visual')}")
        else:
            logger.info(f"  Name: {characters.get('name')}")
            logger.info(f"  Concept: {characters.get('concept')}")
            logger.info(f"  Personality: {characters.get('personality')}")
            logger.info(f"  Visual: {characters.get('visual')}")
    
    if result.get("logo_design"):
        logger.info("🎨 LOGO DESIGN (로고 설계):")
        logo_designs = result["logo_design"]
        # Handle both array and single object for backward compatibility
        if isinstance(logo_designs, list):
            for i, logo in enumerate(logo_designs, 1):
                logger.info(f"  [{i}]")
                for key, value in logo.items():
                    logger.info(f"      {key}: {value}")
        else:
            for key, value in logo_designs.items():
                logger.info(f"  {key}: {value}")
    
    logger.info("=" * 80)

    return result


def generate_logo_image(brand_name: str, brand_story: str, vibes: list[str], symbol_type: str = "기하학적", brand_color: str = "", logo_type: str = "심볼+텍스트 조합", background: str = "흰색") -> str:
    """
    Generate a logo image using Gemini 3.1 Flash Image API with detailed specifications.

    Args:
        brand_name: Name of the brand
        brand_story: Story/description of the brand
        vibes: List of brand vibes
        symbol_type: Symbol style (기하학적, 유기적, 미니멀, 아이콘형, 레터마크)
        brand_color: Brand color (auto-mapped if empty)
        logo_type: Logo composition (심볼+텍스트 조합, 심볼만, 텍스트만, 배지형)
        background: Background color (흰색, 검정, 투명)

    Returns:
        Base64 encoded image string

    Raises:
        RuntimeError: If API key is not set
        ValueError: If image generation fails
    """
    # Use dedicated image generation API key from environment
    image_api_key = os.getenv("GEMINI_IMAGE_API_KEY", "").strip()
    if not image_api_key:
        raise RuntimeError("GEMINI_IMAGE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    client = genai.Client(api_key=image_api_key)

    # Get mood mapping for auto color assignment
    target_mood = vibes[0] if vibes else "모던 & 신뢰"
    if not brand_color:
        mood_map = get_mood_mapping_table()
        mood_data = mood_map.get(f"MOOD-{list(mood_map.keys())[0]}", {})
        brand_color = mood_data.get("color", "검정")

    prompt = f"""당신은 초기 스타트업 브랜드 아이덴티티를 전문으로 하는 
전문 로고 디자이너입니다. 아래 사양에 따라 
깔끔하고 벡터 스타일의 로고를 생성해주세요.

**브랜드 맥락**
브랜드명: {brand_name}
업종/주제: {brand_story}
핵심 가치: {', '.join(vibes)}
브랜드 무드: {target_mood}

**심볼 디자인**
스타일: {symbol_type}
{brand_story}을 {symbol_type} 형태로 시각화한 심볼을 디자인하세요.
심볼은 {', '.join(vibes)}를 첫눈에 전달해야 합니다.
진부한 스톡 이미지 느낌이 아닌, 독창적인 형태를 사용하세요.
직관적인 표현보다 추상적 표현으로 품격을 높이세요.

**타이포그래피**
서체 스타일: 기하학적 산세리프 (모던한 느낌)
심볼 아래 중앙 정렬로 '{brand_name}' 텍스트 배치
자간: 현대적 느낌을 위해 약간 넓게
굵기: 심볼 굵기와 균형 유지
텍스트와 심볼의 높이 비율: 약 1:2

**색상**
주색상: {brand_color}
배경: {background}
최대 2가지 색상만 사용
그라디언트 없음
인쇄 및 디지털 모두에서 높은 대비 유지

**구성**
로고 유형: {logo_type}
정렬: 중앙, 완벽한 대칭
여백: 사방 균등한 여백
심볼과 텍스트는 각각 분리된 요소가 아닌 
하나의 통합된 시스템으로 느껴져야 합니다.

**품질 요구사항**
- 벡터 스타일의 선명한 가장자리, 블러 없음
- 매트 마감 질감 (광택이나 금속 광택 없음)
- 16px와 500px 모두에서 가독성 유지
- 핵심 컨셉 외 장식 요소 없음
- 여백은 의도적으로 넓게
- 결과물은 AI 생성 로고가 아닌 
  전문 브랜드 아이덴티티처럼 느껴져야 함

**배경**
{background} — 완전히 평평하게, 텍스처나 노이즈 없음"""

    try:
        # Use streaming with minimal config
        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        )
        
        # Create Content object like in Test/Image_genaration_Test.py
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
        
        for chunk in client.models.generate_content_stream(
            model="gemini-3.1-flash-image-preview",
            contents=[content],
            config=config,
        ):
            # Check if chunk has parts attribute and if it's not None
            if not hasattr(chunk, 'parts') or chunk.parts is None:
                continue
            if len(chunk.parts) > 0 and hasattr(chunk.parts[0], 'inline_data') and chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
                image_bytes = chunk.parts[0].inline_data.data
                return base64.b64encode(image_bytes).decode("utf-8")
        
        raise ValueError("이미지 생성에 실패했습니다. 응답에 이미지 데이터가 없습니다.")

    except Exception as e:
        raise ValueError(f"로고 이미지 생성 실패: {str(e)}")


def generate_character_image(
    character_name: str, character_concept: str, character_visual: str, vibes: list[str], 
    character_style: str = "플랫 일러스트", character_age_feel: str = "나이 초월", 
    brand_name: str = "", brand_topic: str = "", core_value: str = ""
) -> str:
    """
    Generate a character image using Gemini 3.1 Flash Image API with detailed specifications.

    Args:
        character_name: Name of the character
        character_concept: Concept of the character
        character_visual: Visual description of the character
        vibes: List of brand vibes
        character_style: Illustration style (플랫 일러스트, 손그림 느낌, 2.5D, 3D 렌더, 픽셀아트)
        character_age_feel: Age feeling (어린이, 청소년, 청년, 중장년, 나이 초월)
        brand_name: Brand name for context
        brand_topic: Brand topic for context
        core_value: Core values for context

    Returns:
        Base64 encoded image string

    Raises:
        RuntimeError: If API key is not set
        ValueError: If image generation fails
    """
    # Use dedicated image generation API key from environment
    image_api_key = os.getenv("GEMINI_IMAGE_API_KEY", "").strip()
    if not image_api_key:
        raise RuntimeError("GEMINI_IMAGE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    client = genai.Client(api_key=image_api_key)

    target_mood = vibes[0] if vibes else "따뜻 & 친근"
    brand_context = f"{brand_name} ({brand_topic})" if brand_name else "스타트업"

    prompt = f"""당신은 스타트업과 소비자 앱 전문 브랜드 마스코트 디자이너입니다.
아래 사양에 따라 브랜드 캐릭터/마스코트를 디자인해주세요.

**브랜드 맥락**
브랜드명: {brand_context}
업종/주제: {brand_topic}
핵심 가치: {core_value if core_value else '미정'}
브랜드 무드: {target_mood}

**캐릭터 정체성**
캐릭터 이름: {character_name}
캐릭터 컨셉: {character_concept}
이 캐릭터는 브랜드 그 자체입니다.
단순한 장식이 아닌, 형태와 자세, 표정으로 {', '.join(vibes)}를 구현해야 합니다.

성격: {character_visual}
이 특성을 시각 언어로 번역하세요:
- 신체 비율: {character_visual}의 특성에 맞게
- 표정: 친근하고 따뜻한 느낌
- 자세/제스처: 자연스럽고 매력있게

나이대 느낌: {character_age_feel}

**비주얼 스타일**
일러스트 스타일: {character_style}
색상: 주색상은 차분하고 잔잔한 톤, 포인트 색상 1~2개 추가
선 처리: 깔끔한 아웃라인
음영: 소프트한 그림자 또는 플랫 스타일

**구성**
캐릭터를 중립적 서있는 포즈로 표현 (마스터 포즈)
캐릭터는 약간 뷰어 쪽을 향해 (3/4 각도 권장)
배경 없음 — 투명 또는 순백색
캐릭터가 프레임의 약 70% 차지

**디자인 제약 사항**
- 64x64px 아이콘으로도 인식 가능해야 함
- 특정 문화에만 통용되는 요소 사용 금지
- 텍스트는 캐릭터 디자인에 포함되지 않음
- 흑백(모노크롬)으로도 작동 가능해야 함
- 최대 5가지 색상 사용

**기본 표정**
기본 표정: 친근하고 긍정적인 느낌
공격적이거나 과하게 흥분한 표정 금지

**결과물**
하나의 캐릭터만 흰색 배경에
마스터 포즈 (서있거나 떠있고, 뷰어를 향함)
고해상도, 벡터 스타일 품질"""

    try:
        # Use streaming with minimal config
        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        )
        
        # Create Content object like in Test/Image_genaration_Test.py
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
        
        for chunk in client.models.generate_content_stream(
            model="gemini-3.1-flash-image-preview",
            contents=[content],
            config=config,
        ):
            # Check if chunk has parts attribute and if it's not None
            if not hasattr(chunk, 'parts') or chunk.parts is None:
                continue
            if len(chunk.parts) > 0 and hasattr(chunk.parts[0], 'inline_data') and chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
                image_bytes = chunk.parts[0].inline_data.data
                return base64.b64encode(image_bytes).decode("utf-8")
        
        raise ValueError("이미지 생성에 실패했습니다. 응답에 이미지 데이터가 없습니다.")

    except Exception as e:
        raise ValueError(f"캐릭터 이미지 생성 실패: {str(e)}")


def generate_logo_image_with_context(
    brand_name: str,
    brand_topic: str,
    core_value: str,
    vibes: list[str],
    brand_color: str = "",
    symbol_type: str = "기하학적",
    logo_type: str = "심볼+텍스트 조합",
    background: str = "흰색",
) -> str:
    """
    Generate a professional logo image using Name Tag prompt template.

    Uses the prompt template from Prompt/네임텍 로고 캐릭터 생성 프롬프트.md
    to create a high-quality logo with detailed specifications.

    Args:
        brand_name: Name of the brand
        brand_topic: Topic/business type
        core_value: Core brand values
        vibes: List of brand vibes (감성)
        brand_color: Preferred brand color (auto-mapped if empty)
        symbol_type: Symbol style (기하학적, 유기적, 미니멀, etc.)
        logo_type: Logo composition type (심볼+텍스트 조합, 심볼만, etc.)
        background: Background color (흰색, 검정, 투명, etc.)

    Returns:
        Base64 encoded logo image string

    Raises:
        RuntimeError: If API key is not set
        ValueError: If image generation fails
    """
    # Use dedicated image generation API key from environment
    image_api_key = os.getenv("GEMINI_IMAGE_API_KEY", "").strip()
    if not image_api_key:
        raise RuntimeError("GEMINI_IMAGE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    client = genai.Client(api_key=image_api_key)

    # Get template and replace variables
    # For mood mapping, use the first vibe as target mood
    target_mood = vibes[0] if vibes else "모던 & 신뢰"

    template = get_logo_prompt_template()
    prompt = replace_variables(
        template=template,
        brand_name=brand_name,
        brand_topic=brand_topic,
        core_value=core_value,
        target_mood=target_mood,
        brand_color=brand_color,
        symbol_type=symbol_type,
        logo_type=logo_type,
        background=background,
    )

    try:
        # Use streaming with minimal config
        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        )
        
        # Create Content object like in Test/Image_genaration_Test.py
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
        
        for chunk in client.models.generate_content_stream(
            model="gemini-3.1-flash-image-preview",
            contents=[content],
            config=config,
        ):
            # Check if chunk has parts attribute and if it's not None
            if not hasattr(chunk, 'parts') or chunk.parts is None:
                continue
            if len(chunk.parts) > 0 and hasattr(chunk.parts[0], 'inline_data') and chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
                image_bytes = chunk.parts[0].inline_data.data
                return base64.b64encode(image_bytes).decode("utf-8")

        raise ValueError("로고 이미지 생성에 실패했습니다. 응답에 이미지 데이터가 없습니다.")

    except Exception as e:
        raise ValueError(f"로고 이미지 생성 실패: {str(e)}")


def generate_character_image_with_context(
    brand_name: str,
    brand_topic: str,
    core_value: str,
    character_name: str,
    character_concept: str,
    character_personality: str,
    vibes: list[str],
    character_style: str = "플랫 일러스트",
    character_age_feel: str = "나이 초월",
) -> str:
    """
    Generate a professional character image using Name Tag prompt template.

    Uses the prompt template from Prompt/네임텍 로고 캐릭터 생성 프롬프트.md
    to create a high-quality character/mascot with detailed specifications.

    Args:
        brand_name: Name of the brand
        brand_topic: Topic/business type
        core_value: Core brand values
        character_name: Name of the character
        character_concept: Character concept (의인화 사물, 동물, 인간형, etc.)
        character_personality: Character personality traits (comma-separated)
        vibes: List of brand vibes
        character_style: Illustration style (플랫 일러스트, 손그림 느낌, 3D 렌더, etc.)
        character_age_feel: Age feeling (어린이, 청소년, 청년, 중장년, 나이 초월)

    Returns:
        Base64 encoded character image string

    Raises:
        RuntimeError: If API key is not set
        ValueError: If image generation fails
    """
    # Use dedicated image generation API key from environment
    image_api_key = os.getenv("GEMINI_IMAGE_API_KEY", "").strip()
    if not image_api_key:
        raise RuntimeError("GEMINI_IMAGE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    client = genai.Client(api_key=image_api_key)

    # Get template and prepare prompt with character-specific variables
    target_mood = vibes[0] if vibes else "따뜻 & 친근"

    template = get_character_prompt_template()

    # Replace variables with character-specific info
    prompt = template.replace("[BRAND_NAME]", brand_name)
    prompt = prompt.replace("[BRAND_TOPIC]", brand_topic)
    prompt = prompt.replace("[CORE_VALUE]", core_value)
    prompt = prompt.replace("[TARGET_MOOD]", target_mood)
    prompt = prompt.replace("[CHAR_CONCEPT]", character_concept)
    prompt = prompt.replace("[CHAR_PERSONALITY]", character_personality)
    prompt = prompt.replace("[CHAR_AGE_FEEL]", character_age_feel)
    prompt = prompt.replace("[CHAR_STYLE]", character_style)

    try:
        # Use streaming with minimal config
        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        )
        
        # Create Content object like in Test/Image_genaration_Test.py
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
        
        for chunk in client.models.generate_content_stream(
            model="gemini-3.1-flash-image-preview",
            contents=[content],
            config=config,
        ):
            # Check if chunk has parts attribute and if it's not None
            if not hasattr(chunk, 'parts') or chunk.parts is None:
                continue
            if len(chunk.parts) > 0 and hasattr(chunk.parts[0], 'inline_data') and chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
                image_bytes = chunk.parts[0].inline_data.data
                return base64.b64encode(image_bytes).decode("utf-8")

        raise ValueError("캐릭터 이미지 생성에 실패했습니다. 응답에 이미지 데이터가 없습니다.")

    except Exception as e:
        raise ValueError(f"캐릭터 이미지 생성 실패: {str(e)}")


def infer_missing_variables(
    brand_name: str = "",
    brand_topic: str = "",
    core_value: str = "",
    target_mood: str = "",
    business_type: str = "",
    vibes: list[str] = None,
    target: str = "",
    keywords: str = "",
) -> dict[str, str]:
    """
    Infer missing image generation variables from existing brand data.

    Args:
        brand_name: Brand name (if available)
        brand_topic: Brand topic (if available)
        core_value: Core values (if available)
        target_mood: Target mood/vibe (if available)
        business_type: Business type (if available)
        vibes: Brand vibes list
        target: Target customer (if available)
        keywords: Additional keywords

    Returns:
        Dictionary with inferred variables

    Raises:
        RuntimeError: If API key is not set
        ValueError: If inference fails
    """
    client, model_name = _get_model()

    # Prepare available information
    available_info = []
    if brand_name:
        available_info.append(f"브랜드명: {brand_name}")
    if brand_topic or business_type:
        available_info.append(f"업종/주제: {brand_topic or business_type}")
    if core_value:
        available_info.append(f"핵심 가치: {core_value}")
    if vibes:
        available_info.append(f"브랜드 감성: {', '.join(vibes)}")
    if target:
        available_info.append(f"타겟 고객: {target}")
    if keywords:
        available_info.append(f"추가 키워드: {keywords}")

    available_context = "\n".join(available_info) if available_info else "기본 정보가 제공되지 않았습니다"

    # Prepare inference prompt
    inference_prompt = f"""기존 브랜드 정보를 바탕으로 로고와 캐릭터 생성에 필요한 변수를 추론해주세요.

**제공된 브랜드 정보**
{available_context}

아래 JSON 형식으로만 응답하세요. 추론할 수 없는 항목은 "추론 불가"로 표기:

{{
  "inferred_variables": {{
    "brand_name": "브랜드명 (제공되지 않은 경우 추천)",
    "brand_topic": "업종/사업 주제 설명",
    "core_value": "핵심 가치 1-2개",
    "symbol_type": "심볼 스타일 추천 (기하학적/유기적/미니멀/아이콘형)",
    "character_concept": "캐릭터 컨셉",
    "character_personality": "캐릭터 성격 특징 3개",
    "character_style": "일러스트 스타일 추천 (플랫 일러스트/손그림 느낌/2.5D)",
    "character_age_feel": "캐릭터 나이대 느낌 (어린이/청소년/청년/중장년/나이 초월)",
    "recommended_mood": "추천 브랜드 무드 코드 (MOOD-01~08)"
  }},
  "reasoning": "추론 로직 설명 2-3문장"
}}"""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=inference_prompt,
            config=types.GenerateContentConfig(
                system_instruction="당신은 브랜드 아이덴티티 전문가입니다. 주어진 정보로부터 로고와 캐릭터 생성 변수를 추론합니다."
            ),
        )

        raw_text = response.text or ""
        result = extract_json(raw_text)

        if result is None:
            raise ValueError(f"JSON 파싱 실패. 원본 응답:\n{raw_text[:500]}")

        if "inferred_variables" not in result:
            raise ValueError("응답에 필수 'inferred_variables' 키가 없습니다")

        return result.get("inferred_variables", {})

    except Exception as e:
        raise ValueError(f"변수 추론 실패: {str(e)}")

