import { s as resolveAgentWorkspaceDir } from "../../agent-scope-DWsn5rte.js";
import { c as resolveStateDir } from "../../paths-C6TxBCvO.js";
import { t as createSubsystemLogger } from "../../subsystem-nlluZawe.js";
import { u as resolveAgentIdFromSessionKey } from "../../session-key-a6av96Fj.js";
import "../../utils-Dvtm0mzf.js";
import "../../workspace-BU8QxCQK.js";
import "../../logger-wD6tEZWm.js";
import "../../model-selection-ikt2OC4j.js";
import "../../env-BgFeGxoV.js";
import "../../github-copilot-token-Dr6AUVHb.js";
import "../../boolean-mcn6kL0s.js";
import "../../internal-hooks-Y1c3CR6c.js";
import "../../registry-ycXZ0GNV.js";
import "../../dock-D49biwXh.js";
import "../../tokens-BXGWtt7T.js";
import "../../pi-embedded-CtM2Mrrj.js";
import "../../plugins-noDEKrDH.js";
import "../../accounts-DGCf7PCM.js";
import "../../bindings-CtbdcwyF.js";
import "../../send-DVuCXZhB.js";
import "../../send-Mhq_NgNz.js";
import "../../deliver-FEreRY0J.js";
import "../../diagnostic-C-4UTg3h.js";
import "../../diagnostic-session-state-DBPrVBk3.js";
import "../../accounts-C1iVq9v_.js";
import "../../send-BjxxplhK.js";
import "../../image-ops-0nwMDFtL.js";
import "../../pi-model-discovery-DvKumK6n.js";
import "../../message-channel-DZhYsPbp.js";
import "../../pi-embedded-helpers-DvNaskDY.js";
import "../../chrome-BJ1olan3.js";
import "../../frontmatter-DIRc-IR1.js";
import "../../skills-D3c_mBu8.js";
import "../../path-alias-guards-CfaVCHQ7.js";
import "../../redact-yC-5vZip.js";
import "../../errors-0iO9hLII.js";
import { c as writeFileWithinRoot } from "../../fs-safe-CW7g83pG.js";
import "../../proxy-env-Y95QXuB3.js";
import "../../store-Dn1gZuiJ.js";
import { D as hasInterSessionUserProvenance } from "../../sessions-_Cu6BqJv.js";
import "../../accounts-C9nmgL8E.js";
import "../../paths-B8Ne8ciC.js";
import "../../tool-images-Bcm94hV8.js";
import "../../thinking-FnAYAFD8.js";
import "../../image-5e0tgQ1Z.js";
import "../../audio-transcription-runner-DYom1Phd.js";
import "../../fetch-DJLxHaLt.js";
import "../../fetch-guard-C23rIR_K.js";
import "../../api-key-rotation-BeJ-Lf5S.js";
import "../../proxy-fetch-DrI0Gh6p.js";
import "../../reply-prefix-DlRGjs31.js";
import "../../chunk-Cgy4C3Nh.js";
import "../../markdown-tables-KowmfLDF.js";
import "../../ir-B6xHv9oi.js";
import "../../render-flG67HhW.js";
import "../../target-errors-C4l9j6WQ.js";
import "../../commands-registry-D7j4kc5h.js";
import "../../skill-commands-BaeDAEuP.js";
import "../../fetch-CIXnD4u2.js";
import "../../channel-activity-Do4UxjWY.js";
import "../../tables-B_RTd-mr.js";
import "../../send-Cwk6REJC.js";
import "../../outbound-attachment-DkDekuYo.js";
import "../../send-P4PvriEH.js";
import "../../resolve-route-DCfod4Po.js";
import "../../proxy-D6pp6ZSj.js";
import "../../replies-Bkdfnyoh.js";
import "../../session-meta-D3MMUgfg.js";
import "../../manager--qQfR6iR.js";
import "../../query-expansion-CeyLNalm.js";
import { generateSlugViaLLM } from "../../llm-slug-generator.js";
import { t as resolveHookConfig } from "../../config-gaZfb7eZ.js";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

