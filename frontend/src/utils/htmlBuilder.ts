export function buildSectionOHtml(brandData: any, selected: any = {}) {
  const { business_type, vibes = [], target, keywords } = brandData || {};
  const brandName = selected.brand_name || selected.name || '브랜드명 미정';
  const meaning = selected.name_meaning || '';
  const slogan = selected.slogan || '';
  const story = selected.story_summary || '';

  return `
  <div class="nametag-preview">
    <h1>${brandName}</h1>
    <p><strong>업종/서비스:</strong> ${business_type || ''}</p>
    <p><strong>타겟:</strong> ${target || ''}</p>
    <p><strong>감성:</strong> ${vibes.join(', ')}</p>
    <p><strong>키워드:</strong> ${keywords || ''}</p>
    <hr/>
    <h2>의미</h2>
    <p>${meaning}</p>
    <h2>슬로건</h2>
    <p>${slogan}</p>
    <h2>스토리</h2>
    <p>${story}</p>
  </div>`;
}
