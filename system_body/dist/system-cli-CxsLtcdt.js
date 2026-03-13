import { p as theme, t as danger } from "./globals-d3aR1MYC.js";
import "./paths-BMo6kTge.js";
import { d as defaultRuntime } from "./subsystem-kl-vrkYi.js";
import "./boolean-DtWR5bt3.js";
import "./auth-profiles-CNyDTsy4.js";
import "./agent-scope-DuFk7JfV.js";
import "./utils-cwpAMi-t.js";
import "./openclaw-root-BFfBQ6FD.js";
import "./logger-BFQv53Hf.js";
import "./exec-t2VHjaVf.js";
import "./github-copilot-token-Byc_YVYE.js";
import "./host-env-security-lcjXF83D.js";
import "./version-B7TNfFMY.js";
import "./env-vars-mSSOl7Rv.js";
import "./registry-ds-_TqV5.js";
import "./manifest-registry-DKS5Msti.js";
import "./message-channel-vD1W0gaU.js";
import "./client-CuIxivDk.js";
import "./call-DaJKh-6e.js";
import "./pairing-token-DfIpR3Pw.js";
import "./net-Bf8Z-b6p.js";
import "./tailnet-Dei3mqID.js";
import { t as formatDocsLink } from "./links-BMokj3K3.js";
import "./progress-CcvPqJyX.js";
import { n as callGatewayFromCli, t as addGatewayClientOptions } from "./gateway-rpc-Mk08XvhP.js";

//#region src/cli/system-cli.ts
const normalizeWakeMode = (raw) => {
	const mode = typeof raw === "string" ? raw.trim() : "";
	if (!mode) return "next-heartbeat";
	if (mode === "now" || mode === "next-heartbeat") return mode;
	throw new Error("--mode must be now or next-heartbeat");
};
async function runSystemGatewayCommand(opts, action, successText) {
	try {
		const result = await action();
		if (opts.json || successText === void 0) defaultRuntime.log(JSON.stringify(result, null, 2));
		else defaultRuntime.log(successText);
	} catch (err) {
		defaultRuntime.error(danger(String(err)));
		defaultRuntime.exit(1);
	}
}
function registerSystemCli(program) {
	const system = program.command("system").description("System tools (events, heartbeat, presence)").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/system", "docs.openclaw.ai/cli/system")}\n`);
	addGatewayClientOptions(system.command("event").description("Enqueue a system event and optionally trigger a heartbeat").requiredOption("--text <text>", "System event text").option("--mode <mode>", "Wake mode (now|next-heartbeat)", "next-heartbeat").option("--json", "Output JSON", false)).action(async (opts) => {
		await runSystemGatewayCommand(opts, async () => {
			const text = typeof opts.text === "string" ? opts.text.trim() : "";
			if (!text) throw new Error("--text is required");
			return await callGatewayFromCli("wake", opts, {
				mode: normalizeWakeMode(opts.mode),
				text
			}, { expectFinal: false });
		}, "ok");
	});
	const heartbeat = system.command("heartbeat").description("Heartbeat controls");
	addGatewayClientOptions(heartbeat.command("last").description("Show the last heartbeat event").option("--json", "Output JSON", false)).action(async (opts) => {
		await runSystemGatewayCommand(opts, async () => {
			return await callGatewayFromCli("last-heartbeat", opts, void 0, { expectFinal: false });
		});
	});
	addGatewayClientOptions(heartbeat.command("enable").description("Enable heartbeats").option("--json", "Output JSON", false)).action(async (opts) => {
		await runSystemGatewayCommand(opts, async () => {
			return await callGatewayFromCli("set-heartbeats", opts, { enabled: true }, { expectFinal: false });
		});
	});
	addGatewayClientOptions(heartbeat.command("disable").description("Disable heartbeats").option("--json", "Output JSON", false)).action(async (opts) => {
		await runSystemGatewayCommand(opts, async () => {
			return await callGatewayFromCli("set-heartbeats", opts, { enabled: false }, { expectFinal: false });
		});
	});
	addGatewayClientOptions(system.command("presence").description("List system presence entries").option("--json", "Output JSON", false)).action(async (opts) => {
		await runSystemGatewayCommand(opts, async () => {
			return await callGatewayFromCli("system-presence", opts, void 0, { expectFinal: false });
		});
	});
}

//#endregion
export { registerSystemCli };