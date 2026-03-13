import "./agent-scope-C6B8oVI5.js";
import "./paths-CaA28K0s.js";
import { p as shouldLogVerbose, u as logVerbose } from "./subsystem-D46iuydz.js";
import "./utils-CNn3YdHZ.js";
import "./logger-CrpGldUe.js";
import "./model-selection-Zb7eBzSY.js";
import "./env-D5EE512c.js";
import "./github-copilot-token-By7PESfQ.js";
import "./registry-D1yqdHZn.js";
import "./dock-B5lLbKgi.js";
import "./plugins-BS8GH8mN.js";
import "./accounts-DNbMnBiO.js";
import "./bindings-D1Z3L5De.js";
import "./accounts-BZg2FIL0.js";
import "./image-ops-B2AqzJal.js";
import "./pi-model-discovery-D_XBKsjt.js";
import "./message-channel-DPcPK3Sd.js";
import "./pi-embedded-helpers-iGV05m9S.js";
import "./chrome-CdadObm0.js";
import "./skills-vKUYIsP-.js";
import "./path-alias-guards-DQpQ0x1n.js";
import "./redact-CA6oB4gc.js";
import "./errors-BpHSz0MX.js";
import "./fs-safe-B20zpZ_Z.js";
import "./proxy-env-BTrO34DI.js";
import "./store-WMptVzO3.js";
import "./sessions-Oj8tiZLJ.js";
import "./accounts-MwKflLwB.js";
import "./paths--yrwKtJp.js";
import "./tool-images-wfczWzTL.js";
import "./thinking-kXAj2UX9.js";
import "./image-DJDSkrdD.js";
import { g as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-nLJiJHj1.js";
import "./fetch-D3FeIe-t.js";
import "./fetch-guard-h6NrZCtQ.js";
import "./api-key-rotation-CwgIHp3a.js";
import "./proxy-fetch-Q2Qi-bwj.js";

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