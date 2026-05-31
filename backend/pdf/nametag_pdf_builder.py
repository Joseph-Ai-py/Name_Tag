from __future__ import annotations

import os
from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType


@lru_cache(maxsize=1)
def _load_base_module() -> ModuleType:
    root = Path(__file__).resolve().parents[2]
    file_path = root / "notebook_backend" / "nametag_pdf_builder.py"
    spec = spec_from_file_location("nametag_pdf_builder_base", file_path)
    if not spec or not spec.loader:
        raise RuntimeError("PDF 빌더 모듈을 로드할 수 없습니다.")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_d_logo_identity(data_D, logo_image_path=None):
    base = _load_base_module()
    concept = data_D.get("logo_identity", {}).get("concept", {})
    guide = data_D.get("logo_identity", {}).get("guide", {})

    symbol_reason = base.e(concept.get("symbol_reason", ""))
    color_reason = base.e(concept.get("color_reason", ""))
    overall_message = base.e(concept.get("overall_message", "")).replace("\n", "<br>")
    direction_text = base.e(concept.get("direction_text", ""))

    min_size = base.e(guide.get("minimum_size", ""))
    clear_space = base.e(guide.get("clear_space", ""))

    # 디버그 로그
    print(f"[DEBUG] build_d_logo_identity - logo_image_path: {logo_image_path}")
    print(f"[DEBUG] build_d_logo_identity - os.path.exists: {os.path.exists(logo_image_path) if logo_image_path else False}")

    if logo_image_path and os.path.exists(logo_image_path):
        # 파일 경로를 file:// URL로 변환 (절대 경로 사용)
        abs_path = os.path.abspath(logo_image_path).replace("\\", "/")
        img_tag = f'<img src="file:///{abs_path}" style="max-width: 100%; max-height: 280px; object-fit: contain; margin: 0 auto; display: block;">'
        print(f"[DEBUG] build_d_logo_identity - Using file URL: file:///{abs_path}")
    else:
        img_tag = """
        <div style="width: 100%; height: 250px; background: rgba(0,0,0,0.02); border: 1px dashed var(--border-strong); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 13px;">
            [로고 이미지 렌더링 대기 중]
        </div>"""
        print(f"[DEBUG] build_d_logo_identity - Image not found or path is None")

    return f"""
    <div class="section" style="page-break-inside: avoid; break-inside: avoid-page;">
        <div class="sec-hdr">
            <span class="sec-num">Section D-1</span>
            <span class="sec-title">Logo Identity & Concept</span>
            <span class="sec-sub">브랜드의 철학과 핵심 가치를 시각적으로 압축한 마스터 로고입니다.</span>
        </div>

      <div class="card" style="text-align: center; margin-bottom: 16px; padding: 28px 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.02);">
            {img_tag}
        </div>

        <div class="hl-box">
            <div class="c-lbl">Design Direction · 시각적 방향성</div>
            <p style="font-weight: 500; font-style: italic;">"{direction_text}"</p>
        </div>

      <div class="grid-2" style="margin-bottom: 12px; gap: 10px;">
        <div class="card" style="border-top: 3px solid var(--sd); padding: 10px 11px;">
          <div class="c-lbl" style="font-size: 9.5px; margin-bottom: 6px;">Symbol Motif</div>
          <div class="c-body" style="text-align: justify; font-size: 11.5px; line-height: 1.55;">{symbol_reason}</div>
        </div>
        <div class="card" style="border-top: 3px solid var(--sd); padding: 10px 11px;">
          <div class="c-lbl" style="font-size: 9.5px; margin-bottom: 6px;">Color Identity</div>
          <div class="c-body" style="text-align: justify; font-size: 11.5px; line-height: 1.55;">{color_reason}</div>
        </div>
      </div>

        <div class="promise-block" style="margin-top: 6px;">
            <div class="ch">Brand Message · 로고가 전달하는 철학</div>
            <div class="ct" style="text-align: justify; font-size: 13.5px;">{overall_message}</div>
        </div>
    </div>

    <div class="section" style="margin-top: 32px;">
        <div class="sec-hdr">
            <span class="sec-num">Section D-2</span>
            <span class="sec-title">Logo Usage Guide</span>
            <span class="sec-sub">크로스 미디어 환경에서 로고의 가독성과 독립성을 보호하기 위한 규정입니다.</span>
        </div>

        <div class="grid-2">
            <div class="card centered-card" style="padding: 30px 20px; overflow: hidden; position: relative;">
                <div style="width: 100px; height: 60px; border: 1px dashed var(--sd); display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.02); margin-bottom: 20px;">
                    <div style="width: 60px; height: 20px; background: var(--text-muted); opacity: 0.2; border-radius: 2px;"></div>
                </div>
                <div class="c-lbl">Clear Space · 안전 여백</div>
                <div class="c-body" style="font-size: 12.5px; font-weight: 500;">{clear_space}</div>
            </div>

            <div class="card centered-card" style="padding: 30px 20px;">
                <div style="display: flex; gap: 20px; align-items: flex-end; justify-content: center; height: 60px; margin-bottom: 20px;">
                    <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                        <div style="width: 40px; height: 14px; background: var(--text-muted); opacity: 0.3; border-radius: 2px;"></div>
                        <span style="font-size: 9px; color: var(--text-muted); font-weight: 600;">WEB</span>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
                        <div style="width: 20px; height: 7px; background: var(--text-muted); opacity: 0.3; border-radius: 1px;"></div>
                        <span style="font-size: 9px; color: var(--text-muted); font-weight: 600;">PRINT</span>
                    </div>
                </div>
                <div class="c-lbl">Minimum Size · 최소 크기</div>
                <div class="c-body" style="font-size: 12.5px; font-weight: 500;">{min_size}</div>
            </div>
        </div>
    </div>
    """


