(() => {
  "use strict";

  const get = suffix => document.getElementById("direction-" + suffix);
  const data = window.REI_DIRECTION_DATA;
  if (!data) {
    get("unavailable").classList.remove("hidden");
    return;
  }

  const formSelect = get("form");
  const angleSelect = get("angle");
  const statusSelect = get("status");
  const comment = get("comment");
  const recordType = "rei-p4c-direction-review";
  const storageKey = recordType + "::v1";
  const statuses = ["ACCEPTED", "PENDING_HUMAN_REVIEW", "NEEDS_FIX", "REJECTED"];
  const keyOf = ({form, angle}) => form + "::" + angle;
  const frames = new Map(data.frames.map(frame => [keyOf(frame), frame]));
  const records = new Map();

  for (const form of data.forms) {
    formSelect.add(new Option(form.label, form.id));
  }
  for (const angle of data.angles) {
    angleSelect.add(new Option(angle + "°", angle));
  }

  function selectedFrame() {
    return frames.get(keyOf({form: formSelect.value, angle: angleSelect.value}));
  }

  function decision(frame) {
    const {form, angle, version, sha256, source_sha256, origin, human_status} = frame;
    const record = records.get(keyOf(frame));
    return {
      form, angle, version, sha256, source_sha256, origin,
      status: origin === "REUSED_PILOT" ? human_status : record?.status ?? human_status,
      comment: record?.comment ?? "",
    };
  }

  function payload() {
    return {type: recordType, schema_version: 1, decisions: data.frames.map(decision)};
  }

  function importRecords(input) {
    if (input?.type !== recordType || input.schema_version !== 1 || !Array.isArray(input.decisions)) {
      throw new Error("请选择 P4-C 方向验收 JSON。");
    }
    const accepted = new Map();
    let skipped = 0;
    for (const entry of input.decisions) {
      const key = entry && keyOf(entry);
      const frame = frames.get(key);
      if (!frame || accepted.has(key)
        || entry.sha256 !== frame.sha256 || entry.source_sha256 !== frame.source_sha256
        || entry.version !== frame.version || entry.origin !== frame.origin
        || !statuses.includes(entry.status) || typeof entry.comment !== "string") {
        skipped++;
        continue;
      }
      accepted.set(key, {status: entry.status, comment: entry.comment});
    }
    for (const [key, record] of accepted) {
      records.set(key, record);
    }
    return skipped;
  }

  function renderCounts() {
    const results = [...frames.values()].map(decision);
    const counts = statuses.map(status => results.filter(item => item.status === status).length);
    const label = get("counts");
    label.dataset.counts = counts.join(",");
    label.textContent = `通过 ${counts[0]}（含复用 4） · 待审 ${counts[1]} · 需修复 ${counts[2]} · 拒收 ${counts[3]}`;
  }

  function render() {
    const frame = selectedFrame();
    const record = decision(frame);
    const image = get("img");
    const label = formSelect.selectedOptions[0].text;
    image.src = frame.src;
    image.alt = `${label} ${frame.angle}° 方向帧`;
    get("origin").textContent = frame.origin === "REUSED_PILOT"
      ? "复用已验收黑服基准帧" : "P4-C 新生成候选";
    get("slot").textContent = `Row ${frame.row} · Col ${frame.col} · ${frame.version}`;
    get("hash").textContent = frame.sha256;
    get("source-hash").textContent = frame.source_sha256;
    statusSelect.value = record.status;
    statusSelect.disabled = frame.origin === "REUSED_PILOT";
    comment.value = record.comment;
    renderCounts();
  }

  function persist() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(payload()));
      return true;
    } catch {
      get("message").textContent = "浏览器无法保存草稿。请导出方向 JSON。";
      return false;
    }
  }

  function update() {
    records.set(keyOf(selectedFrame()), {status: statusSelect.value, comment: comment.value});
    persist();
    renderCounts();
  }

  function step(delta) {
    const count = data.angles.length;
    angleSelect.selectedIndex = (angleSelect.selectedIndex + delta + count) % count;
    render();
  }

  formSelect.addEventListener("change", render);
  angleSelect.addEventListener("change", render);
  get("prev").addEventListener("click", () => step(-1));
  get("next").addEventListener("click", () => step(1));
  get("background").addEventListener("change", event => {
    get("stage").className = "bg-" + event.target.value;
  });
  statusSelect.addEventListener("change", update);
  comment.addEventListener("input", update);

  get("export").addEventListener("click", () => {
    const json = JSON.stringify(payload(), null, 2) + "\n";
    const url = URL.createObjectURL(new Blob([json], {type: "application/json"}));
    const link = document.createElement("a");
    link.href = url;
    link.download = "REI_P4C_DIRECTION_REVIEW.json";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 0);
  });

  get("import").addEventListener("change", async event => {
    const file = event.target.files[0];
    if (!file) return;
    try {
      const skipped = importRecords(JSON.parse(await file.text()));
      render();
      if (persist()) {
        get("message").textContent = skipped ? `导入完成，已跳过 ${skipped} 条无法绑定当前资产的记录。` : "导入完成。";
      }
    } catch (error) {
      get("message").textContent = error instanceof SyntaxError ? "方向 JSON 格式有误。" : error.message;
    } finally {
      event.target.value = "";
    }
  });

  try {
    const saved = localStorage.getItem(storageKey);
    if (saved && importRecords(JSON.parse(saved))) {
      get("message").textContent = "部分旧草稿无法绑定当前资产，已跳过。";
    }
  } catch {
    get("message").textContent = "无法加载本地草稿。可导入已导出的方向 JSON。";
  }
  get("review").classList.remove("hidden");
  render();
})();
