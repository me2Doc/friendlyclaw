import "./agent-scope-DWsn5rte.js";
import "./paths-C6TxBCvO.js";
import { p as shouldLogVerbose, u as logVerbose } from "./subsystem-nlluZawe.js";
import "./utils-Dvtm0mzf.js";
import "./workspace-BU8QxCQK.js";
import "./logger-wD6tEZWm.js";
import "./model-selection-ikt2OC4j.js";
import "./env-BgFeGxoV.js";
import "./github-copilot-token-Dr6AUVHb.js";
import "./boolean-mcn6kL0s.js";
import "./internal-hooks-Y1c3CR6c.js";
import "./registry-ycXZ0GNV.js";
import "./dock-D49biwXh.js";
import "./plugins-noDEKrDH.js";
import "./accounts-DGCf7PCM.js";
import "./bindings-CtbdcwyF.js";
import "./accounts-C1iVq9v_.js";
import "./image-ops-0nwMDFtL.js";
import "./pi-model-discovery-DvKumK6n.js";
import "./message-channel-DZhYsPbp.js";
import "./pi-embedded-helpers-DvNaskDY.js";
import "./chrome-BJ1olan3.js";
import "./frontmatter-DIRc-IR1.js";
import "./skills-D3c_mBu8.js";
import "./path-alias-guards-CfaVCHQ7.js";
import "./redact-yC-5vZip.js";
import "./errors-0iO9hLII.js";
import "./fs-safe-CW7g83pG.js";
import "./proxy-env-Y95QXuB3.js";
import "./store-Dn1gZuiJ.js";
import "./sessions-_Cu6BqJv.js";
import "./accounts-C9nmgL8E.js";
import "./paths-B8Ne8ciC.js";
import "./tool-images-Bcm94hV8.js";
import "./thinking-FnAYAFD8.js";
import "./image-5e0tgQ1Z.js";
import { g as isAudioAttachment, i as normalizeMediaAttachments, o as resolveMediaAttachmentLocalRoots, t as runAudioTranscription } from "./audio-transcription-runner-DYom1Phd.js";
import "./fetch-DJLxHaLt.js";
import "./fetch-guard-C23rIR_K.js";
import "./api-key-rotation-BeJ-Lf5S.js";
import "./proxy-fetch-DrI0Gh6p.js";

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