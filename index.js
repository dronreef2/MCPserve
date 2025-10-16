#!/usr/bin/env node

const { spawn } = require('child_process');

// Smithery expects a default export function with sessionId and config
export default function({ sessionId, config }) {
  return new Promise((resolve, reject) => {
    // Get the Python executable path
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

    // Set environment variables from config
    const env = { ...process.env };
    if (config) {
      if (config.jinaApiKey) env.JINA_API_KEY = config.jinaApiKey;
      if (config.geminiApiKey) env.GEMINI_API_KEY = config.geminiApiKey;
      if (config.deeplApiKey) env.DEEPL_API_KEY = config.deeplApiKey;
      if (config.redisUrl) env.REDIS_URL = config.redisUrl;
    }

    // Spawn the Python MCP server
    const serverProcess = spawn(pythonCmd, ['-m', 'enhanced_mcp_server.core.server'], {
      stdio: ['pipe', 'pipe', 'pipe'],
      env: env
    });

    // Handle process events
    serverProcess.on('error', (err) => {
      console.error('Failed to start Python MCP server:', err);
      reject(err);
    });

    // Return the process streams for Smithery to handle
    resolve({
      stdin: serverProcess.stdin,
      stdout: serverProcess.stdout,
      stderr: serverProcess.stderr,
      process: serverProcess
    });
  });
}