/**
 * Theme Toggle Component Tests
 */

import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import ThemeToggle from '../components/theme-toggle'

// Mock useTheme
vi.mock('next-themes', () => ({
  useTheme: () => ({
    theme: 'light',
    setTheme: vi.fn(),
  }),
}))

describe('ThemeToggle Component', () => {
  it('renders theme toggle button', () => {
    render(<ThemeToggle />)
    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()
  })

  it('has accessible name', () => {
    render(<ThemeToggle />)
    const button = screen.getByRole('button', { name: /theme/i })
    expect(button).toBeInTheDocument()
  })
})
