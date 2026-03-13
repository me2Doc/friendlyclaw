import { p as theme } from "./globals-d3aR1MYC.js";
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
import "./message-channel-vD1W0gaU.js";
import "./client-CuIxivDk.js";
import "./call-DaJKh-6e.js";
import "./pairing-token-DfIpR3Pw.js";
import "./net-Bf8Z-b6p.js";
import "./tailnet-Dei3mqID.js";
import "./runtime-config-collectors-BJhmqEOW.js";
import "./command-secret-targets-B3asrqY0.js";
import { t as formatDocsLink } from "./links-BMokj3K3.js";
import { n as registerQrCli } from "./qr-cli-BBXZ71Yj.js";

//#region src/cli/clawbot-cli.ts
function registerClawbotCli(program) {
	registerQrCli(program.command("clawbot").description("Legacy clawbot command aliases").addHelpText("after", () => `\n${theme.muted("Docs:")} ${formatDocsLink("/cli/clawbot", "docs.openclaw.ai/cli/clawbot")}\n`));
}

//#endregion
export { registerClawbotCli };