from __future__ import annotations

from urllib.parse import quote

from pdf_builder import assemble_html

from pdf_builder import (
    build_css,
	build_cover,
    build_section_o_mvb,
    build_a1_philosophy,
    build_a2_core_identity,
    build_a3_story,
    build_a4_verbal_toolkit,
    build_a5_positioning,
    build_a6_promise,
    build_b1_target_profile,
    build_b2_persona_detail,
    build_b3_customer_journey,
    build_c1_color_system,
    build_c2_typography,
    build_c3_visual_mood,
    build_d_logo_identity,
    build_e_character_guide,
    get_absolute_path
)


def generate_pdf_bytes(
	brand_info: dict,
	data_a: dict,
	data_b: dict,
	data_c: dict,
	data_de: dict,
) -> bytes:
	try:
		from weasyprint import HTML
	except (ImportError, OSError) as exc:
		raise RuntimeError(
			"Unable to import WeasyPrint. Install system dependencies such as libcairo2, "
			"libgobject-2.0-0, and libpango."
		) from exc

	html_content = assemble_html(brand_info, data_a, data_b, data_c, data_de)
	return HTML(string=html_content).write_pdf()


def build_download_filename(brand_name: str) -> str:
	return f"nametag_{brand_name}_guideline.pdf"


def build_content_disposition(brand_name: str) -> str:
	encoded_filename = quote(build_download_filename(brand_name))
	return f"attachment; filename*=utf-8''{encoded_filename}"

def generate_o_only_html(brand_info: dict) -> str:
    """PDF 변환 없이 HTML 문자열만 렌더링하여 반환합니다 (Section O 빠른 미리보기용)"""
    
    # 브랜드 컬러 적용
    seed_color = brand_info.get('seed_color', '#000000') if brand_info else '#000000'
    sd_color = "#3A3A3A"
    sl_color = "#F8F9FA"

    # 기본 CSS 로드 및 미리보기 전용 껍질(Wrapper) CSS 추가
    base_css = build_css(seed_color, sd_color, sl_color)
    preview_css = base_css + """
    body {
        max-width: 210mm;
        margin: 0 auto;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 40px;
        overflow-x: hidden;
    }
    """

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;800&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@400;600;700&display=swap" rel="stylesheet">
  <style>{preview_css}</style>
</head>
<body>
"""
    # 🌟 표지와 Section O 내용을 조립합니다
    if brand_info:
        html += build_cover(brand_info)
        html += build_section_o_mvb(brand_info)

    html += "</body>\n</html>"

    return html

def generate_a_only_html(brand_info: dict, data_a: dict) -> str:
    """PDF 변환 없이 HTML 문자열만 렌더링하여 반환합니다 (빠른 미리보기용)"""
    
    if data_a and 'data_a' in data_a:
        data_a = data_a['data_a']

    seed_color = brand_info.get('seed_color', '#000000') if brand_info else '#000000'
    sd_color = "#3A3A3A"
    sl_color = "#F8F9FA"

    # 기본 CSS 로드
    base_css = build_css(seed_color, sd_color, sl_color)
    
    preview_css = base_css + """
    body {
        max-width: 210mm;
        margin: 0 auto;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 40px;
        overflow-x: hidden;
    }
    """

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;800&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@400;600;700&display=swap" rel="stylesheet">
  <style>{preview_css}</style>
</head>
<body>
"""
    if data_a:
        html += build_a1_philosophy(data_a)
        html += build_a2_core_identity(data_a)
        html += build_a3_story(data_a)
        html += build_a4_verbal_toolkit(data_a)
        html += build_a5_positioning(data_a)
        html += build_a6_promise(data_a)

    html += "</body>\n</html>"

    return html

