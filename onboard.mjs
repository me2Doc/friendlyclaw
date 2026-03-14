import * as p from '@clack/prompts';
import chalk from 'chalk';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ENV_FILE = path.join(__dirname, '.env');

async function verifyTelegram(token) {
    try {
        const resp = await fetch(`https://api.telegram.org/bot${token}/getMe`);
        const data = await resp.json();
        return data.ok ? data.result.username : null;
    } catch { return null; }
}

async function main() {
    p.intro(chalk.bgCyan.black(' FriendlyClaw Hive — Strategic Onboarding [v3.7] '));

    const proceed = await p.confirm({ message: 'Acknowledge system-level access and proceed?' });
    if (p.isCancel(proceed) || !proceed) { p.cancel('Operational shutdown.'); process.exit(1); }

    let config = {};
    if (fs.existsSync(ENV_FILE)) config = dotenv.parse(fs.readFileSync(ENV_FILE));

    // 1. Intelligence Core
    const provider = await p.select({
        message: 'Select Intelligence Core (Model Provider)',
        options: [
            { value: 'gemini', label: 'Google Gemini', hint: 'Native OAuth/API' },
            { value: 'openai', label: 'OpenAI', hint: 'GPT-5.4' },
            { value: 'anthropic', label: 'Anthropic', hint: 'Claude 4.6' },
        ],
    });
    if (p.isCancel(provider)) process.exit(1);
    config.MODEL_PROVIDER = provider;

    if (provider === 'gemini') {
        const authType = await p.select({
            message: 'Gemini Authentication Method',
            options: [
                { value: 'oauth', label: 'Google Gemini CLI OAuth', hint: 'Browser Login' },
                { value: 'api_key', label: 'Gemini API Key', hint: 'Direct Key' },
            ],
        });

        if (authType === 'oauth') {
            const loginNow = await p.confirm({ message: 'Open browser now to authenticate with Google?' });
            if (loginNow) {
                try {
                    p.note('Launching browser for Google ADC login...');
                    // This will open the browser and wait for login
                    execSync('gcloud auth application-default login', { stdio: 'inherit' });
                    p.note(chalk.green('✔ Google Authentication successful.'));
                    config.GEMINI_USE_OAUTH = 'true';
                } catch (e) {
                    p.note(chalk.red('✘ Google Login failed. Ensure "gcloud" CLI is installed.'));
                    const retry = await p.confirm({ message: 'Continue anyway?' });
                    if (!retry) process.exit(1);
                    config.GEMINI_USE_OAUTH = 'true';
                }
            }
        } else {
            const key = await p.password({ message: 'Enter Gemini API Key' });
            if (p.isCancel(key)) process.exit(1);
            config.GEMINI_API_KEY = key;
            config.GEMINI_USE_OAUTH = 'false';
        }
        config.MODEL_NAME = 'gemini-3.1-pro';
    }

    // 2. Channel & Platform Verification
    const platform = await p.select({
        message: 'Select Primary Channel',
        options: [
            { value: 'cli', label: 'CLI (Standard Terminal)' },
            { value: 'telegram', label: 'Telegram Bot', hint: 'Verified Login' },
        ],
    });
    if (p.isCancel(platform)) process.exit(1);
    config.PLATFORM = platform;

    if (platform === 'telegram') {
        const token = await p.password({ message: 'Enter Telegram Bot Token (@BotFather)' });
        if (p.isCancel(token)) process.exit(1);

        const s = p.spinner();
        s.start('Verifying Bot Identity...');
        const botName = await verifyTelegram(token);
        
        if (botName) {
            s.stop(chalk.green(`✔ Connected as @${botName}`));
            config.TELEGRAM_BOT_TOKEN = token;
        } else {
            s.stop(chalk.red('✘ Invalid Bot Token. Connection failed.'));
            const force = await p.confirm({ message: 'Save unverified token anyway?' });
            if (!force) process.exit(1);
            config.TELEGRAM_BOT_TOKEN = token;
        }
    }

    // 3. System Write
    const envContent = Object.entries(config).map(([k, v]) => `${k}=${v}`).join('\n');
    fs.writeFileSync(ENV_FILE, envContent);
    p.outro(chalk.bgGreen.black(' Deployment Ready '));

    const action = await p.select({
        message: 'Action:',
        options: [
            { value: 'hatch', label: '🚀 Hatch Operative (Verify & Launch)' },
            { value: 'exit', label: 'Exit' },
        ],
    });
    process.exit(action === 'hatch' ? 0 : 2);
}

main().catch(console.error);
