import * as p from '@clack/prompts';
import chalk from 'chalk';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync, spawn } from 'node:child_process';
import open from 'open';
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
    p.intro(chalk.bgCyan.black(' FriendlyClaw Hive — Strategic Onboarding [v3.9.1] '));

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
                { value: 'oauth', label: 'Google Gemini CLI OAuth (Browser Flow)', hint: 'Best for local dev' },
                { value: 'api_key', label: 'Gemini API Key (Direct)', hint: 'Best for servers' },
            ],
        });

        if (authType === 'oauth') {
            p.note('Starting Google Cloud Authentication flow...');
            const loginNow = await p.confirm({ message: 'Launch browser for Google Login?' });
            if (loginNow) {
                try {
                    console.log(chalk.yellow('\n--- GOOGLE LOGIN STARTING ---'));
                    console.log(chalk.dim('Please follow the browser instructions and ensure you check all consent boxes.'));
                    // Using --no-browser if they want, but standard is fine if they just click the boxes.
                    // Let's stick to standard but add a tip about the checkbox.
                    execSync('gcloud auth application-default login', { stdio: 'inherit' });
                    console.log(chalk.yellow('--- GOOGLE LOGIN COMPLETE ---\n'));
                    
                    p.note(chalk.green('✔ Google ADC credentials verified on system.'));
                    config.GEMINI_USE_OAUTH = 'true';
                } catch (e) {
                    p.note(chalk.red('✘ Login failed or was cancelled.'));
                    const retry = await p.confirm({ message: 'Continue with manual key instead?' });
                    if (!retry) process.exit(1);
                    authType = 'api_key';
                }
            }
        }
        
        if (authType === 'api_key' || !config.GEMINI_USE_OAUTH) {
            p.note('Opening Google AI Studio to generate your key...');
            await open('https://aistudio.google.com/app/apikey');
            const key = await p.password({ message: 'Paste your Gemini API Key here' });
            if (p.isCancel(key)) process.exit(1);
            config.GEMINI_API_KEY = key;
            config.GEMINI_USE_OAUTH = 'false';
        }
        config.MODEL_NAME = 'gemini-3.1-pro';

    } else if (provider === 'openai') {
        p.note('Opening OpenAI Dashboard...');
        await open('https://platform.openai.com/api-keys');
        const key = await p.password({ message: 'Paste your OpenAI API Key' });
        if (p.isCancel(key)) process.exit(1);
        config.OPENAI_API_KEY = key;
        config.MODEL_NAME = 'gpt-5.4';
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
        p.note('Opening @BotFather on Telegram...');
        await open('https://t.me/botfather');
        const token = await p.password({ message: 'Enter Telegram Bot Token' });
        if (p.isCancel(token)) process.exit(1);

        const s = p.spinner();
        s.start('Verifying Bot Identity...');
        const botName = await verifyTelegram(token);
        
        if (botName) {
            s.stop(chalk.green(`✔ Connected as @${botName}`));
            config.TELEGRAM_BOT_TOKEN = token;
        } else {
            s.stop(chalk.red('✘ Invalid Bot Token. Connection failed.'));
            const force = await p.confirm({ message: 'Save anyway?' });
            if (!force) process.exit(1);
            config.TELEGRAM_BOT_TOKEN = token;
        }
    }

    // 3. System Write
    const envContent = Object.entries(config).map(([k, v]) => `${k}=${v}`).join('\n');
    fs.writeFileSync(ENV_FILE, envContent);
    p.outro(chalk.bgGreen.black(' Strategic Deployment Finalized '));

    const action = await p.select({
        message: 'Action:',
        options: [
            { value: 'hatch', label: '🚀 Hatch Operative (Verify & Launch)' },
            { value: 'exit', label: 'Return to Terminal' },
        ],
    });
    process.exit(action === 'hatch' ? 0 : 2);
}

main().catch(console.error);