def generate_b_only_html(brand_info: dict, data_b: dict) -> str:
    """Section B 미리보기용 HTML 생성"""
    if data_b and 'data_b' in data_b: data_b = data_b['data_b']

    seed_color = brand_info.get('seed_color', '#000000') if brand_info else '#000000'
    sd_color, sl_color = "#3A3A3A", "#F8F9FA"

    base_css = build_css(seed_color, sd_color, sl_color)
    preview_css = base_css + "\nbody { max-width: 210mm; margin: 0 auto; background-color: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 40px; overflow-x: hidden; }"

    html = f"""<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n<style>{preview_css}</style>\n</head>\n<body>\n"""
    
    if data_b:
        html += build_b1_target_profile(data_b)
        html += build_b2_persona_detail(data_b)
        html += build_b3_customer_journey(data_b)
        
    html += "</body>\n</html>"
    return html


def generate_c_only_html(brand_info: dict, data_c: dict) -> str:
    """Section C 미리보기용 HTML 생성"""
    if data_c and 'data_c' in data_c: data_c = data_c['data_c']

    seed_color = brand_info.get('seed_color', '#000000') if brand_info else '#000000'
    sd_color, sl_color = "#3A3A3A", "#F8F9FA"

    # Section C에서 추출된 팔레트가 있다면 테마 컬러에 반영합니다.
    if data_c:
        palette = data_c.get('color_palette', [])
        if isinstance(palette, list):
            for c in palette:
                role = c.get('role', '').lower()
                if 'primary' in role: sl_color = c.get('hex_code', sl_color)
                elif 'secondary' in role or 'accent' in role: sd_color = c.get('hex_code', sd_color)

    base_css = build_css(seed_color, sd_color, sl_color)
    preview_css = base_css + "\nbody { max-width: 210mm; margin: 0 auto; background-color: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 40px; overflow-x: hidden; }"

    html = f"""<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n<style>{preview_css}</style>\n</head>\n<body>\n"""
    
    if data_c:
        html += build_c1_color_system(data_c)
        html += build_c2_typography(data_c)
        html += build_c3_visual_mood(data_c)
        
    html += "</body>\n</html>"
    return html

def get_image_base64(image_path):
    """이미지 파일을 읽어 Base64 데이터 URI 문자열로 반환합니다."""
    if not os.path.exists(image_path):
        return ""
    
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # 확장자에 맞춰 MIME 타입 설정 (예: png, jpeg)
    ext = image_path.split('.')[-1].lower()
    mime_type = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
    
    # Base64 데이터 URI 형식으로 반환
    return f"data:{mime_type};base64,{encoded_string}"

def generate_de_only_html(brand_info: dict, data_c: dict, data_de: dict) -> str:
    """Section DE 미리보기용 HTML 생성"""
    if data_c and 'data_c' in data_c: data_c = data_c['data_c']
    if data_de and 'data_de' in data_de: data_de = data_de['data_de']

    seed_color = brand_info.get('seed_color', '#000000') if brand_info else '#000000'
    sd_color, sl_color = "#3A3A3A", "#F8F9FA"

    # C의 컬러 시스템을 가져와서 통일감을 줍니다.
    if data_c:
        palette = data_c.get('color_palette', [])
        if isinstance(palette, list):
            for c in palette:
                role = c.get('role', '').lower()
                if 'primary' in role: sl_color = c.get('hex_code', sl_color)
                elif 'secondary' in role or 'accent' in role: sd_color = c.get('hex_code', sd_color)

    base_css = build_css(seed_color, sd_color, sl_color)
    preview_css = base_css + "\nbody { max-width: 210mm; margin: 0 auto; background-color: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 40px; overflow-x: hidden; }"

    # 로고 및 캐릭터 이미지 경로 추출
    logo_path = get_absolute_path(data_de.get('logo_path', None)) if data_de else None
    base64_logo = get_image_base64(logo_path)
    print(f'logo paht : {base64_logo}')
    char_path = get_absolute_path(data_de.get('char_path', None)) if data_de else None
    base64_char = get_image_base64(char_path)
    print(f'char paht : {base64_char}')

    html = f"""<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n<style>{preview_css}</style>\n</head>\n<body>\n"""
    
    if data_de:
        html += build_d_logo_identity(data_de, logo_path)
        html += build_e_character_guide(data_de, char_path)
        print(f"html_1 = {html}")
        
    html += "</body>\n</html>"
    return html

