const form = document.getElementById("run-form");
const summary = document.getElementById("summary");
const timeline = document.getElementById("timeline");
const artifacts = document.getElementById("artifacts");
const artifactPath = document.getElementById("artifact-path");
const artifactContent = document.getElementById("artifact-content");

async function fetchArtifact(runId, path) {
  const response = await fetch(`/api/runs/${runId}/artifacts/${path}`);
  if (!response.ok) {
    artifactContent.textContent = "Failed to load artifact.";
    return;
  }
  artifactPath.textContent = path;
  artifactContent.textContent = await response.text();
}

function renderTimeline(events) {
  timeline.innerHTML = "";
  events.forEach((event) => {
    const item = document.createElement("div");
    item.className = "timeline-item";
    item.innerHTML = `
      <strong>${event.type}</strong>
      <small>${event.source}</small>
      <span>${new Date(event.created_at).toLocaleString()}</span>
    `;
    timeline.appendChild(item);
  });
}

function renderArtifacts(run) {
  artifacts.innerHTML = "";
  run.artifacts.forEach((artifact) => {
    const button = document.createElement("button");
    button.className = "artifact";
    button.type = "button";
    button.innerHTML = `
      <strong>${artifact.title}</strong>
      <span>${artifact.path}</span>
      <small>${artifact.kind}</small>
    `;
    button.addEventListener("click", () => fetchArtifact(run.id, artifact.path));
    artifacts.appendChild(button);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  summary.textContent = "正在执行长链编排...";
  timeline.innerHTML = "";
  artifacts.innerHTML = "";
  artifactContent.textContent = "运行中，请稍候。";
  artifactPath.textContent = "尚未选择工件";

  const payload = {
    project_name: form.project_name.value,
    prompt: form.prompt.value,
    target_repo: form.target_repo.value || null,
    preferred_stack: form.preferred_stack.value || null,
  };

  const response = await fetch("/api/runs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    summary.textContent = "任务执行失败。";
    artifactContent.textContent = await response.text();
    return;
  }

  const run = await response.json();
  summary.textContent = run.summary || "运行完成。";
  renderTimeline(run.events);
  renderArtifacts(run);
  if (run.artifacts.length > 0) {
    fetchArtifact(run.id, run.artifacts[0].path);
  }
});

