// Pi adapter: registers the codara-mcp stdio server. Secrets are inherited from the environment.
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function codara(pi: ExtensionAPI) {
  pi.registerMcpServer("codara", { command: "uvx", timeout: 600, description: "Semantic codebase retrieval and exact repository search", args: ["--from", "git+https://github.com/sitien173/codara-mcp", "codara-mcp"] });
}
