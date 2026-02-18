/**
 * Skeleton Component Tests
 */

import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Skeleton } from '@/components/ui/skeleton'

describe('Skeleton Component', () => {
  it('renders skeleton element', () => {
    render(<Skeleton />)
    const skeleton = screen.getByRole('generic')
    expect(skeleton).toBeInTheDocument()
    expect(skeleton).toHaveClass('animate-pulse')
  })

  it('applies custom className', () => {
    render(<Skeleton className="custom-class" />)
    const skeleton = screen.getByRole('generic')
    expect(skeleton).toHaveClass('custom-class')
  })

  it('renders with default styles', () => {
    render(<Skeleton />)
    const skeleton = screen.getByRole('generic')
    expect(skeleton).toHaveClass('bg-muted', 'h-4', 'w-full')
  })
})
