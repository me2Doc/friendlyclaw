import "./paths-BBP4yd-2.js";
import { p as theme } from "./globals-DyWRcjQY.js";
import "./utils-xFiJOAuL.js";
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
import "./message-channel-iOBej-45.js";
import "./tailnet-B0iMa3fv.js";
import "./ws-j0__CWxN.js";
import "./client-eOXd-Nak.js";
import "./call-NYL7YiAM.js";
import "./pairing-token-DuijwWQW.js";
import "./runtime-config-collectors-zuZeqj0p.js";
import "./command-secret-targets-CcRJSelN.js";
import { t as formatDocsLink } from "./links-C_8X69xU.js";
import { n as registerQrCli } from "./qr-cli-WG8jMiSD.js";

//#region src/cli/clawbot-cli.ts
function registerClawbotCli(program) {
	registerQrCli(program.command("clawbot").description("Legacy clawbot command aliases").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/clawbot", "docs.openclaw.ai/cli/clawbot")}\n`));
}

//#endregion
export { registerClawbotCli };