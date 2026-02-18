{
  "$schema": "https://vitest.dev/config/schema.json",
  "test": {
    "globals": true,
    "environment": "jsdom",
    "setupFiles": ["./tests/setup.ts"],
    "coverage": {
      "provider": "v8",
      "reporter": ["text", "json", "html"],
      "exclude": [
        "node_modules/",
        "tests/",
        "**/*.config.*",
        "**/*.d.ts"
      ]
    }
  }
}
