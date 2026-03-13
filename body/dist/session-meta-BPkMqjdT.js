import { t as __exportAll } from "./rolldown-runtime-Cbj13DAv.js";
import { c as recordSessionMetaFromInbound } from "./sessions-Oj8tiZLJ.js";
import { s as resolveStorePath } from "./paths--yrwKtJp.js";

//#region src/channels/session-meta.ts
var session_meta_exports = /* @__PURE__ */ __exportAll({ recordInboundSessionMetaSafe: () => recordInboundSessionMetaSafe });
async function recordInboundSessionMetaSafe(params) {
	const storePath = resolveStorePath(params.cfg.session?.store, { agentId: params.agentId });
	try {
		await recordSessionMetaFromInbound({
			storePath,
			sessionKey: params.sessionKey,
			ctx: params.ctx
		});
	} catch (err) {
		params.onError?.(err);
	}
}

//#endregion
export { session_meta_exports as n, recordInboundSessionMetaSafe as t };