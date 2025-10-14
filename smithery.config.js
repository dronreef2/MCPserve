import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default function({ config }) {
  return new Promise((resolve, reject) => {
    // Set environment variables from config
    const env = {
      ...process.env,
      JINA_API_KEY: config.jinaApiKey || process.env.JINA_API_KEY,
      GEMINI_API_KEY: config.geminiApiKey || process.env.GEMINI_API_KEY,
      DEEPL_API_KEY: config.deeplApiKey || process.env.DEEPL_API_KEY,
      REDIS_URL: config.redisUrl || process.env.REDIS_URL,
      LOG_LEVEL: config.logLevel || process.env.LOG_LEVEL || 'INFO',
      PYTHONIOENCODING: 'utf-8'
    };

    console.log('Starting Python MCP server...');

    // Start Python process
    const pythonProcess = exec(
      'python main.py',
      {
        cwd: __dirname,
        env: env
      }
    );

    // Handle process events
    pythonProcess.on('exit', (code) => {
      console.log(`Python process exited with code ${code}`);
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}`));
      }
    });

    pythonProcess.on('error', (error) => {
      console.error('Failed to start Python process:', error);
      reject(error);
    });

    // Log stdout and stderr
    pythonProcess.stdout.on('data', (data) => {
      console.log('Python stdout:', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Python stderr:', data.toString());
    });

    // For stdio transport we don't expose an HTTP port
    setTimeout(() => {
      resolve({
        process: pythonProcess
      });
    }, 1500);
  });
}