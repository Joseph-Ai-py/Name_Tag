import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { SectionA } from '../SectionA';
import { useBrandStore } from '../../store/brandStore';

vi.mock('../../api/client', () => ({
  regenerateSectionAField: vi.fn(),
  generateSectionA: vi.fn(),
  getAInterview: vi.fn(),
  apiLogger: {
    info: vi.fn(),
    warn: vi.fn(),
    error: vi.fn(),
  },
}));

import * as api from '../../api/client';

describe('SectionA selection persistence', () => {
  beforeEach(() => {
    // reset store
    const store = useBrandStore.getState();
    store.reset();
    // provide brandInfo and dataA so buttons render
    store.setBrandInfo({
      brand_name: 'Test',
      brand_name_en: 'TestEN',
      name_meaning: 'Meaning',
      slogan: 'Slogan',
      story_summary: 'Story',
      seed_color: '#000',
      seed_color_reason: 'reason',
    });
    store.setDataA({ brand_name: 'Test', name_meaning: 'Meaning', slogan: 'Slogan', story_summary: 'Story' });
    // clear applied selections
    store.clearAppliedSelections('A');
    // ensure mock cleared
    (api.regenerateSectionAField as any).mockClear();
  });

  it('shows saved selection and does not call API when applied selection exists', async () => {
    const store = useBrandStore.getState();
    store.setAppliedSelection('A', 'brand_name', 'SAVED_NAME');

    render(<SectionA />);

    // click 재생성 (브랜드명) button
    const regenBtn = screen.getByText(/재생성 \(브랜드명\)/);
    fireEvent.click(regenBtn);

    // modal should show saved selection text
    await waitFor(() => expect(screen.getByText('SAVED_NAME')).toBeTruthy());

    // API should not have been called
    expect(api.regenerateSectionAField).not.toHaveBeenCalled();
  });
});
