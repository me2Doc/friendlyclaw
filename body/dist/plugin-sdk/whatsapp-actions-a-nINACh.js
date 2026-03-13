import { i as resolveWhatsAppAccount } from "./accounts-CCsyRzgq.js";
import "./paths-MKyEVmEb.js";
import "./github-copilot-token-D5fdS6xD.js";
import "./config-GHoFNNPc.js";
import "./subsystem-QV9R1a2-.js";
import "./utils--zJ6K5WT.js";
import "./command-format-D1BnT4u1.js";
import "./agent-scope-Rx3XjZIq.js";
import "./logger-Ber8CW5F.js";
import "./registry-DmSqCQJS.js";
import "./message-channel-C0jRZuxZ.js";
import "./plugins-BmrNmh_7.js";
import "./bindings-DnPvYgC3.js";
import "./path-alias-guards-BurZu1bF.js";
import "./fs-safe-BJFxj5_x.js";
import "./image-ops-lixKaBrx.js";
import "./ssrf-CNFE2mLw.js";
import "./fetch-guard-TrC02Qcz.js";
import "./local-roots-DQ5uREi7.js";
import "./ir-B7tRnYSY.js";
import "./chunk-CHx5Q3Qu.js";
import "./markdown-tables-CueDW0Jl.js";
import "./render-CRfOWrdg.js";
import "./tables-S1tFA5ZE.js";
import "./tool-images-CrVWvj9m.js";
import { f as readReactionParams, h as readStringParam, i as ToolAuthorizationError, l as jsonResult, o as createActionGate } from "./target-errors-DMn1WrA2.js";
import { t as resolveWhatsAppOutboundTarget } from "./resolve-outbound-target-DEbS8TYI.js";
import { r as sendReactionWhatsApp } from "./outbound-CtufLPaa.js";

//#region src/agents/tools/whatsapp-target-auth.ts
function resolveAuthorizedWhatsAppOutboundTarget(params) {
	const account = resolveWhatsAppAccount({
		cfg: params.cfg,
		accountId: params.accountId
	});
	const resolution = resolveWhatsAppOutboundTarget({
		to: params.chatJid,
		allowFrom: account.allowFrom ?? [],
		mode: "implicit"
	});
	if (!resolution.ok) throw new ToolAuthorizationError(`WhatsApp ${params.actionLabel} blocked: chatJid "${params.chatJid}" is not in the configured allowFrom list for account "${account.accountId}".`);
	return {
		to: resolution.to,
		accountId: account.accountId
	};
}

//#endregion
//#region src/agents/tools/whatsapp-actions.ts
async function handleWhatsAppAction(params, cfg) {
	const action = readStringParam(params, "action", { required: true });
	const isActionEnabled = createActionGate(cfg.channels?.whatsapp?.actions);
	if (action === "react") {
		if (!isActionEnabled("reactions")) throw new Error("WhatsApp reactions are disabled.");
		const chatJid = readStringParam(params, "chatJid", { required: true });
		const messageId = readStringParam(params, "messageId", { required: true });
		const { emoji, remove, isEmpty } = readReactionParams(params, { removeErrorMessage: "Emoji is required to remove a WhatsApp reaction." });
		const participant = readStringParam(params, "participant");
		const accountId = readStringParam(params, "accountId");
		const fromMeRaw = params.fromMe;
		const fromMe = typeof fromMeRaw === "boolean" ? fromMeRaw : void 0;
		const resolved = resolveAuthorizedWhatsAppOutboundTarget({
			cfg,
			chatJid,
			accountId,
			actionLabel: "reaction"
		});
		const resolvedEmoji = remove ? "" : emoji;
		await sendReactionWhatsApp(resolved.to, messageId, resolvedEmoji, {
			verbose: false,
			fromMe,
			participant: participant ?? void 0,
			accountId: resolved.accountId
		});
		if (!remove && !isEmpty) return jsonResult({
			ok: true,
			added: emoji
		});
		return jsonResult({
			ok: true,
			removed: true
		});
	}
	throw new Error(`Unsupported WhatsApp action: ${action}`);
}

//#endregion
export { handleWhatsAppAction };