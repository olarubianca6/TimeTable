import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import index from '@/pages/index.vue'

vi.mock('@/components/TimetableGrid.vue', () => ({
  default: {
    template: '<div data-testid="mock-timetable-grid"></div>'
  }
}))

describe('Index page', () => {
  it('renders title and TimetableGrid', () => {
    const wrapper = mount(index)
    expect(wrapper.text()).toContain('Orar')
    expect(wrapper.find('[data-testid="mock-timetable-grid"]').exists()).toBe(true)
  })
})
