/**
 * Button Component Tests
 */

import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Button from '../components/ui/button'

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('applies default variant', () => {
    render(<Button>Test</Button>)
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-primary')
  })

  it('applies variant prop', () => {
    render(<Button variant="secondary">Test</Button>)
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-secondary')
  })

  it('applies size prop', () => {
    render(<Button size="lg">Test</Button>)
    const button = screen.getByRole('button')
    expect(button).toHaveClass('h-10', 'px-8')
  })

  it('applies gradient variant', () => {
    render(<Button variant="gradient">Test</Button>)
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-gradient-to-r')
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Test</Button>)
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
  })

  it('handles click events', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    screen.getByRole('button').click()
    expect(handleClick).toHaveBeenCalledOnce()
  })
})
