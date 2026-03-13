import type { CronSchedule } from "./types.js";
export declare function computeNextRunAtMs(schedule: CronSchedule, nowMs: number): number | undefined;
export declare function clearCronScheduleCacheForTest(): void;
export declare function getCronScheduleCacheSizeForTest(): number;
