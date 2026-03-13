import "./paths-BBP4yd-2.js";
import { p as theme } from "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
import "./thinking-44rmAw5o.js";
import "./agent-scope-lcHHTjPm.js";
import { d as defaultRuntime } from "./subsystem-BfkFJ4uQ.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DOAKKqsf.js";
import "./exec-C1jYNNci.js";
import "./model-selection-CjMYMtR0.js";
import "./github-copilot-token-b6kJVrW-.js";
import "./boolean-BsqeuxE6.js";
import "./env-o3cHIFWK.js";
import "./host-env-security-DkAVVuaw.js";
import "./env-vars-Cs8xIArf.js";
import "./registry-Dih4j9AI.js";
import "./manifest-registry-D__tUCLh.js";
import "./dock-DXD7B6uA.js";
import "./message-channel-iOBej-45.js";
import "./pi-embedded-helpers-WkKFkFQ7.js";
import "./sandbox-D2wbSKUX.js";
import "./tool-catalog-6nGolBD5.js";
import "./chrome-6xxAgKnD.js";
import "./tailscale-Bu3Gbo9s.js";
import "./tailnet-B0iMa3fv.js";
import "./ws-j0__CWxN.js";
import "./auth-D5QF8d44.js";
import "./server-context-UtYz8B-5.js";
import "./frontmatter-ByDncoXD.js";
import "./skills-CgJQu758.js";
import "./path-alias-guards-BKPifPiz.js";
import "./paths-D6PWtrIM.js";
import "./redact-Cl6kEomM.js";
import "./errors-BmWNPXkt.js";
import "./fs-safe-2ZPbjCmk.js";
import "./proxy-env-DQgMiRoV.js";
import "./image-ops-Bq4eA8UY.js";
import "./store-DlP4j4Js.js";
import "./ports-B5sn4_rk.js";
import "./trash-C5hclNOU.js";
import "./server-middleware-DKdQGR92.js";
import "./sessions-XdimqNx2.js";
import "./plugins-DeWZwV_l.js";
import "./accounts-dRSkNPbF.js";
import "./accounts-B_f8R6HO.js";
import "./logging-ADUQX6n5.js";
import "./accounts-DueMu7dK.js";
import "./bindings-D10iRlwL.js";
import "./paths-Db_9vfXk.js";
import "./chat-envelope-CjZ3-rvQ.js";
import "./tool-images-BWPsBENR.js";
import "./tool-display-BZdJCRfR.js";
import "./commands-DjMqttDa.js";
import "./commands-registry-DHlKvB9V.js";
import "./client-eOXd-Nak.js";
import "./call-NYL7YiAM.js";
import "./pairing-token-DuijwWQW.js";
import { t as formatDocsLink } from "./links-C_8X69xU.js";
import { t as parseTimeoutMs } from "./parse-timeout-DrSLkPL_.js";
import { t as runTui } from "./tui-BVnE3UgW.js";

//#region src/cli/tui-cli.ts
function registerTuiCli(program) {
	program.command("tui").description("Open a terminal UI connected to the Gateway").option("--url <url>", "Gateway WebSocket URL (defaults to gateway.remote.url when configured)").option("--token <token>", "Gateway token (if required)").option("--password <password>", "Gateway password (if required)").option("--session <key>", "Session key (default: \"main\", or \"global\" when scope is global)").option("--deliver", "Deliver assistant replies", false).option("--thinking <level>", "Thinking level override").option("--message <text>", "Send an initial message after connecting").option("--timeout-ms <ms>", "Agent timeout in ms (defaults to agents.defaults.timeoutSeconds)").option("--history-limit <n>", "History entries to load", "200").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/tui", "docs.openclaw.ai/cli/tui")}\n`).action(async (opts) => {
		try {
			const timeoutMs = parseTimeoutMs(opts.timeoutMs);
			if (opts.timeoutMs !== void 0 && timeoutMs === void 0) defaultRuntime.error(`warning: invalid --timeout-ms "${String(opts.timeoutMs)}"; ignoring`);
			const historyLimit = Number.parseInt(String(opts.historyLimit ?? "200"), 10);
			await runTui({
				url: opts.url,
				token: opts.token,
				password: opts.password,
				session: opts.session,
				deliver: Boolean(opts.deliver),
				thinking: opts.thinking,
				message: opts.message,
				timeoutMs,
				historyLimit: Number.isNaN(historyLimit) ? void 0 : historyLimit
			});
		} catch (err) {
			defaultRuntime.error(String(err));
			defaultRuntime.exit(1);
		}
	});
}

//#endregion
export { registerTuiCli };