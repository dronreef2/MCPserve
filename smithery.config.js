/** @type {import('@smithery/cli').SmitheryConfig} */
module.exports = {
  name: 'MCPserve',
  version: '0.2.0',
  description: 'Servidor MCP avançado com ferramentas de IA',
  server: {
    command: 'python',
    args: ['-m', 'enhanced_mcp_server.main', '--http'],
    env: {
      WEB_PORT: 8001,
      LOG_LEVEL: 'INFO'
    }
  },
  build: {
    command: 'docker',
    args: ['build', '-t', 'mcpserve', '.'],
    output: 'Dockerfile'
  }
};