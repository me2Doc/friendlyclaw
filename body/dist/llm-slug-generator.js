import { a as resolveAgentEffectiveModelPrimary, c as resolveDefaultAgentId, i as resolveAgentDir, s as resolveAgentWorkspaceDir } from "./agent-scope-DWsn5rte.js";
import "./paths-C6TxBCvO.js";
import { t as createSubsystemLogger } from "./subsystem-nlluZawe.js";
import "./utils-Dvtm0mzf.js";
import "./workspace-BU8QxCQK.js";
import "./logger-wD6tEZWm.js";
import { Jn as DEFAULT_PROVIDER, l as parseModelRef, qn as DEFAULT_MODEL } from "./model-selection-ikt2OC4j.js";
import "./env-BgFeGxoV.js";
import "./github-copilot-token-Dr6AUVHb.js";
import "./boolean-mcn6kL0s.js";
import "./internal-hooks-Y1c3CR6c.js";
import "./registry-ycXZ0GNV.js";
import "./dock-D49biwXh.js";
import "./tokens-BXGWtt7T.js";
import { t as runEmbeddedPiAgent } from "./pi-embedded-CtM2Mrrj.js";
import "./plugins-noDEKrDH.js";
import "./accounts-DGCf7PCM.js";
import "./bindings-CtbdcwyF.js";
import "./send-DVuCXZhB.js";
import "./send-Mhq_NgNz.js";
import "./deliver-FEreRY0J.js";
import "./diagnostic-C-4UTg3h.js";
import "./diagnostic-session-state-DBPrVBk3.js";
import "./accounts-C1iVq9v_.js";
import "./send-BjxxplhK.js";
import "./image-ops-0nwMDFtL.js";
import "./pi-model-discovery-DvKumK6n.js";
import "./message-channel-DZhYsPbp.js";
import "./pi-embedded-helpers-DvNaskDY.js";
import "./chrome-BJ1olan3.js";
import "./frontmatter-DIRc-IR1.js";
import "./skills-D3c_mBu8.js";
import "./path-alias-guards-CfaVCHQ7.js";
import "./redact-yC-5vZip.js";
import "./errors-0iO9hLII.js";
import "./fs-safe-CW7g83pG.js";
import "./proxy-env-Y95QXuB3.js";
import "./store-Dn1gZuiJ.js";
import "./sessions-_Cu6BqJv.js";
import "./accounts-C9nmgL8E.js";
import "./paths-B8Ne8ciC.js";
import "./tool-images-Bcm94hV8.js";
import "./thinking-FnAYAFD8.js";
import "./image-5e0tgQ1Z.js";
import "./audio-transcription-runner-DYom1Phd.js";
import "./fetch-DJLxHaLt.js";
import "./fetch-guard-C23rIR_K.js";
import "./api-key-rotation-BeJ-Lf5S.js";
import "./proxy-fetch-DrI0Gh6p.js";
import "./reply-prefix-DlRGjs31.js";
import "./chunk-Cgy4C3Nh.js";
import "./markdown-tables-KowmfLDF.js";
import "./ir-B6xHv9oi.js";
import "./render-flG67HhW.js";
import "./target-errors-C4l9j6WQ.js";
import "./commands-registry-D7j4kc5h.js";
import "./skill-commands-BaeDAEuP.js";
import "./fetch-CIXnD4u2.js";
import "./channel-activity-Do4UxjWY.js";
import "./tables-B_RTd-mr.js";
import "./send-Cwk6REJC.js";
import "./outbound-attachment-DkDekuYo.js";
import "./send-P4PvriEH.js";
import "./resolve-route-DCfod4Po.js";
import "./proxy-D6pp6ZSj.js";
import "./replies-Bkdfnyoh.js";
import "./session-meta-D3MMUgfg.js";
import "./manager--qQfR6iR.js";
import "./query-expansion-CeyLNalm.js";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

//#region src/hooks/llm-slug-generator.ts
/**
* LLM-based slug generator for session memory filenames
*/
const log = createSubsystemLogger("llm-slug-generator");
/**
* Generate a short 1-2 word filename slug from session content using LLM
*/
async function generateSlugViaLLM(params) {
	let tempSessionFile = null;
	try {
		const agentId = resolveDefaultAgentId(params.cfg);
		const workspaceDir = resolveAgentWorkspaceDir(params.cfg, agentId);
		const agentDir = resolveAgentDir(params.cfg, agentId);
		const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "openclaw-slug-"));
		tempSessionFile = path.join(tempDir, "session.jsonl");
		const prompt = `Based on this conversation, generate a short 1-2 word filename slug (lowercase, hyphen-separated, no file extension).

Conversation summary:
${params.sessionContent.slice(0, 2e3)}

Reply with ONLY the slug, nothing else. Examples: "vendor-pitch", "api-design", "bug-fix"`;
		const modelRef = resolveAgentEffectiveModelPrimary(params.cfg, agentId);
		const parsed = modelRef ? parseModelRef(modelRef, DEFAULT_PROVIDER) : null;
		const provider = parsed?.provider ?? DEFAULT_PROVIDER;
		const model = parsed?.model ?? DEFAULT_MODEL;
		const result = await runEmbeddedPiAgent({
			sessionId: `slug-generator-${Date.now()}`,
			sessionKey: "temp:slug-generator",
			agentId,
			sessionFile: tempSessionFile,
			workspaceDir,
			agentDir,
			config: params.cfg,
			prompt,
			provider,
			model,
			timeoutMs: 15e3,
			runId: `slug-gen-${Date.now()}`
		});
		if (result.payloads && result.payloads.length > 0) {
			const text = result.payloads[0]?.text;
			if (text) return text.trim().toLowerCase().replace(/[^a-z0-9-]/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "").slice(0, 30) || null;
		}
		return null;
	} catch (err) {
		const message = err instanceof Error ? err.stack ?? err.message : String(err);
		log.error(`Failed to generate slug: ${message}`);
		return null;
	} finally {
		if (tempSessionFile) try {
			await fs.rm(path.dirname(tempSessionFile), {
				recursive: true,
				force: true
			});
		} catch {}
	}
}

//#endregion
export { generateSlugViaLLM };