//#region src/hooks/bundled/session-memory/handler.ts
/**
* Session memory hook handler
*
* Saves session context to memory when /new or /reset command is triggered
* Creates a new dated memory file with LLM-generated slug
*/
const log = createSubsystemLogger("hooks/session-memory");
/**
* Read recent messages from session file for slug generation
*/
async function getRecentSessionContent(sessionFilePath, messageCount = 15) {
	try {
		const lines = (await fs.readFile(sessionFilePath, "utf-8")).trim().split("\n");
		const allMessages = [];
		for (const line of lines) try {
			const entry = JSON.parse(line);
			if (entry.type === "message" && entry.message) {
				const msg = entry.message;
				const role = msg.role;
				if ((role === "user" || role === "assistant") && msg.content) {
					if (role === "user" && hasInterSessionUserProvenance(msg)) continue;
					const text = Array.isArray(msg.content) ? msg.content.find((c) => c.type === "text")?.text : msg.content;
					if (text && !text.startsWith("/")) allMessages.push(`${role}: ${text}`);
				}
			}
		} catch {}
		return allMessages.slice(-messageCount).join("\n");
	} catch {
		return null;
	}
}
/**
* Try the active transcript first; if /new already rotated it,
* fallback to the latest .jsonl.reset.* sibling.
*/
async function getRecentSessionContentWithResetFallback(sessionFilePath, messageCount = 15) {
	const primary = await getRecentSessionContent(sessionFilePath, messageCount);
	if (primary) return primary;
	try {
		const dir = path.dirname(sessionFilePath);
		const resetPrefix = `${path.basename(sessionFilePath)}.reset.`;
		const resetCandidates = (await fs.readdir(dir)).filter((name) => name.startsWith(resetPrefix)).toSorted();
		if (resetCandidates.length === 0) return primary;
		const latestResetPath = path.join(dir, resetCandidates[resetCandidates.length - 1]);
		const fallback = await getRecentSessionContent(latestResetPath, messageCount);
		if (fallback) log.debug("Loaded session content from reset fallback", {
			sessionFilePath,
			latestResetPath
		});
		return fallback || primary;
	} catch {
		return primary;
	}
}
function stripResetSuffix(fileName) {
	const resetIndex = fileName.indexOf(".reset.");
	return resetIndex === -1 ? fileName : fileName.slice(0, resetIndex);
}
async function findPreviousSessionFile(params) {
	try {
		const files = await fs.readdir(params.sessionsDir);
		const fileSet = new Set(files);
		const baseFromReset = params.currentSessionFile ? stripResetSuffix(path.basename(params.currentSessionFile)) : void 0;
		if (baseFromReset && fileSet.has(baseFromReset)) return path.join(params.sessionsDir, baseFromReset);
		const trimmedSessionId = params.sessionId?.trim();
		if (trimmedSessionId) {
			const canonicalFile = `${trimmedSessionId}.jsonl`;
			if (fileSet.has(canonicalFile)) return path.join(params.sessionsDir, canonicalFile);
			const topicVariants = files.filter((name) => name.startsWith(`${trimmedSessionId}-topic-`) && name.endsWith(".jsonl") && !name.includes(".reset.")).toSorted().toReversed();
			if (topicVariants.length > 0) return path.join(params.sessionsDir, topicVariants[0]);
		}
		if (!params.currentSessionFile) return;
		const nonResetJsonl = files.filter((name) => name.endsWith(".jsonl") && !name.includes(".reset.")).toSorted().toReversed();
		if (nonResetJsonl.length > 0) return path.join(params.sessionsDir, nonResetJsonl[0]);
	} catch {}
}
/**
* Save session context to memory when /new or /reset command is triggered
*/
const saveSessionToMemory = async (event) => {
	const isResetCommand = event.action === "new" || event.action === "reset";
	if (event.type !== "command" || !isResetCommand) return;
	try {
		log.debug("Hook triggered for reset/new command", { action: event.action });
		const context = event.context || {};
		const cfg = context.cfg;
		const agentId = resolveAgentIdFromSessionKey(event.sessionKey);
		const workspaceDir = cfg ? resolveAgentWorkspaceDir(cfg, agentId) : path.join(resolveStateDir(process.env, os.homedir), "workspace");
		const memoryDir = path.join(workspaceDir, "memory");
		await fs.mkdir(memoryDir, { recursive: true });
		const now = new Date(event.timestamp);
		const dateStr = now.toISOString().split("T")[0];
		const sessionEntry = context.previousSessionEntry || context.sessionEntry || {};
		const currentSessionId = sessionEntry.sessionId;
		let currentSessionFile = sessionEntry.sessionFile || void 0;
		if (!currentSessionFile || currentSessionFile.includes(".reset.")) {
			const sessionsDirs = /* @__PURE__ */ new Set();
			if (currentSessionFile) sessionsDirs.add(path.dirname(currentSessionFile));
			sessionsDirs.add(path.join(workspaceDir, "sessions"));
			for (const sessionsDir of sessionsDirs) {
				const recoveredSessionFile = await findPreviousSessionFile({
					sessionsDir,
					currentSessionFile,
					sessionId: currentSessionId
				});
				if (!recoveredSessionFile) continue;
				currentSessionFile = recoveredSessionFile;
				log.debug("Found previous session file", { file: currentSessionFile });
				break;
			}
		}
		log.debug("Session context resolved", {
			sessionId: currentSessionId,
			sessionFile: currentSessionFile,
			hasCfg: Boolean(cfg)
		});
		const sessionFile = currentSessionFile || void 0;
		const hookConfig = resolveHookConfig(cfg, "session-memory");
		const messageCount = typeof hookConfig?.messages === "number" && hookConfig.messages > 0 ? hookConfig.messages : 15;
		let slug = null;
		let sessionContent = null;
		if (sessionFile) {
			sessionContent = await getRecentSessionContentWithResetFallback(sessionFile, messageCount);
			log.debug("Session content loaded", {
				length: sessionContent?.length ?? 0,
				messageCount
			});
			const allowLlmSlug = !(process.env.OPENCLAW_TEST_FAST === "1" || process.env.VITEST === "true" || process.env.VITEST === "1" || false) && hookConfig?.llmSlug !== false;
			if (sessionContent && cfg && allowLlmSlug) {
				log.debug("Calling generateSlugViaLLM...");
				slug = await generateSlugViaLLM({
					sessionContent,
					cfg
				});
				log.debug("Generated slug", { slug });
			}
		}
		if (!slug) {
			slug = now.toISOString().split("T")[1].split(".")[0].replace(/:/g, "").slice(0, 4);
			log.debug("Using fallback timestamp slug", { slug });
		}
		const filename = `${dateStr}-${slug}.md`;
		const memoryFilePath = path.join(memoryDir, filename);
		log.debug("Memory file path resolved", {
			filename,
			path: memoryFilePath.replace(os.homedir(), "~")
		});
		const timeStr = now.toISOString().split("T")[1].split(".")[0];
		const sessionId = sessionEntry.sessionId || "unknown";
		const source = context.commandSource || "unknown";
		const entryParts = [
			`# Session: ${dateStr} ${timeStr} UTC`,
			"",
			`- **Session Key**: ${event.sessionKey}`,
			`- **Session ID**: ${sessionId}`,
			`- **Source**: ${source}`,
			""
		];
		if (sessionContent) entryParts.push("## Conversation Summary", "", sessionContent, "");
		await writeFileWithinRoot({
			rootDir: memoryDir,
			relativePath: filename,
			data: entryParts.join("\n"),
			encoding: "utf-8"
		});
		log.debug("Memory file written successfully");
		const relPath = memoryFilePath.replace(os.homedir(), "~");
		log.info(`Session context saved to ${relPath}`);
	} catch (err) {
		if (err instanceof Error) log.error("Failed to save session memory", {
			errorName: err.name,
			errorMessage: err.message,
			stack: err.stack
		});
		else log.error("Failed to save session memory", { error: String(err) });
	}
};

//#endregion
export { saveSessionToMemory as default };