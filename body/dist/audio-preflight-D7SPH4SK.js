import { a as logVerbose, c as shouldLogVerbose } from "./globals-d3aR1MYC.js";
import "./paths-BMo6kTge.js";
import "./subsystem-kl-vrkYi.js";
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
import "./dock-ChE50rbQ.js";
import "./pi-model-discovery-DTh-dRmO.js";
import "./frontmatter-BLUo-dxn.js";
import "./skills-B9NkSU2u.js";
import "./path-alias-guards-BLnvB3eQ.js";
import "./message-channel-vD1W0gaU.js";
import "./sessions-DNn6Jbbx.js";
import "./plugins-Co0ormRA.js";
import "./accounts-zRQn433-.js";
import "./accounts-K1IaOhUI.js";
import "./logging-CcxUDNcI.js";
import "./accounts-C35KnEXA.js";
import "./bindings-vxn_WYGq.js";
import "./paths-Bn3zjTqJ.js";
import "./chat-envelope-AUuZAcrC.js";
import "./net-Bf8Z-b6p.js";
import "./tailnet-Dei3mqID.js";
import "./image-ops-B1XQ8UAg.js";
import "./pi-embedded-helpers-q7AlAFu4.js";
import "./sandbox-BTk3jOUP.js";
import "./tool-catalog-CDe8aNjS.js";
import "./chrome-Dt8bkIrk.js";
import "./tailscale-CcmGuDnz.js";
import "./auth-C24xIErm.js";
import "./server-context-CBtC0TLR.js";
import "./paths-8MkNWbbj.js";
import "./redact-kP6dI-RQ.js";
import "./errors-DrflaMHL.js";
import "./fs-safe-kadrhuVr.js";
import "./proxy-env-BxxPVbHn.js";
import "./store-D0GaA-PU.js";
import "./ports-DuT3O3nk.js";
import "./trash-CzgjR7DR.js";
import "./server-middleware-BwkaybNn.js";
import "./tool-images-BCnln0pJ.js";
import "./thinking-BxCyPtl0.js";
import "./models-config-ERyMYjbg.js";
import "./model-catalog-qZGHxvcI.js";
import "./fetch-C79EVYRM.js";
import { _ as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-Bq3uEE74.js";
import "./fetch-guard-BUZ81J83.js";
import "./image-BfgjMXod.js";
import "./tool-display-3t3R7qfs.js";
import "./api-key-rotation-Coo663aY.js";
import "./proxy-fetch-D397Vi7A.js";

//#region src/media-understanding/audio-preflight.ts
/**
* Transcribes the first audio attachment BEFORE mention checking.
* This allows voice notes to be processed in group chats with requireMention: true.
* Returns the transcript or undefined if transcription fails or no audio is found.
*/
async function transcribeFirstAudio(params) {
	const { ctx, cfg } = params;
	const audioConfig = cfg.tools?.media?.audio;
	if (!audioConfig || audioConfig.enabled === false) return;
	const attachments = normalizeMediaAttachments(ctx);
	if (!attachments || attachments.length === 0) return;
	const firstAudio = attachments.find((att) => att && isAudioAttachment(att) && !att.alreadyTranscribed);
	if (!firstAudio) return;
	if (shouldLogVerbose()) logVerbose(`audio-preflight: transcribing attachment ${firstAudio.index} for mention check`);
	try {
		const { transcript } = await runAudioTranscription({
			ctx,
			cfg,
			attachments,
			agentDir: params.agentDir,
			providers: params.providers,
			activeModel: params.activeModel,
			localPathRoots: resolveMediaAttachmentLocalRoots({
				cfg,
				ctx
			})
		});
		if (!transcript) return;
		firstAudio.alreadyTranscribed = true;
		if (shouldLogVerbose()) logVerbose(`audio-preflight: transcribed ${transcript.length} chars from attachment ${firstAudio.index}`);
		return transcript;
	} catch (err) {
		if (shouldLogVerbose()) logVerbose(`audio-preflight: transcription failed: ${String(err)}`);
		return;
	}
}

//#endregion
export { transcribeFirstAudio };