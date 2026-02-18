/**
 * Navbar Component Tests
 */

import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import Navbar from '@/components/layout/navbar'

vi.mock('next-themes', () => ({
  useTheme: () => ({
    theme: 'light',
    setTheme: vi.fn(),
  }),
}))

describe('Navbar', () => {
  it('renders logo', () => {
    render(<Navbar />)
    expect(screen.getByText('AI Designer')).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<Navbar />)
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Generator')).toBeInTheDocument()
  })

  it('renders start button', () => {
    render(<Navbar />)
    const button = screen.getByRole('button', { name: /start creating/i })
    expect(button).toBeInTheDocument()
  })
})
