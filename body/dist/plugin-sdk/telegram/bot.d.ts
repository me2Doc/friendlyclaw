import { Bot } from "grammy";
import type { OpenClawConfig, ReplyToMode } from "../config/config.js";
import { type RuntimeEnv } from "../runtime.js";
import { getTelegramSequentialKey } from "./sequential-key.js";
export type TelegramBotOptions = {
    token: string;
    accountId?: string;
    runtime?: RuntimeEnv;
    requireMention?: boolean;
    allowFrom?: Array<string | number>;
    groupAllowFrom?: Array<string | number>;
    mediaMaxMb?: number;
    replyToMode?: ReplyToMode;
    proxyFetch?: typeof fetch;
    config?: OpenClawConfig;
    updateOffset?: {
        lastUpdateId?: number | null;
        onUpdateId?: (updateId: number) => void | Promise<void>;
    };
    testTimings?: {
        mediaGroupFlushMs?: number;
        textFragmentGapMs?: number;
    };
};
export { getTelegramSequentialKey };
export declare function createTelegramBot(opts: TelegramBotOptions): Bot<import("grammy").Context, import("grammy").Api<import("grammy").RawApi>>;
export declare function createTelegramWebhookCallback(bot: Bot, path?: string): {
    path: string;
    handler: (req: {
        headers: Record<string, string | string[] | undefined>;
        on: (event: string, listener: (chunk: unknown) => void) => /*elided*/ any;
        once: (event: string, listener: () => void) => /*elided*/ any;
    }, res: {
        writeHead: {
            (status: number): /*elided*/ any;
            (status: number, headers: Record<string, string>): /*elided*/ any;
        };
        end: (json?: string) => void;
    }) => Promise<void>;
};
