import "./paths-BBP4yd-2.js";
import { p as theme } from "./globals-DyWRcjQY.js";
import { S as shortenHomePath } from "./utils-xFiJOAuL.js";
import { E as ensureAgentWorkspace, _ as DEFAULT_AGENT_WORKSPACE_DIR } from "./agent-scope-lcHHTjPm.js";
import { d as defaultRuntime } from "./subsystem-BfkFJ4uQ.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DOAKKqsf.js";
import "./exec-C1jYNNci.js";
import { Jt as createConfigIO, tn as writeConfigFile } from "./model-selection-CjMYMtR0.js";
import "./github-copilot-token-b6kJVrW-.js";
import "./boolean-BsqeuxE6.js";
import "./env-o3cHIFWK.js";
import "./host-env-security-DkAVVuaw.js";
import "./env-vars-Cs8xIArf.js";
import "./registry-Dih4j9AI.js";
import "./manifest-registry-D__tUCLh.js";
import "./dock-DXD7B6uA.js";
import "./message-channel-iOBej-45.js";
import "./tailnet-B0iMa3fv.js";
import "./ws-j0__CWxN.js";
import "./redact-Cl6kEomM.js";
import "./errors-BmWNPXkt.js";
import "./sessions-XdimqNx2.js";
import "./plugins-DeWZwV_l.js";
import "./accounts-dRSkNPbF.js";
import "./accounts-B_f8R6HO.js";
import "./logging-ADUQX6n5.js";
import "./accounts-DueMu7dK.js";
import "./bindings-D10iRlwL.js";
import { o as resolveSessionTranscriptsDir } from "./paths-Db_9vfXk.js";
import "./chat-envelope-CjZ3-rvQ.js";
import "./client-eOXd-Nak.js";
import "./call-NYL7YiAM.js";
import "./pairing-token-DuijwWQW.js";
import "./onboard-helpers-BallfiRO.js";
import "./prompt-style-sSBOSp0c.js";
import { t as formatDocsLink } from "./links-C_8X69xU.js";
import { n as runCommandWithRuntime } from "./cli-utils-BAoBKJmP.js";
import "./progress-BZ6ybIkX.js";
import "./runtime-guard-Buo06NOu.js";
import { t as hasExplicitOptions } from "./command-options-CfGhT1Of.js";
import "./note-CLFObuHy.js";
import "./clack-prompter-B_7TLaHA.js";
import "./onboarding.secret-input-DEiy-G0p.js";
import "./onboarding-N833r5v5.js";
import { n as logConfigUpdated, t as formatConfigPath } from "./logging-uAKXu_UT.js";
import { t as onboardCommand } from "./onboard-DqaxSCSu.js";
import JSON5 from "json5";
import fs from "node:fs/promises";

//#region src/commands/setup.ts
async function readConfigFileRaw(configPath) {
	try {
		const raw = await fs.readFile(configPath, "utf-8");
		const parsed = JSON5.parse(raw);
		if (parsed && typeof parsed === "object") return {
			exists: true,
			parsed
		};
		return {
			exists: true,
			parsed: {}
		};
	} catch {
		return {
			exists: false,
			parsed: {}
		};
	}
}
async function setupCommand(opts, runtime = defaultRuntime) {
	const desiredWorkspace = typeof opts?.workspace === "string" && opts.workspace.trim() ? opts.workspace.trim() : void 0;
	const configPath = createConfigIO().configPath;
	const existingRaw = await readConfigFileRaw(configPath);
	const cfg = existingRaw.parsed;
	const defaults = cfg.agents?.defaults ?? {};
	const workspace = desiredWorkspace ?? defaults.workspace ?? DEFAULT_AGENT_WORKSPACE_DIR;
	const next = {
		...cfg,
		agents: {
			...cfg.agents,
			defaults: {
				...defaults,
				workspace
			}
		}
	};
	if (!existingRaw.exists || defaults.workspace !== workspace) {
		await writeConfigFile(next);
		if (!existingRaw.exists) runtime.log(`Wrote ${formatConfigPath(configPath)}`);
		else logConfigUpdated(runtime, {
			path: configPath,
			suffix: "(set agents.defaults.workspace)"
		});
	} else runtime.log(`Config OK: ${formatConfigPath(configPath)}`);
	const ws = await ensureAgentWorkspace({
		dir: workspace,
		ensureBootstrapFiles: !next.agents?.defaults?.skipBootstrap
	});
	runtime.log(`Workspace OK: ${shortenHomePath(ws.dir)}`);
	const sessionsDir = resolveSessionTranscriptsDir();
	await fs.mkdir(sessionsDir, { recursive: true });
	runtime.log(`Sessions OK: ${shortenHomePath(sessionsDir)}`);
}

//#endregion
//#region src/cli/program/register.setup.ts
function registerSetupCommand(program) {
	program.command("setup").description("Initialize ~/.openclaw/openclaw.json and the agent workspace").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/setup", "docs.openclaw.ai/cli/setup")}\n`).option("--workspace <dir>", "Agent workspace directory (default: ~/.openclaw/workspace; stored as agents.defaults.workspace)").option("--wizard", "Run the interactive onboarding wizard", false).option("--non-interactive", "Run the wizard without prompts", false).option("--mode <mode>", "Wizard mode: local|remote").option("--remote-url <url>", "Remote Gateway WebSocket URL").option("--remote-token <token>", "Remote Gateway token (optional)").action(async (opts, command) => {
		await runCommandWithRuntime(defaultRuntime, async () => {
			const hasWizardFlags = hasExplicitOptions(command, [
				"wizard",
				"nonInteractive",
				"mode",
				"remoteUrl",
				"remoteToken"
			]);
			if (opts.wizard || hasWizardFlags) {
				await onboardCommand({
					workspace: opts.workspace,
					nonInteractive: Boolean(opts.nonInteractive),
					mode: opts.mode,
					remoteUrl: opts.remoteUrl,
					remoteToken: opts.remoteToken
				}, defaultRuntime);
				return;
			}
			await setupCommand({ workspace: opts.workspace }, defaultRuntime);
		});
	});
}

//#endregion
export { registerSetupCommand };