def build_e_character_guide(data_E, char_image_path=None):
    base = _load_base_module()
    guide = data_E.get("character_guide", {})
    intro = guide.get("intro", {})
    reasoning = guide.get("reasoning", {})
    story = guide.get("story", {})

    char_name = base.e(intro.get("name", ""))
    appearance = base.e(intro.get("appearance", "")).replace("\n", "<br>")
    symbolic_value = base.e(intro.get("symbolic_value", ""))

    selection_reason = base.e(reasoning.get("selection_reason", ""))
    emotional_connection = base.e(reasoning.get("emotional_connection", ""))

    background_story = base.e(story.get("background", "")).replace("\n", "<br>")
    brand_role = base.e(story.get("brand_role", ""))

    # 디버그 로그
    print(f"[DEBUG] build_e_character_guide - char_image_path: {char_image_path}")
    print(f"[DEBUG] build_e_character_guide - os.path.exists: {os.path.exists(char_image_path) if char_image_path else False}")

    if char_image_path and os.path.exists(char_image_path):
        # 파일 경로를 file:// URL로 변환 (절대 경로 사용)
        abs_path = os.path.abspath(char_image_path).replace("\\", "/")
        img_tag = f'<img src="file:///{abs_path}" style="max-width: 100%; max-height: 320px; object-fit: contain; margin: 0 auto; display: block; border-radius: 8px;">'
        print(f"[DEBUG] build_e_character_guide - Using file URL: file:///{abs_path}")
    else:
        img_tag = """
        <div style="width: 100%; height: 320px; background: rgba(0,0,0,0.02); border: 1px dashed var(--border-strong); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 13px;">
            [캐릭터 이미지 렌더링 대기 중]
        </div>"""
        print(f"[DEBUG] build_e_character_guide - Image not found or path is None")

    return f"""
    <div class="section">
        <div class="sec-hdr">
            <span class="sec-num">Section E-1</span>
            <span class="sec-title">Brand Persona & Character</span>
            <span class="sec-sub">고객과 브랜드 사이의 정서적 유대감을 형성하는 핵심 페르소나입니다.</span>
        </div>

        <div style="display: grid; grid-template-columns: 4fr 6fr; gap: 16px; margin-bottom: 24px; page-break-inside: avoid;">
            <div class="card" style="display: flex; align-items: center; justify-content: center; padding: 20px; background: var(--bg);">
                {img_tag}
            </div>

            <div style="display: flex; flex-direction: column; gap: 12px;">
                <div class="slogan-box" style="margin: 0; padding: 16px; border-width: 1px; background: var(--surface);">
                    <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 4px;">Persona Name</div>
                    <div style="font-family: 'Noto Serif KR', serif; font-size: 24px; font-weight: 700; color: var(--sd); line-height: 1.3;">{char_name}</div>
                </div>

                <div class="card" style="flex-grow: 1;">
                    <div class="c-lbl">Appearance · 외형 및 디자인 특징</div>
                    <div class="c-body" style="text-align: justify;">{appearance}</div>
                </div>
            </div>
        </div>

    <div class="hl-box" style="margin-bottom: 16px;">
            <div class="c-lbl" style="color: rgba(0,0,0,0.5);">Worldview & Role · 세계관 및 브랜드 내 역할</div>
            <p style="font-size: 14px; font-weight: 600; line-height: 1.6; margin-bottom: 8px;">"{brand_role}"</p>
            <p style="font-size: 13px; font-weight: 400; opacity: 0.9;">{background_story}</p>
        </div>

        <div class="grid-2">
            <div class="card">
                <div class="c-lbl">Core Value · 상징 가치 및 선택 이유</div>
                <div class="c-body" style="text-align: justify; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px dashed var(--border-light);">
                    <strong style="color: var(--text-main); font-weight: 600;">상징 가치:</strong> {symbolic_value}
                </div>
                <div class="c-body" style="text-align: justify;">
                    {selection_reason}
                </div>
            </div>
             <div class="card">
                <div class="c-lbl">Emotional Link · 감정적 연결 포인트</div>
                <div class="c-body" style="text-align: justify; line-height: 1.8;">{emotional_connection}</div>
            </div>
        </div>
    </div>
    """


