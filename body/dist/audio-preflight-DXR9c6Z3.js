import "./paths-BBP4yd-2.js";
import { a as logVerbose, c as shouldLogVerbose } from "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
import "./thinking-44rmAw5o.js";
import "./agent-scope-lcHHTjPm.js";
import "./subsystem-BfkFJ4uQ.js";
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
import { d as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-BoyUdfw0.js";
import "./image-2Bk1vmbn.js";
import "./models-config-C-XXfu7J.js";
import "./pi-model-discovery-B_3w5ebP.js";
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
import "./fetch-guard-DffejaoP.js";
import "./api-key-rotation-5wHpygo9.js";
import "./local-roots-CaKaWHKu.js";
import "./model-catalog-C3SO4Y0b.js";
import "./proxy-fetch-IfymuHXF.js";

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