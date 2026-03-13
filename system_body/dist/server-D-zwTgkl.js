import "./paths-BBP4yd-2.js";
import "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
import "./agent-scope-lcHHTjPm.js";
import { t as createSubsystemLogger } from "./subsystem-BfkFJ4uQ.js";
import "./openclaw-root-DeEQQJyX.js";
import "./logger-DOAKKqsf.js";
import "./exec-C1jYNNci.js";
import { Yt as loadConfig } from "./model-selection-CjMYMtR0.js";
import "./github-copilot-token-b6kJVrW-.js";
import "./boolean-BsqeuxE6.js";
import "./env-o3cHIFWK.js";
import "./host-env-security-DkAVVuaw.js";
import "./env-vars-Cs8xIArf.js";
import "./registry-Dih4j9AI.js";
import "./manifest-registry-D__tUCLh.js";
import "./chrome-6xxAgKnD.js";
import "./tailscale-Bu3Gbo9s.js";
import "./tailnet-B0iMa3fv.js";
import "./ws-j0__CWxN.js";
import "./auth-D5QF8d44.js";
import { c as resolveBrowserControlAuth, i as resolveBrowserConfig, r as registerBrowserRoutes, s as ensureBrowserControlAuth, t as createBrowserRouteContext } from "./server-context-UtYz8B-5.js";
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
import { n as installBrowserCommonMiddleware, t as installBrowserAuthMiddleware } from "./server-middleware-DKdQGR92.js";
import { t as isPwAiLoaded } from "./diagnostic-session-state-BdsrlXSG.js";
import { n as stopKnownBrowserProfiles, t as ensureExtensionRelayForProfiles } from "./server-lifecycle-CkCwt54j.js";
import express from "express";

//#region src/browser/server.ts
let state = null;
const logServer = createSubsystemLogger("browser").child("server");
async function startBrowserControlServerFromConfig() {
	if (state) return state;
	const cfg = loadConfig();
	const resolved = resolveBrowserConfig(cfg.browser, cfg);
	if (!resolved.enabled) return null;
	let browserAuth = resolveBrowserControlAuth(cfg);
	let browserAuthBootstrapFailed = false;
	try {
		const ensured = await ensureBrowserControlAuth({ cfg });
		browserAuth = ensured.auth;
		if (ensured.generatedToken) logServer.info("No browser auth configured; generated gateway.auth.token automatically.");
	} catch (err) {
		logServer.warn(`failed to auto-configure browser auth: ${String(err)}`);
		browserAuthBootstrapFailed = true;
	}
	if (browserAuthBootstrapFailed && !browserAuth.token && !browserAuth.password) {
		logServer.error("browser control startup aborted: authentication bootstrap failed and no fallback auth is configured.");
		return null;
	}
	const app = express();
	installBrowserCommonMiddleware(app);
	installBrowserAuthMiddleware(app, browserAuth);
	registerBrowserRoutes(app, createBrowserRouteContext({
		getState: () => state,
		refreshConfigFromDisk: true
	}));
	const port = resolved.controlPort;
	const server = await new Promise((resolve, reject) => {
		const s = app.listen(port, "127.0.0.1", () => resolve(s));
		s.once("error", reject);
	}).catch((err) => {
		logServer.error(`openclaw browser server failed to bind 127.0.0.1:${port}: ${String(err)}`);
		return null;
	});
	if (!server) return null;
	state = {
		server,
		port,
		resolved,
		profiles: /* @__PURE__ */ new Map()
	};
	await ensureExtensionRelayForProfiles({
		resolved,
		onWarn: (message) => logServer.warn(message)
	});
	const authMode = browserAuth.token ? "token" : browserAuth.password ? "password" : "off";
	logServer.info(`Browser control listening on http://127.0.0.1:${port}/ (auth=${authMode})`);
	return state;
}
async function stopBrowserControlServer() {
	const current = state;
	if (!current) return;
	await stopKnownBrowserProfiles({
		getState: () => state,
		onWarn: (message) => logServer.warn(message)
	});
	if (current.server) await new Promise((resolve) => {
		current.server?.close(() => resolve());
	});
	state = null;
	if (isPwAiLoaded()) try {
		await (await import("./pw-ai-CVJHvi3I.js")).closePlaywrightBrowserConnection();
	} catch {}
}

//#endregion
export { startBrowserControlServerFromConfig, stopBrowserControlServer };