def assemble_html(brand_info, data_A=None, data_B=None, data_C=None, data_DE=None):
    base = _load_base_module()
    base.build_d_logo_identity = build_d_logo_identity
    base.build_e_character_guide = build_e_character_guide
    
    # 웹 경로를 파일 경로로 변환 (data_DE에 있는 이미지 경로)
    if data_DE and isinstance(data_DE, dict):
        def convert_web_path_to_file_path(web_path):
            """웹 경로 (e.g., '/assets/...') 를 파일 시스템 경로로 변환"""
            if not web_path or not web_path.startswith("/assets/"):
                return web_path
            
            relative = web_path[1:]  # 앞의 / 제거
            root = Path(__file__).resolve().parents[2]  # 프로젝트 루트
            file_path = root / relative
            return str(file_path)
        
        # 이미지 경로 변환
        if "logo_path" in data_DE:
            original_logo_path = data_DE.get("logo_path")
            file_logo_path = convert_web_path_to_file_path(original_logo_path)
            print(f"[DEBUG] assemble_html - logo_path: {original_logo_path} -> {file_logo_path}")
            data_DE["_logo_file_path"] = file_logo_path
        
        if "char_path" in data_DE:
            original_char_path = data_DE.get("char_path")
            file_char_path = convert_web_path_to_file_path(original_char_path)
            print(f"[DEBUG] assemble_html - char_path: {original_char_path} -> {file_char_path}")
            data_DE["_char_file_path"] = file_char_path
    
    # 원본 notebook_backend 함수 호출하되, 이미지 경로 주입
    html = base.assemble_html(brand_info, data_A, data_B, data_C, data_DE)
    return html