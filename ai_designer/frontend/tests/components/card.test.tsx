/**
 * Card Component Tests
 */

import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Card from '../components/ui/card'

describe('Card Component', () => {
  it('renders card with children', () => {
    render(
      <Card>
        <Card.Header>
          <Card.Title>Title</Card.Title>
        </Card.Header>
        <Card.Content>Content</Card.Content>
      </Card>
    )
    expect(screen.getByText('Title')).toBeInTheDocument()
    expect(screen.getByText('Content')).toBeInTheDocument()
  })

  it('applies card styling', () => {
    render(<Card>Content</Card>)
    const card = screen.getByText('Content').parentElement
    expect(card).toHaveClass('rounded-lg', 'border', 'bg-card', 'text-card-foreground')
  })

  it('renders card header', () => {
    render(
      <Card>
        <Card.Header>
          <Card.Title>Test Title</Card.Title>
        </Card.Header>
      </Card>
    )
    expect(screen.getByText('Test Title')).toBeInTheDocument()
  })

  it('renders card content', () => {
    render(
      <Card>
        <Card.Content>Test Content</Card.Content>
      </Card>
    )
    expect(screen.getByText('Test Content')).toBeInTheDocument()
  })

  it('renders card footer', () => {
    render(
      <Card>
        <Card.Footer>Footer Text</Card.Footer>
      </Card>
    )
    expect(screen.getByText('Footer Text')).toBeInTheDocument()
  })
})
