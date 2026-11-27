(() => {
  "use strict";

  const official = window.REI_REVIEW_DATA.actions.find(action => action.key === "rei-school::waiting");
  const pilot = window.REI_PILOT_DATA;
  const storageKey = "rei-codex-cloud-art-pilot-v1";
  const recordType = "rei-codex-cloud-art-pilot";
  const pending = "PENDING_HUMAN_REVIEW";
  const statuses = [pending, "ACCEPTED", "NEEDS_FIX", "REJECTED"];
  const get = id => document.getElementById("pilot-" + id);
  const sampleSelect = get("sample");
  const frameSelect = get("frame");
  const oldImage = get("old");
  const newImage = get("new");
  const statusSelect = get("status");
  const comment = get("comment");

  const samples = new Map(pilot.samples.map(sample => [sample.id, sample]));
  const knownFocus = {
    face: [96, 35], chest: [96, 66], hands: [99, 94], feet: [96, 189],
  };
  let frame = 0;
  let timer = null;
  let playing = false;
  let point = null;
  let records = {};

  function selected() {
    return samples.get(sampleSelect.value);
  }

  function binding(sample) {
    return {
      candidate: {
        version: sample.version,
        source: sample.sourceSha256,
        frames: sample.frames.map(entry => entry.sha256),
      },
      reference: sample.id === "waiting" ? {
        version: official.selected_version,
        source: official.source_sha256,
        frames: official.frames.map(entry => entry.sha256),
      } : { version: pilot.blackMaster.version, source: pilot.blackMaster.sha256, frames: [] },
    };
  }

  function sameCandidate(saved, active) {
    return saved?.version === active.version && saved.source === active.source
      && Array.isArray(saved.frames) && saved.frames.length === active.frames.length
      && active.frames.every((hash, i) => saved.frames[i] === hash);
  }

  function importRecords(payload) {
    if (payload?.type !== recordType || payload.schema_version !== 1 || !Array.isArray(payload.decisions)) {
      throw new Error("文件格式不兼容，请使用专项试验的 JSON。");
    }
    const next = {};
    const seen = new Set();
    let stale = 0;
    for (const decision of payload.decisions) {
      if (!decision || !samples.has(decision.id) || seen.has(decision.id)
          || !statuses.includes(decision.status) || typeof decision.comment !== "string") {
        throw new Error("试验验收记录无效。");
      }
      seen.add(decision.id);
      const expected = binding(samples.get(decision.id));
      if (!sameCandidate(decision.binding?.candidate, expected.candidate)
          || !sameCandidate(decision.binding?.reference, expected.reference)) {
        stale += 1;
      } else {
        next[decision.id] = {status: decision.status, comment: decision.comment};
      }
    }
    records = next;
    return stale;
  }

  function payload() {
    return {
      type: recordType,
      schema_version: 1,
      decisions: [...samples.values()].map(sample => ({
        id: sample.id,
        ...(records[sample.id] || {status: pending, comment: ""}),
        binding: binding(sample),
      })),
    };
  }

  function persist() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(payload()));
    } catch {
      get("message").textContent = "浏览器未能保存草稿。请导出试验 JSON。";
      return false;
    }
    return true;
  }

  function renderSummary() {
    const decided = [...samples.values()].filter(sample => records[sample.id]?.status
      && records[sample.id].status !== pending);
    const frames = decided.reduce((sum, sample) => sum + sample.frames.length, 0);
    get("summary").textContent = `已判定 ${decided.length}/${samples.size} 项 · ${frames}/${pilot.frameCount} 帧`;
  }

  function renderReview() {
    const sample = selected();
    statusSelect.value = records[sample.id]?.status || pending;
    comment.value = records[sample.id]?.comment || "";
    renderSummary();

    const bindings = get("bindings");
    bindings.replaceChildren();
    const active = binding(sample);
    for (const [label, item] of [["试验候选", active.candidate], ["参考", active.reference]]) {
      const values = [[label + "版本", item.version], [label + "原图 SHA-256", item.source]];
      item.frames.forEach((hash, i) => values.push([`${label} F${i + 1} SHA-256`, hash]));
      for (const [name, value] of values) {
        const dt = document.createElement("dt");
        const dd = document.createElement("dd");
        dt.textContent = name;
        dd.textContent = value;
        bindings.append(dt, dd);
      }
    }
  }

  function drawLoupe(image, canvas) {
    const focus = get("focus").value;
    const [x, y] = point || knownFocus[focus];
    const zoom = Number(get("zoom").value);
    const side = canvas.width / zoom;
    const left = Math.max(0, Math.min(192 - side, x - side / 2));
    const top = Math.max(0, Math.min(208 - side, y - side / 2));
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas.dataset.focus = point ? "custom" : focus;
    if (image.complete && image.naturalWidth) {
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(image, left, top, side, side, 0, 0, canvas.width, canvas.height);
    }
  }

  function drawLoupes() {
    if (selected().id === "waiting") drawLoupe(oldImage, get("old-loupe"));
    drawLoupe(newImage, get("new-loupe"));
  }

  function renderFrame() {
    const sample = selected();
    const waiting = sample.id === "waiting";
    const number = waiting ? frame + 1 : 1;
    if (waiting) {
      oldImage.src = official.frames[frame].src;
      oldImage.dataset.frame = number;
      get("timing").textContent = `${official.durations_ms[frame]} ms`;
    }
    newImage.src = sample.frames[number - 1].src;
    newImage.dataset.frame = number;
    frameSelect.value = String(frame);
    drawLoupes();
  }

  function setPlaying(value) {
    clearTimeout(timer);
    playing = value;
    const button = get("play");
    button.textContent = value ? "暂停" : "播放";
    button.setAttribute("aria-pressed", String(value));
    if (value) {
      timer = setTimeout(() => {
        frame = (frame + 1) % official.frames.length;
        renderFrame();
        setPlaying(true);
      }, official.durations_ms[frame]);
    }
  }

  function stepTo(index) {
    setPlaying(false);
    frame = (index + official.frames.length) % official.frames.length;
    renderFrame();
  }

  function renderSample() {
    const sample = selected();
    const waiting = sample.id === "waiting";
    get("reference").classList.toggle("hidden", !waiting);
    get("transport").classList.toggle("hidden", !waiting);
    get("caption").textContent = waiting ? "试验 waiting" : `试验黑服 ${sample.id}°`;
    get("links").replaceChildren();
    for (const {label, src} of pilot.links[waiting ? "waiting" : "directions"]) {
      const a = document.createElement("a");
      a.href = src;
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = label;
      get("links").append(a);
    }
    renderFrame();
    renderReview();
  }

  function updateRecord() {
    records[selected().id] = {status: statusSelect.value, comment: comment.value};
    persist();
    renderSummary();
  }

  sampleSelect.addEventListener("change", () => {
    setPlaying(false);
    frame = 0;
    point = null;
    renderSample();
  });
  get("play").addEventListener("click", () => setPlaying(!playing));
  get("prev").addEventListener("click", () => stepTo(frame - 1));
  get("next").addEventListener("click", () => stepTo(frame + 1));
  frameSelect.addEventListener("change", () => stepTo(Number(frameSelect.value)));
  get("background").addEventListener("change", event => {
    get("visuals").dataset.background = event.target.value;
  });
  get("focus").addEventListener("change", () => {
    point = null;
    drawLoupes();
  });
  get("zoom").addEventListener("change", drawLoupes);
  for (const image of [oldImage, newImage]) {
    image.addEventListener("load", drawLoupes);
    image.addEventListener("click", event => {
      const box = image.getBoundingClientRect();
      point = [(event.clientX - box.left) * 192 / box.width, (event.clientY - box.top) * 208 / box.height];
      drawLoupes();
    });
  }
  statusSelect.addEventListener("change", updateRecord);
  comment.addEventListener("input", updateRecord);
  get("import").addEventListener("change", async event => {
    const [file] = event.target.files;
    if (!file) return;
    try {
      const stale = importRecords(JSON.parse(await file.text()));
      renderReview();
      if (persist()) {
        get("message").textContent = stale ? `${stale} 项哈希或版本已变，已回退为待审。` : "已导入试验验收记录。";
      }
    } catch (error) {
      get("message").textContent = error instanceof SyntaxError ? "文件不是有效的 JSON。" : error.message;
    } finally {
      event.target.value = "";
    }
  });
  get("export").addEventListener("click", () => {
    const href = URL.createObjectURL(new Blob([JSON.stringify(payload(), null, 2)], {type: "application/json"}));
    const a = document.createElement("a");
    a.href = href;
    a.download = "REI_CODEX_CLOUD_PILOT_REVIEW.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(href), 1000);
  });
  try {
    const draft = localStorage.getItem(storageKey);
    if (draft) {
      const stale = importRecords(JSON.parse(draft));
      if (stale) get("message").textContent = `${stale} 项哈希或版本已变，已回退为待审。`;
    }
  } catch {
    get("message").textContent = "无法读取本地试验草稿。";
  }
  renderSample();
})();
