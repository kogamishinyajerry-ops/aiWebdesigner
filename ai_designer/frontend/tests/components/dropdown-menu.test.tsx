/**
 * Dropdown Menu Component Tests
 */

import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import * as RadixDropdownMenu from '@radix-ui/react-dropdown-menu'
import { ChevronDown } from 'lucide-react'

describe('Dropdown Menu', () => {
  it('renders dropdown menu button', () => {
    const DropdownMenu = RadixDropdownMenu.Root
    const DropdownMenuTrigger = RadixDropdownMenu.Trigger

    render(
      <DropdownMenu>
        <DropdownMenuTrigger>
          <button>Open Menu</button>
        </DropdownMenuTrigger>
        <RadixDropdownMenu.Content>
          <RadixDropdownMenu.Item>Item 1</RadixDropdownMenu.Item>
        </RadixDropdownMenu.Content>
      </DropdownMenu>
    )

    expect(screen.getByRole('button', { name: /open menu/i })).toBeInTheDocument()
  })

  it('opens menu on click', () => {
    const DropdownMenu = RadixDropdownMenu.Root
    const DropdownMenuTrigger = RadixDropdownMenu.Trigger

    render(
      <DropdownMenu>
        <DropdownMenuTrigger>
          <button>Open Menu</button>
        </DropdownMenuTrigger>
        <RadixDropdownMenu.Content>
          <RadixDropdownMenu.Item>Item 1</RadixDropdownMenu.Item>
        </RadixDropdownMenu.Content>
      </DropdownMenu>
    )

    const button = screen.getByRole('button')
    fireEvent.click(button)

    // Menu should be visible
    expect(screen.getByText('Item 1')).toBeInTheDocument()
  })

  it('calls onClick handler on item click', () => {
    const handleClick = vi.fn()

    const DropdownMenu = RadixDropdownMenu.Root
    const DropdownMenuTrigger = RadixDropdownMenu.Trigger

    render(
      <DropdownMenu>
        <DropdownMenuTrigger>
          <button>Open Menu</button>
        </DropdownMenuTrigger>
        <RadixDropdownMenu.Content>
          <RadixDropdownMenu.Item onSelect={handleClick}>Item 1</RadixDropdownMenu.Item>
        </RadixDropdownMenu.Content>
      </DropdownMenu>
    )

    const button = screen.getByRole('button')
    fireEvent.click(button)

    const item = screen.getByText('Item 1')
    fireEvent.click(item)

    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
