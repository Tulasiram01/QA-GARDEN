const { test, expect } = require('@playwright/test');

/**
 * Demo Playwright Tests - Designed to Fail for Triage Engine Testing
 * These tests intentionally fail to generate test failure data for the bug triage engine
 */

test.describe('Demo Failure Tests', () => {

    test('should fail - incorrect page title', async ({ page }) => {
        await page.goto('https://example.com');
        // This will fail because the actual title is "Example Domain"
        await expect(page).toHaveTitle('Welcome to Example Website');
    });

    test('should fail - missing button element', async ({ page }) => {
        await page.goto('https://example.com');
        // This will fail because the button doesn't exist
        const loginButton = page.locator('button#login');
        await expect(loginButton).toBeVisible();
    });

    test('should fail - incorrect URL navigation', async ({ page }) => {
        await page.goto('https://example.com');
        await page.click('a'); // Click the "More information..." link
        // This will fail because we navigate to iana.org, not example.org
        await expect(page).toHaveURL('https://www.example.org/');
    });

    test('should fail - text content mismatch', async ({ page }) => {
        await page.goto('https://example.com');
        const heading = page.locator('h1');
        // This will fail because the actual text is "Example Domain"
        await expect(heading).toHaveText('Welcome to Our Website');
    });

    test('should fail - element count assertion', async ({ page }) => {
        await page.goto('https://example.com');
        const paragraphs = page.locator('p');
        // This will fail because there are only 2 paragraphs, not 5
        await expect(paragraphs).toHaveCount(5);
    });

});
