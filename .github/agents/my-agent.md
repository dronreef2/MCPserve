---
name: my-agent
description: Agent that runs the @smithery/cli tool to perform build and deployment tasks for MCPserve
---

# My Agent

This agent runs the @smithery/cli package to perform common project tasks for the MCPserve repository.

Usage

- The agent invokes the @smithery/cli Node.js CLI from the repository environment.
- It expects Node 18+ and that dependencies have been installed (npm install) before running.

Example agent steps (for a GitHub Actions or Copilot agent runner):

1. Install dependencies

```bash
npm ci
```

2. Run smithery CLI commands

- To run a build task:

```bash
npx @smithery/cli build --project=MCPserve
```

- To run a deploy task (example):

```bash
npx @smithery/cli deploy --env=production --project=MCPserve
```

3. Exit codes

- The agent will surface the exit code from @smithery/cli. Non-zero exit codes indicate failure.

Environment variables

- SMITHERY_API_KEY: (optional) If your smithery CLI workflow requires authentication, set this as a secret in GitHub Actions or in the environment where the agent runs.
- NODE_ENV: set to production for deploy commands.

Examples for GitHub Actions

Below is an example job snippet showing how to call this agent from a GitHub Actions workflow (place in .github/workflows/*.yml):

```yaml
jobs:
  run-smithery:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run smithery build via agent
        run: npx @smithery/cli build --project=MCPserve
        env:
          SMITHERY_API_KEY: ${{ secrets.SMITHERY_API_KEY }}
```

Notes

- Replace command flags with the ones required by your specific @smithery/cli version.
- If you have a monorepo or workspace set up, adjust the --project flag or working directory accordingly.
