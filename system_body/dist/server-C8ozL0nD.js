import "./globals-d3aR1MYC.js";
import "./paths-BMo6kTge.js";
import { t as createSubsystemLogger } from "./subsystem-kl-vrkYi.js";
import "./boolean-DtWR5bt3.js";
import { F as loadConfig } from "./auth-profiles-CNyDTsy4.js";
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
import "./path-alias-guards-BLnvB3eQ.js";
import "./net-Bf8Z-b6p.js";
import "./tailnet-Dei3mqID.js";
import { t as isPwAiLoaded } from "./diagnostic-session-state-CDEk5vOn.js";
import "./image-ops-B1XQ8UAg.js";
import "./chrome-Dt8bkIrk.js";
import "./tailscale-CcmGuDnz.js";
import "./auth-C24xIErm.js";
import { c as resolveBrowserControlAuth, i as resolveBrowserConfig, r as registerBrowserRoutes, s as ensureBrowserControlAuth, t as createBrowserRouteContext } from "./server-context-CBtC0TLR.js";
import "./paths-8MkNWbbj.js";
import "./redact-kP6dI-RQ.js";
import "./errors-DrflaMHL.js";
import "./fs-safe-kadrhuVr.js";
import "./proxy-env-BxxPVbHn.js";
import "./store-D0GaA-PU.js";
import "./ports-DuT3O3nk.js";
import "./trash-CzgjR7DR.js";
import { n as installBrowserCommonMiddleware, t as installBrowserAuthMiddleware } from "./server-middleware-BwkaybNn.js";
import { n as stopKnownBrowserProfiles, t as ensureExtensionRelayForProfiles } from "./server-lifecycle-BfrWnmUb.js";
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
		await (await import("./pw-ai-gGTz8ayf.js")).closePlaywrightBrowserConnection();
	} catch {}
}

//#endregion
export { startBrowserControlServerFromConfig, stopBrowserControlServer };