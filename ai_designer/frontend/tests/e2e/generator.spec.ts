/**
 * Image Generator Page E2E Tests
 */

import { test, expect } from '@playwright/test'

test.describe('Image Generator Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/generator/image')
  })

  test('shows generator heading', async ({ page }) => {
    const heading = page.locator('h1, h2')
    await expect(heading.first()).toBeVisible()
  })

  test('has prompt input field', async ({ page }) => {
    const input = page.locator('textarea[placeholder*="prompt"], input[placeholder*="prompt"]')
    await expect(input.first()).toBeVisible()
  })

  test('has generate button', async ({ page }) => {
    const button = page.getByRole('button', { name: /generate/i })
    await expect(button).toBeVisible()
  })

  test('shows style presets', async ({ page }) => {
    const presets = page.locator('button').filter({ hasText: /(modern|minimal|glass)/i })
    await expect(presets.first()).toBeVisible()
  })
})
