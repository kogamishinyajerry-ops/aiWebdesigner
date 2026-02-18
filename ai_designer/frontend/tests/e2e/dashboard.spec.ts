/**
 * Dashboard Page E2E Tests
 */

import { test, expect } from '@playwright/test'

test.describe('Dashboard Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/dashboard')
  })

  test('shows dashboard heading', async ({ page }) => {
    const heading = page.locator('h1, h2')
    await expect(heading.first()).toBeVisible()
  })

  test('shows statistics cards', async ({ page }) => {
    const cards = page.locator('[class*="card"]').first()
    await expect(cards).toBeVisible()
  })

  test('has new project button', async ({ page }) => {
    const button = page.getByRole('button', { name: /new project/i })
    await expect(button).toBeVisible()
  })
})
