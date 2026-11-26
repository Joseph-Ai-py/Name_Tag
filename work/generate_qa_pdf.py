import json
from pathlib import Path
import urllib.request, urllib.error
from backend.prompts.nametag_prompts_v2 import REPORT_PAGE_ORDER, REQUIRED_DATA_KEYS, REPORT_PAGE_SPECS
from backend.pdf.report_v2_pdf import DEFAULT_PAGE_LAYOUTS

brand = "NAME TAG · PDF 레이아웃 QA"
test = "QA"
pages = {}
for pid in REPORT_PAGE_ORDER:
    data = {key: [] for key in REQUIRED_DATA_KEYS[pid]}
    for key in REQUIRED_DATA_KEYS[pid]:
        if key in {"source_ids", "sources", "assumptions", "exclusions", "limitations", "validation_records", "evidence_types", "key_metrics", "key_findings", "key_strategies", "priority_actions", "shared_problems", "differences", "comparison_summary", "market_gaps", "recommended_differentiation", "three_c", "five_forces", "key_success_factors", "market_attractiveness", "calculation_basis", "validation_plan", "plan_30_60_90_days", "validation_hypotheses", "kpis", "owners", "timeline", "priority", "stages", "applications", "brand_consistency_notes", "color_palette", "typography", "image_mood", "design_principles", "strengths", "weaknesses", "opportunities", "threats", "SO", "WO", "ST", "WT", "customer_segments", "value_propositions", "channels", "customer_relationships", "revenue_streams", "key_resources", "key_activities", "key_partners", "cost_structure", "hypotheses", "competitors", "personas", "persona_vpcs", "persona_ids"}:
            data[key] = []
        else:
            data[key] = test
    if pid == "00":
        data.update(brand_name=brand, industry="QA 픽스처", report_version="V2 · QA", report_date="2026-11-24", key_sentence=test, brand_promise=test)
    elif pid == "01":
        data.update(brand_thesis=test, key_metrics=[], key_findings=[], key_strategies=[], priority_actions=[], calculation_basis=test)
    elif pid == "02":
        data.update(golden_circle={"why":test,"how":test,"what":test}, brand_essence=test, customer_connection=test)
    elif pid == "03": data.update(identity_prism={}, archetype=test, core_values=[])
    elif pid == "04": data.update(naming={"name":brand,"meaning":test}, story={"summary":test,"promise":test}, slogan=test)
    elif pid == "05":
        axes={"axis_x":{"name":test,"description":test,"low_anchor":test,"high_anchor":test,"evaluation_factors":[{"factor_id":"x_test","weight":1.0,"description":test}]},"axis_y":{"name":test,"description":test,"low_anchor":test,"high_anchor":test,"evaluation_factors":[{"factor_id":"y_test","weight":1.0,"description":test}]}}
        data.update(axes, entities=[{"entity_id":"our_idea","entity_type":"our_idea","name":brand,"factor_scores":[{"factor_id":"x_test","score":50,"reasoning":test},{"factor_id":"y_test","score":50,"reasoning":test}],"confidence":"low","evidence_type":"test_fixture"}], pop=test,pod=test,brand_mantra=test,strategic_implication=test)
    elif pid == "06": data.update(business_stage=test,products_services=[],resources=[],current_performance=[],constraints=[],evidence=[])
    elif pid in {"07","08"}:
        start=1 if pid=="07" else 3
        data["personas"]=[{"persona_id":f"P{i}","name":f"가상 QA 페르소나 P{i}","segment":test,"name_is_fictional":True,"quote_is_fictional":True,"needs":[],"goals":[],"pain_points":[],"behaviors":[],"evidence_type":"test_fixture"} for i in range(start,start+2)]
    elif pid == "09": data.update(comparison=[{"persona_id":f"P{i}","priority":i,"score":50,"reasoning":test} for i in range(1,5)],shared_problems=[],differences=[],priority_segment="QA 전용")
    elif pid == "10":
        factors={k:{"score":50,"reasoning":test} for k in "SFIAPGDC"}
        data.update(persona_vpcs=[{"persona_id":f"P{i}","x":50,"y":50,"quadrant":"test_fixture"} for i in range(1,5)], value_fit_inputs={f"P{i}":factors for i in range(1,5)})
    elif pid == "12":
        blank={"amount":None,"customer_count":None,"annual_revenue_per_customer":None}
        data.update(tam=blank,sam=blank,som=blank,calculation_method=test,assumptions=[],exclusions=[],source_ids=[])
    elif pid == "13": data.update(competitors=[],comparison_summary=[],market_gaps=[],recommended_differentiation=[])
    elif pid == "14": data.update(strengths=[],weaknesses=[],opportunities=[],threats=[])
    elif pid == "15": data.update(SO=[],WO=[],ST=[],WT=[])
    elif pid == "16":
        for k in REQUIRED_DATA_KEYS[pid][:-1]: data[k]=[]
        data["validation_plan"]=[]
    elif pid == "17": data.update(enabled=False,problem=[],customer_segments=[],unique_value_proposition=test,solution=[],channels=[],revenue_streams=[],cost_structure=[],key_metrics=[],unfair_advantage=test,hypotheses=[])
    elif pid == "18": data.update(persona_ids=[f"P{i}" for i in range(1,5)],stages=[])
    elif pid == "21": data.update(enabled=False,character_identity={})
    result={"page_id":pid,"title":REPORT_PAGE_SPECS[pid]["title"],"status":"insufficient_data","data":data,"field_guidance":[],"evidence_type":"test_fixture","source_ids":[],"confidence":"low","validation_notes":[]}
    pages[pid]=result
layouts=[]
for pid,(size,orientation,margin) in DEFAULT_PAGE_LAYOUTS.items(): layouts.append({"page_id":pid,"paper_size":size,"orientation":orientation,"margins_mm":margin})
payload={"pages":pages,"page_layouts":layouts,"brand_name":brand}
Path("work/payload.json").write_text(json.dumps(payload,ensure_ascii=False),encoding="utf-8")
body=json.dumps(payload,ensure_ascii=False).encode("utf-8")
req=urllib.request.Request("http://127.0.0.1:8000/api/pdf/generate-v2",data=body,headers={"Content-Type":"application/json"},method="POST")
out=Path("outputs/NAME_TAG_V2_PDF_QA_Test.pdf")
try:
    with urllib.request.urlopen(req,timeout=120) as resp:
        content=resp.read()
        print("status",resp.status,"content_type",resp.headers.get("Content-Type"),"bytes",len(content))
        if not content.startswith(b"%PDF-"): raise RuntimeError("response is not a PDF")
        out.write_bytes(content)
except urllib.error.HTTPError as e:
    print("HTTP_ERROR",e.code,e.read().decode("utf-8",errors="replace"))
    raise
print("saved",out.resolve())




