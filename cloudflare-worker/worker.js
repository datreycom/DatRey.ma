/**
 * DatRey Autopilot Cloudflare Worker
 * Triggers GitHub Actions workflow via repository_dispatch at 09:00, 12:00, and 20:00 Morocco Time.
 */
export default {
  // 1. Scheduled Cron Trigger (Cloudflare Global Edge)
  async scheduled(event, env, ctx) {
    console.log(`[Cloudflare Worker] Cron triggered at ${event.scheduledTime}`);
    const result = await triggerGitHubAutopilot(env);
    console.log(`[Cloudflare Worker] Trigger result: ${JSON.stringify(result)}`);
  },

  // 2. HTTP Fetch Handler (for manual trigger or webhook test)
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/trigger") {
      const result = await triggerGitHubAutopilot(env);
      return new Response(JSON.stringify(result, null, 2), {
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response("DatRey Autopilot Cloudflare Worker is Active 🚀\nEndpoints: /trigger", {
      headers: { "Content-Type": "text/plain; charset=utf-8" }
    });
  }
};

async function triggerGitHubAutopilot(env) {
  const repoOwner = "datreycom";
  const repoName = "DatRey.ma";
  const githubToken = env.GITHUB_TOKEN || "";

  const dispatchUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/dispatches`;

  try {
    const response = await fetch(dispatchUrl, {
      method: "POST",
      headers: {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": `Bearer ${githubToken}`,
        "User-Agent": "DatRey-Cloudflare-Worker",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        event_type: "trigger_autopilot",
        client_payload: {
          source: "cloudflare_worker_cron",
          triggered_at: new Date().toISOString()
        }
      })
    });

    if (response.ok || response.status === 204) {
      return { status: "success", code: response.status, message: "GitHub Actions Autopilot triggered successfully!" };
    } else {
      const errText = await response.text();
      return { status: "error", code: response.status, message: errText };
    }
  } catch (error) {
    return { status: "exception", error: error.message };
  }
}
