import "./paths-BBP4yd-2.js";
import { L as shouldMigrateStateFromPath, d as colorize, f as isRich, p as theme } from "./globals-DyWRcjQY.js";
import { S as shortenHomePath } from "./utils-xFiJOAuL.js";
import "./agent-scope-lcHHTjPm.js";
import "./subsystem-BfkFJ4uQ.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DOAKKqsf.js";
import "./exec-C1jYNNci.js";
import { Zt as readConfigFileSnapshot } from "./model-selection-CjMYMtR0.js";
import "./github-copilot-token-b6kJVrW-.js";
import { t as formatCliCommand } from "./command-format-Gp1OUMPH.js";
import "./boolean-BsqeuxE6.js";
import "./env-o3cHIFWK.js";
import "./host-env-security-DkAVVuaw.js";
import "./env-vars-Cs8xIArf.js";
import "./registry-Dih4j9AI.js";
import "./manifest-registry-D__tUCLh.js";
import "./dock-DXD7B6uA.js";
import "./message-channel-iOBej-45.js";
import "./sessions-XdimqNx2.js";
import "./plugins-DeWZwV_l.js";
import "./accounts-dRSkNPbF.js";
import "./accounts-B_f8R6HO.js";
import "./logging-ADUQX6n5.js";
import "./accounts-DueMu7dK.js";
import "./bindings-D10iRlwL.js";
import "./paths-Db_9vfXk.js";
import "./chat-envelope-CjZ3-rvQ.js";
import "./pairing-store-DQtghpRv.js";
import "./exec-approvals-allowlist-D8qpSn28.js";
import "./exec-safe-bin-runtime-policy-CEOPu7_h.js";
import "./plugin-auto-enable-CyReXbA7.js";
import "./prompt-style-sSBOSp0c.js";
import "./note-CLFObuHy.js";
import { n as formatConfigIssueLines } from "./issue-format-CR1DQPs7.js";
import { t as loadAndMaybeMigrateDoctorConfig } from "./doctor-config-flow-qpEYb7-O.js";

//#region src/cli/program/config-guard.ts
const ALLOWED_INVALID_COMMANDS = new Set([
	"doctor",
	"logs",
	"health",
	"help",
	"status"
]);
const ALLOWED_INVALID_GATEWAY_SUBCOMMANDS = new Set([
	"status",
	"probe",
	"health",
	"discover",
	"call",
	"install",
	"uninstall",
	"start",
	"stop",
	"restart"
]);
let didRunDoctorConfigFlow = false;
let configSnapshotPromise = null;
function resetConfigGuardStateForTests() {
	didRunDoctorConfigFlow = false;
	configSnapshotPromise = null;
}
async function getConfigSnapshot() {
	if (process.env.VITEST === "true") return readConfigFileSnapshot();
	configSnapshotPromise ??= readConfigFileSnapshot();
	return configSnapshotPromise;
}
async function ensureConfigReady(params) {
	const commandPath = params.commandPath ?? [];
	if (!didRunDoctorConfigFlow && shouldMigrateStateFromPath(commandPath)) {
		didRunDoctorConfigFlow = true;
		const runDoctorConfigFlow = async () => loadAndMaybeMigrateDoctorConfig({
			options: { nonInteractive: true },
			confirm: async () => false
		});
		if (!params.suppressDoctorStdout) await runDoctorConfigFlow();
		else {
			const originalStdoutWrite = process.stdout.write.bind(process.stdout);
			const originalSuppressNotes = process.env.OPENCLAW_SUPPRESS_NOTES;
			process.stdout.write = (() => true);
			process.env.OPENCLAW_SUPPRESS_NOTES = "1";
			try {
				await runDoctorConfigFlow();
			} finally {
				process.stdout.write = originalStdoutWrite;
				if (originalSuppressNotes === void 0) delete process.env.OPENCLAW_SUPPRESS_NOTES;
				else process.env.OPENCLAW_SUPPRESS_NOTES = originalSuppressNotes;
			}
		}
	}
	const snapshot = await getConfigSnapshot();
	const commandName = commandPath[0];
	const subcommandName = commandPath[1];
	const allowInvalid = commandName ? ALLOWED_INVALID_COMMANDS.has(commandName) || commandName === "gateway" && subcommandName && ALLOWED_INVALID_GATEWAY_SUBCOMMANDS.has(subcommandName) : false;
	const issues = snapshot.exists && !snapshot.valid ? formatConfigIssueLines(snapshot.issues, "-", { normalizeRoot: true }) : [];
	const legacyIssues = snapshot.legacyIssues.length > 0 ? formatConfigIssueLines(snapshot.legacyIssues, "-") : [];
	if (!(snapshot.exists && !snapshot.valid)) return;
	const rich = isRich();
	const muted = (value) => colorize(rich, theme.muted, value);
	const error = (value) => colorize(rich, theme.error, value);
	const heading = (value) => colorize(rich, theme.heading, value);
	const commandText = (value) => colorize(rich, theme.command, value);
	params.runtime.error(heading("Config invalid"));
	params.runtime.error(`${muted("File:")} ${muted(shortenHomePath(snapshot.path))}`);
	if (issues.length > 0) {
		params.runtime.error(muted("Problem:"));
		params.runtime.error(issues.map((issue) => `  ${error(issue)}`).join("\n"));
	}
	if (legacyIssues.length > 0) {
		params.runtime.error(muted("Legacy config keys detected:"));
		params.runtime.error(legacyIssues.map((issue) => `  ${error(issue)}`).join("\n"));
	}
	params.runtime.error("");
	params.runtime.error(`${muted("Run:")} ${commandText(formatCliCommand("openclaw doctor --fix"))}`);
	if (!allowInvalid) params.runtime.exit(1);
}
const __test__ = { resetConfigGuardStateForTests };

//#endregion
export { __test__, ensureConfigReady };