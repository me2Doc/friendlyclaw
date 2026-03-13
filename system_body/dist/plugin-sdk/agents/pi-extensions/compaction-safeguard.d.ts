import type { AgentMessage } from "@mariozechner/pi-agent-core";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { computeAdaptiveChunkRatio, isOversizedForSummary } from "../compaction.js";
type ToolFailure = {
    toolCallId: string;
    toolName: string;
    summary: string;
    meta?: string;
};
declare function collectToolFailures(messages: AgentMessage[]): ToolFailure[];
declare function formatToolFailuresSection(failures: ToolFailure[]): string;
/**
 * Read and format critical workspace context for compaction summary.
 * Extracts "Session Startup" and "Red Lines" from AGENTS.md.
 * Limited to 2000 chars to avoid bloating the summary.
 */
declare function readWorkspaceContextForSummary(): Promise<string>;
export default function compactionSafeguardExtension(api: ExtensionAPI): void;
export declare const __testing: {
    readonly collectToolFailures: typeof collectToolFailures;
    readonly formatToolFailuresSection: typeof formatToolFailuresSection;
    readonly computeAdaptiveChunkRatio: typeof computeAdaptiveChunkRatio;
    readonly isOversizedForSummary: typeof isOversizedForSummary;
    readonly readWorkspaceContextForSummary: typeof readWorkspaceContextForSummary;
    readonly BASE_CHUNK_RATIO: 0.4;
    readonly MIN_CHUNK_RATIO: 0.15;
    readonly SAFETY_MARGIN: 1.2;
};
export {};
