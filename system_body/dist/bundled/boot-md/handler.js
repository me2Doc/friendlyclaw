import { n as listAgentIds, s as resolveAgentWorkspaceDir } from "../../agent-scope-DWsn5rte.js";
import "../../paths-C6TxBCvO.js";
import { i as defaultRuntime, t as createSubsystemLogger } from "../../subsystem-nlluZawe.js";
import { u as resolveAgentIdFromSessionKey } from "../../session-key-a6av96Fj.js";
import "../../utils-Dvtm0mzf.js";
import "../../workspace-BU8QxCQK.js";
import "../../logger-wD6tEZWm.js";
import "../../model-selection-ikt2OC4j.js";
import "../../env-BgFeGxoV.js";
import "../../github-copilot-token-Dr6AUVHb.js";
import "../../boolean-mcn6kL0s.js";
import { r as isGatewayStartupEvent } from "../../internal-hooks-Y1c3CR6c.js";
import "../../registry-ycXZ0GNV.js";
import "../../dock-D49biwXh.js";
import { n as SILENT_REPLY_TOKEN } from "../../tokens-BXGWtt7T.js";
import { i as createDefaultDeps, r as agentCommand } from "../../pi-embedded-CtM2Mrrj.js";
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
import "../../fs-safe-CW7g83pG.js";
import "../../proxy-env-Y95QXuB3.js";
import "../../store-Dn1gZuiJ.js";
import { U as resolveMainSessionKey, V as resolveAgentMainSessionKey, o as loadSessionStore, u as updateSessionStore } from "../../sessions-_Cu6BqJv.js";
import "../../accounts-C9nmgL8E.js";
import { s as resolveStorePath } from "../../paths-B8Ne8ciC.js";
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
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

//#region src/gateway/boot.ts
function generateBootSessionId() {
	return `boot-${(/* @__PURE__ */ new Date()).toISOString().replace(/[:.]/g, "-").replace("T", "_").replace("Z", "")}-${crypto.randomUUID().slice(0, 8)}`;
}
const log$1 = createSubsystemLogger("gateway/boot");
const BOOT_FILENAME = "BOOT.md";
function buildBootPrompt(content) {
	return [
		"You are running a boot check. Follow BOOT.md instructions exactly.",
		"",
		"BOOT.md:",
		content,
		"",
		"If BOOT.md asks you to send a message, use the message tool (action=send with channel + target).",
		"Use the `target` field (not `to`) for message tool destinations.",
		`After sending with the message tool, reply with ONLY: ${SILENT_REPLY_TOKEN}.`,
		`If nothing needs attention, reply with ONLY: ${SILENT_REPLY_TOKEN}.`
	].join("\n");
}
async function loadBootFile(workspaceDir) {
	const bootPath = path.join(workspaceDir, BOOT_FILENAME);
	try {
		const trimmed = (await fs.readFile(bootPath, "utf-8")).trim();
		if (!trimmed) return { status: "empty" };
		return {
			status: "ok",
			content: trimmed
		};
	} catch (err) {
		if (err.code === "ENOENT") return { status: "missing" };
		throw err;
	}
}
function snapshotMainSessionMapping(params) {
	const agentId = resolveAgentIdFromSessionKey(params.sessionKey);
	const storePath = resolveStorePath(params.cfg.session?.store, { agentId });
	try {
		const entry = loadSessionStore(storePath, { skipCache: true })[params.sessionKey];
		if (!entry) return {
			storePath,
			sessionKey: params.sessionKey,
			canRestore: true,
			hadEntry: false
		};
		return {
			storePath,
			sessionKey: params.sessionKey,
			canRestore: true,
			hadEntry: true,
			entry: structuredClone(entry)
		};
	} catch (err) {
		log$1.debug("boot: could not snapshot main session mapping", {
			sessionKey: params.sessionKey,
			error: String(err)
		});
		return {
			storePath,
			sessionKey: params.sessionKey,
			canRestore: false,
			hadEntry: false
		};
	}
}
async function restoreMainSessionMapping(snapshot) {
	if (!snapshot.canRestore) return;
	try {
		await updateSessionStore(snapshot.storePath, (store) => {
			if (snapshot.hadEntry && snapshot.entry) {
				store[snapshot.sessionKey] = snapshot.entry;
				return;
			}
			delete store[snapshot.sessionKey];
		}, { activeSessionKey: snapshot.sessionKey });
		return;
	} catch (err) {
		return err instanceof Error ? err.message : String(err);
	}
}
async function runBootOnce(params) {
	const bootRuntime = {
		log: () => {},
		error: (message) => log$1.error(String(message)),
		exit: defaultRuntime.exit
	};
	let result;
	try {
		result = await loadBootFile(params.workspaceDir);
	} catch (err) {
		const message = err instanceof Error ? err.message : String(err);
		log$1.error(`boot: failed to read ${BOOT_FILENAME}: ${message}`);
		return {
			status: "failed",
			reason: message
		};
	}
	if (result.status === "missing" || result.status === "empty") return {
		status: "skipped",
		reason: result.status
	};
	const sessionKey = params.agentId ? resolveAgentMainSessionKey({
		cfg: params.cfg,
		agentId: params.agentId
	}) : resolveMainSessionKey(params.cfg);
	const message = buildBootPrompt(result.content ?? "");
	const sessionId = generateBootSessionId();
	const mappingSnapshot = snapshotMainSessionMapping({
		cfg: params.cfg,
		sessionKey
	});
	let agentFailure;
	try {
		await agentCommand({
			message,
			sessionKey,
			sessionId,
			deliver: false,
			senderIsOwner: true
		}, bootRuntime, params.deps);
	} catch (err) {
		agentFailure = err instanceof Error ? err.message : String(err);
		log$1.error(`boot: agent run failed: ${agentFailure}`);
	}
	const mappingRestoreFailure = await restoreMainSessionMapping(mappingSnapshot);
	if (mappingRestoreFailure) log$1.error(`boot: failed to restore main session mapping: ${mappingRestoreFailure}`);
	if (!agentFailure && !mappingRestoreFailure) return { status: "ran" };
	return {
		status: "failed",
		reason: [agentFailure ? `agent run failed: ${agentFailure}` : void 0, mappingRestoreFailure ? `mapping restore failed: ${mappingRestoreFailure}` : void 0].filter((part) => Boolean(part)).join("; ")
	};
}

//#endregion
//#region src/hooks/bundled/boot-md/handler.ts
const log = createSubsystemLogger("hooks/boot-md");
const runBootChecklist = async (event) => {
	if (!isGatewayStartupEvent(event)) return;
	if (!event.context.cfg) return;
	const cfg = event.context.cfg;
	const deps = event.context.deps ?? createDefaultDeps();
	const agentIds = listAgentIds(cfg);
	for (const agentId of agentIds) {
		const workspaceDir = resolveAgentWorkspaceDir(cfg, agentId);
		const result = await runBootOnce({
			cfg,
			deps,
			workspaceDir,
			agentId
		});
		if (result.status === "failed") {
			log.warn("boot-md failed for agent startup run", {
				agentId,
				workspaceDir,
				reason: result.reason
			});
			continue;
		}
		if (result.status === "skipped") log.debug("boot-md skipped for agent startup run", {
			agentId,
			workspaceDir,
			reason: result.reason
		});
	}
};

//#endregion
export { runBootChecklist as default };