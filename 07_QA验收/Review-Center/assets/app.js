(() => {
  "use strict";

  const DATA = window.REI_REVIEW_DATA;
  if (!DATA || !Array.isArray(DATA.actions) || DATA.actions.length !== 27) {
    document.body.innerHTML =
      '<div style="padding:24px;color:#fca5a5;font-family:monospace;">ERROR: window.REI_REVIEW_DATA missing or invalid (expected 27 actions). Please ensure assets/review-data.js is present.</div>';
    return;
  }

  const STORAGE_KEY = "rei_review_center_v1_draft::" + DATA.manifest_fingerprint.slice(0, 16) + "::" + DATA.acceptance_sha256.slice(0, 16);
  const VALID_STATUSES = ["ACCEPTED", "REJECTED", "NEEDS_FIX", "PENDING"];
  const LOUPE_PRESETS = {
    chest: { x: 96, y: 108, label: "胸口 00/09 与领结" },
    face: { x: 96, y: 54, label: "面部表情与发饰" },
    hands: { x: 96, y: 132, label: "手臂与手指轮廓" },
    feet: { x: 96, y: 186, label: "鞋袜与锚点 (96,195)" },
  };

  // Lookup maps
  const actionByKey = new Map();
  for (const act of DATA.actions) {
    actionByKey.set(act.key, act);
  }
  const formById = new Map();
  for (const f of DATA.forms) {
    formById.set(f.id, f);
  }

  // Application state
  const state = {
    mode: "single",
    activeForm: "rei-school",
    activeState: "idle",
    currentFrame: 0,
    playing: true,
    loop: true,
    bg: "light",
    zoom: 2,
    pixelated: true,
    guides: false,
    filterStatus: "ALL",
    filterForm: "ALL",
    loupeZoom: 6,
    loupeCenter: { x: 96, y: 108 },
    markingSheet: "white",
    timerId: null,
    lastScheduledDurationMs: null,
    reviews: {},
  };

  // Preloaded Image cache for crisp zero-flicker loupe drawing
  const imgCache = new Map();
  function getLoadedImage(src, onLoad) {
    let entry = imgCache.get(src);
    if (!entry) {
      const img = new Image();
      entry = { img, loaded: false, listeners: [] };
      img.onload = () => {
        entry.loaded = true;
        const cbs = entry.listeners.splice(0);
        for (const cb of cbs) cb(img);
      };
      img.src = src;
      imgCache.set(src, entry);
    }
    if (entry.loaded) {
      if (onLoad) onLoad(entry.img);
    } else if (onLoad) {
      entry.listeners.push(onLoad);
    }
    return entry.img;
  }

  function arraysEqual(a, b) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) {
      if (a[i] !== b[i]) return false;
    }
    return true;
  }

  function buildBaselineReviews() {
    const out = {};
    for (const act of DATA.actions) {
      out[act.key] = {
        key: act.key,
        id: act.id,
        state: act.state,
        row: act.row,
        frame_count: act.frame_count,
        status: act.initial_status,
        comment: act.initial_comment || "",
        updated_at: act.initial_updated_at || null,
        selected_version: act.selected_version,
        source_sha256: act.source_sha256,
        action_asset_hash: act.action_asset_hash,
        frame_sha256s: act.frames.map((f) => f.sha256),
        locked_preapproved: Boolean(act.locked_preapproved),
        invalidated: false,
        invalidated_reason: null,
        stale_previous_status: null,
        stale_previous_asset_hash: null,
      };
    }
    return out;
  }

  function applyImportedPayload(payload, sourceLabel) {
    if (!payload || typeof payload !== "object") {
      throw new Error("导入文件不是合法 JSON 对象");
    }
    const items = Array.isArray(payload.decisions)
      ? payload.decisions
      : payload.reviews && typeof payload.reviews === "object"
        ? Object.values(payload.reviews)
        : null;
    if (!items) {
      throw new Error("JSON 缺少 decisions 数组或 reviews 映射字段");
    }

    const next = buildBaselineReviews();
    let matchedCount = 0;
    let invalidatedCount = 0;
    let unknownCount = 0;
    const invalidatedKeys = [];

    for (const raw of items) {
      if (!raw || typeof raw !== "object") continue;
      const key = raw.key || (raw.id && raw.state ? `${raw.id}::${raw.state}` : null);
      if (!key || !actionByKey.has(key)) {
        unknownCount++;
        continue;
      }
      const act = actionByKey.get(key);
      const currentFrameHashes = act.frames.map((f) => f.sha256);
      const importedStatus = VALID_STATUSES.includes(raw.status) ? raw.status : "PENDING";
      const importedHash = raw.action_asset_hash || null;
      const importedVersion = raw.selected_version || null;
      const importedFrameHashes = Array.isArray(raw.frame_sha256s) ? raw.frame_sha256s : null;

      const mismatchReasons = [];
      if (importedHash !== act.action_asset_hash) {
        mismatchReasons.push(`action_asset_hash 不一致 (导入=${importedHash || "缺失"}, 当前=${act.action_asset_hash})`);
      }
      if (importedVersion && importedVersion !== act.selected_version) {
        mismatchReasons.push(`selected_version 不一致 (导入=${importedVersion}, 当前=${act.selected_version})`);
      }
      if (importedFrameHashes && !arraysEqual(importedFrameHashes, currentFrameHashes)) {
        mismatchReasons.push("frame_sha256s 存在单帧哈希变化");
      }

      const hasHashMismatch = mismatchReasons.length > 0;
      if (hasHashMismatch && importedStatus !== "PENDING") {
        invalidatedCount++;
        invalidatedKeys.push(key);
        next[key] = {
          ...next[key],
          status: "PENDING",
          comment: typeof raw.comment === "string" ? raw.comment : "",
          updated_at: raw.updated_at || null,
          invalidated: true,
          invalidated_reason: mismatchReasons.join("；"),
          stale_previous_status: importedStatus,
          stale_previous_asset_hash: importedHash,
        };
      } else {
        next[key] = {
          ...next[key],
          status: hasHashMismatch ? "PENDING" : importedStatus,
          comment: typeof raw.comment === "string" ? raw.comment : "",
          updated_at: raw.updated_at || null,
          invalidated: hasHashMismatch,
          invalidated_reason: hasHashMismatch ? mismatchReasons.join("；") : null,
          stale_previous_status: hasHashMismatch ? importedStatus : null,
          stale_previous_asset_hash: hasHashMismatch ? importedHash : null,
        };
        if (hasHashMismatch) {
          invalidatedCount++;
          invalidatedKeys.push(key);
        }
      }
      matchedCount++;
    }

    state.reviews = next;
    persistDraft();
    renderAll();

    const msg =
      invalidatedCount > 0
        ? `已导入 ${sourceLabel}：匹配 ${matchedCount} 条，其中 ${invalidatedCount} 条因资产哈希变化已自动失效并回退为 PENDING。`
        : `已导入 ${sourceLabel}：成功校验并载入 ${matchedCount} 条动作验收记录（0 哈希失效）。`;
    showToast(msg);
    return { matchedCount, invalidatedCount, unknownCount, invalidatedKeys };
  }

  function persistDraft() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(buildExportPayload()));
    } catch (_) {
      // Ignore storage quota / private mode failures cleanly
    }
  }

  function loadInitialReviews() {
    state.reviews = buildBaselineReviews();
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        applyImportedPayload(parsed, "本地草稿");
        return;
      }
    } catch (_) {
      state.reviews = buildBaselineReviews();
    }
  }

  function computeSummary() {
    const actionsByStatus = { ACCEPTED: 0, NEEDS_FIX: 0, REJECTED: 0, PENDING: 0 };
    const framesByStatus = { ACCEPTED: 0, NEEDS_FIX: 0, REJECTED: 0, PENDING: 0 };
    let invalidatedActions = 0;

    for (const act of DATA.actions) {
      const rec = state.reviews[act.key];
      const st = rec ? rec.status : "PENDING";
      actionsByStatus[st] = (actionsByStatus[st] || 0) + 1;
      framesByStatus[st] = (framesByStatus[st] || 0) + act.frame_count;
      if (rec && rec.invalidated) invalidatedActions++;
    }
    return {
      total_actions: DATA.actions.length,
      total_frames: DATA.total_frames,
      actions_by_status: actionsByStatus,
      frames_by_status: framesByStatus,
      invalidated_actions: invalidatedActions,
    };
  }

  function buildExportPayload() {
    const summary = computeSummary();
    return {
      schema_version: 1,
      project: "rei-desktop-pet",
      tool: "Rei Review Center V1.0",
      stage: DATA.stage,
      baseline_commit: DATA.baseline_commit,
      manifest_fingerprint: DATA.manifest_fingerprint,
      exported_at: new Date().toISOString(),
      structure_pass_never_auto_accepted: true,
      summary,
      decisions: DATA.actions.map((act) => {
        const r = state.reviews[act.key];
        return {
          key: act.key,
          id: act.id,
          state: act.state,
          row: act.row,
          frame_count: act.frame_count,
          status: r.status,
          comment: r.comment,
          updated_at: r.updated_at,
          selected_version: act.selected_version,
          source_sha256: act.source_sha256,
          action_asset_hash: act.action_asset_hash,
          frame_sha256s: act.frames.map((f) => f.sha256),
          locked_preapproved: Boolean(act.locked_preapproved),
          invalidated: Boolean(r.invalidated),
          invalidated_reason: r.invalidated_reason || null,
          stale_previous_status: r.stale_previous_status || null,
          stale_previous_asset_hash: r.stale_previous_asset_hash || null,
        };
      }),
    };
  }

  function buildMarkdownSummary() {
    const payload = buildExportPayload();
    const s = payload.summary;
    const lines = [
      "# Rei Desktop Pet｜P4-B 人工美术验收摘要",
      "",
      `- **导出时间**：\`${payload.exported_at}\``,
      `- **资产基线指纹**：\`${payload.manifest_fingerprint}\``,
      `- **总进度（动作）**：ACCEPTED \`${s.actions_by_status.ACCEPTED}/27\` · NEEDS_FIX \`${s.actions_by_status.NEEDS_FIX}\` · REJECTED \`${s.actions_by_status.REJECTED}\` · PENDING \`${s.actions_by_status.PENDING}\``,
      `- **总进度（帧数）**：ACCEPTED \`${s.frames_by_status.ACCEPTED}/171\` · NEEDS_FIX \`${s.frames_by_status.NEEDS_FIX}\` · REJECTED \`${s.frames_by_status.REJECTED}\` · PENDING \`${s.frames_by_status.PENDING}\``,
      `- **哈希失效记录数**：\`${s.invalidated_actions}\``,
      "",
      "## 3×9 动作验收总表",
      "",
      "| Row | 状态 | 形态 | 帧数 | 候选版本 | 人工验收状态 | 资产哈希(前12位) | 验收意见 |",
      "| ---: | --- | --- | ---: | --- | :---: | --- | --- |",
    ];
    for (const d of payload.decisions) {
      const note = (d.comment || "—").replace(/\r?\n/g, " ").replace(/\|/g, "\\|");
      const statusLabel = d.invalidated ? `${d.status} (HASH_INVALIDATED)` : d.status;
      lines.push(
        `| ${d.row} | \`${d.state}\` | \`${d.id}\` | ${d.frame_count} | \`${d.selected_version}\` | **${statusLabel}** | \`${d.action_asset_hash.slice(0, 12)}\` | ${note} |`
      );
    }

    const actionItems = payload.decisions.filter((d) => d.status === "NEEDS_FIX" || d.status === "REJECTED");
    lines.push("", "## 需修复 / 拒收清单（供 P4-B-FIX 精确排期）", "");
    if (actionItems.length === 0) {
      lines.push("- 当前暂无标记为 `NEEDS_FIX` 或 `REJECTED` 的动作。");
    } else {
      for (const d of actionItems) {
        lines.push(`- **\`${d.id} / ${d.state}\`** (\`${d.status}\`, ${d.frame_count} 帧, hash \`${d.action_asset_hash.slice(0, 12)}\`)：${d.comment || "（未填写备注）"}`);
      }
    }
    return lines.join("\n") + "\n";
  }

  // Toast helper
  let toastTimer = null;
  function showToast(msg) {
    const el = document.getElementById("toastBar");
    el.textContent = msg;
    el.classList.remove("hidden");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.add("hidden"), 4500);
  }

  function getActiveAction() {
    return actionByKey.get(`${state.activeForm}::${state.activeState}`);
  }

  function getStateActions(stateName) {
    return DATA.forms.map((f) => actionByKey.get(`${f.id}::${stateName}`));
  }

  // Strict Frozen-Timing Playback Scheduler
  function stopTimer() {
    if (state.timerId !== null) {
      clearTimeout(state.timerId);
      state.timerId = null;
    }
  }

  function scheduleNextTick() {
    stopTimer();
    if (!state.playing) return;
    const act = getActiveAction();
    const durations = act.durations_ms;
    const idx = state.currentFrame % durations.length;
    const delay = durations[idx];
    state.lastScheduledDurationMs = delay;
    state.timerId = setTimeout(() => {
      const nextIdx = state.currentFrame + 1;
      if (nextIdx >= act.frame_count) {
        if (state.loop) {
          state.currentFrame = 0;
        } else {
          state.playing = false;
          updateTransportUI();
          return;
        }
      } else {
        state.currentFrame = nextIdx;
      }
      renderFrameViews();
      scheduleNextTick();
    }, delay);
  }

  function setPlaying(shouldPlay) {
    state.playing = Boolean(shouldPlay);
    updateTransportUI();
    if (state.playing) {
      scheduleNextTick();
    } else {
      stopTimer();
    }
  }

  function stepFrame(delta) {
    const act = getActiveAction();
    setPlaying(false);
    state.currentFrame = (state.currentFrame + delta + act.frame_count) % act.frame_count;
    renderFrameViews();
  }

  function selectAction(formId, stateName, switchMode) {
    const changedState = state.activeState !== stateName;
    state.activeForm = formId;
    state.activeState = stateName;
    if (changedState) {
      state.currentFrame = 0;
    } else {
      const act = getActiveAction();
      if (state.currentFrame >= act.frame_count) state.currentFrame = 0;
    }
    if (switchMode) {
      state.mode = switchMode;
    }
    renderAll();
    if (state.playing) scheduleNextTick();
  }

  function setActionStatus(key, newStatus) {
    if (!VALID_STATUSES.includes(newStatus) || !state.reviews[key]) return;
    const rec = state.reviews[key];
    rec.status = newStatus;
    rec.updated_at = new Date().toISOString();
    rec.invalidated = false;
    rec.invalidated_reason = null;
    persistDraft();
    renderProgress();
    renderIndex();
    renderInspector();
    if (state.mode === "side-by-side") renderSideBySide();
  }

  function setActionComment(key, text) {
    if (!state.reviews[key]) return;
    state.reviews[key].comment = text;
    state.reviews[key].updated_at = new Date().toISOString();
    persistDraft();
    renderDecisionMeta();
  }

  function bgClassName() {
    return state.bg === "dark" ? "bg-dark" : state.bg === "checker" ? "bg-checker" : "bg-light";
  }

  function updateTransportUI() {
    const btn = document.getElementById("btnPlayPause");
    btn.textContent = state.playing ? "暂停" : "播放";
    document.getElementById("chkLoop").checked = state.loop;
    document.getElementById("chkPixelated").checked = state.pixelated;
    document.getElementById("chkGuides").checked = state.guides;

    for (const b of document.querySelectorAll("#bgSwitchGroup [data-bg]")) {
      b.classList.toggle("active", b.dataset.bg === state.bg);
    }
    for (const b of document.querySelectorAll("#zoomSwitchGroup [data-zoom]")) {
      b.classList.toggle("active", Number(b.dataset.zoom) === state.zoom);
    }
    for (const b of document.querySelectorAll(".mode-tabs [data-mode]")) {
      b.classList.toggle("active", b.dataset.mode === state.mode);
    }
  }

  function renderProgress() {
    const s = computeSummary();
    document.getElementById("cntAcceptedActions").textContent = s.actions_by_status.ACCEPTED;
    document.getElementById("cntAcceptedFrames").textContent = s.frames_by_status.ACCEPTED;
    document.getElementById("cntNeedsFixActions").textContent = s.actions_by_status.NEEDS_FIX;
    document.getElementById("cntRejectedActions").textContent = s.actions_by_status.REJECTED;
    document.getElementById("cntPendingActions").textContent = s.actions_by_status.PENDING;
    document.getElementById("cntPendingFrames").textContent = s.frames_by_status.PENDING;

    const invChip = document.getElementById("statInvalidChip");
    if (s.invalidated_actions > 0) {
      invChip.classList.remove("hidden");
      document.getElementById("cntInvalidActions").textContent = s.invalidated_actions;
    } else {
      invChip.classList.add("hidden");
    }

    const tot = s.total_frames || 171;
    document.getElementById("pbAccepted").style.width = ((s.frames_by_status.ACCEPTED / tot) * 100).toFixed(2) + "%";
    document.getElementById("pbNeedsFix").style.width = ((s.frames_by_status.NEEDS_FIX / tot) * 100).toFixed(2) + "%";
    document.getElementById("pbRejected").style.width = ((s.frames_by_status.REJECTED / tot) * 100).toFixed(2) + "%";
  }

  function renderIndex() {
    const container = document.getElementById("actionIndex");
    container.innerHTML = "";

    for (const rowSpec of DATA.rows) {
      const acts = getStateActions(rowSpec.state);
      const visibleActs = acts.filter((act) => {
        const rec = state.reviews[act.key];
        if (state.filterForm !== "ALL" && act.id !== state.filterForm) return false;
        if (state.filterStatus === "QA_WATCH") return Boolean(act.qa_attention);
        if (state.filterStatus !== "ALL" && rec.status !== state.filterStatus) return false;
        return true;
      });
      if (visibleActs.length === 0) continue;

      const group = document.createElement("div");
      group.className = "row-group";

      const head = document.createElement("div");
      head.className = "row-group-head";
      head.innerHTML = `<span class="row-group-title">Row ${rowSpec.row} · ${rowSpec.state} (${rowSpec.expected_frames}f)</span>`;
      const syncBtn = document.createElement("button");
      syncBtn.type = "button";
      syncBtn.className = "row-sync-btn";
      syncBtn.textContent = "三形态并排";
      syncBtn.addEventListener("click", () => {
        selectAction(state.activeForm, rowSpec.state, "side-by-side");
      });
      head.appendChild(syncBtn);
      group.appendChild(head);

      const pills = document.createElement("div");
      pills.className = "form-pills";
      for (const act of acts) {
        const rec = state.reviews[act.key];
        const isMatched = visibleActs.includes(act);
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "form-pill" + (act.id === state.activeForm && act.state === state.activeState ? " selected" : "");
        btn.dataset.actionKey = act.key;
        if (!isMatched) btn.style.opacity = "0.28";

        const formMeta = formById.get(act.id);
        const dotClass = rec.invalidated ? "dot-INVALID" : `dot-${rec.status}`;
        const shortStatus = rec.invalidated
          ? "已失效"
          : rec.status === "ACCEPTED"
            ? "已通过"
            : rec.status === "NEEDS_FIX"
              ? "需修复"
              : rec.status === "REJECTED"
                ? "拒收"
                : "待审";
        btn.innerHTML = `
          <span class="form-pill-top">
            <span class="status-dot ${dotClass}"></span>
            <span>${formMeta.short_label}</span>
          </span>
          <span class="mono-dim">${shortStatus}</span>
          ${act.qa_attention ? '<span class="qa-flag" title="QA重点复核">QA!</span>' : ""}
        `;
        btn.addEventListener("click", () => selectAction(act.id, act.state));
        pills.appendChild(btn);
      }
      group.appendChild(pills);
      container.appendChild(group);
    }
  }

  function renderTimingBar() {
    const act = getActiveAction();
    const rec = state.reviews[act.key];
    const formMeta = formById.get(act.id);
    const frameObj = act.frames[state.currentFrame];
    const totalMs = act.durations_ms.reduce((a, b) => a + b, 0);

    document.getElementById("currentTitle").textContent =
      `Row ${act.row} · ${formMeta.label} (${act.id}) / ${act.state}`;
    const badge = document.getElementById("currentStatusBadge");
    badge.textContent = rec.status;
    badge.className = `badge badge-${rec.status}`;

    document.getElementById("currentQaWatchBadge").classList.toggle("hidden", !act.qa_attention);
    document.getElementById("currentInvalidBadge").classList.toggle("hidden", !rec.invalidated);

    document.getElementById("frameCounter").textContent = `Frame ${state.currentFrame + 1} / ${act.frame_count}`;
    document.getElementById("frameDurationLabel").textContent = `严格冻结时序: ${frameObj.duration_ms} ms`;
    document.getElementById("cycleTotalLabel").textContent = `循环总长: ${totalMs} ms`;
  }

  function renderDecisionMeta() {
    const act = getActiveAction();
    const rec = state.reviews[act.key];
    document.getElementById("decisionMeta").textContent =
      `上次更新时间：${rec.updated_at ? rec.updated_at : "基线初始值"} · 绑定哈希：${act.action_asset_hash.slice(0, 16)}...`;
  }

  function renderInspector() {
    const act = getActiveAction();
    const rec = state.reviews[act.key];

    document.getElementById("inspectorActionKey").textContent = act.key;

    const invEl = document.getElementById("invalidationAlert");
    if (rec.invalidated) {
      invEl.classList.remove("hidden");
      invEl.innerHTML = `<strong>旧版验收已自动失效：</strong>${rec.invalidated_reason}<br/>旧状态 <code>${rec.stale_previous_status || "UNKNOWN"}</code>（旧哈希 <code>${rec.stale_previous_asset_hash || "N/A"}</code>）已自动回退为 <code>PENDING</code>，请基于当前资产重新人工判定。`;
    } else {
      invEl.classList.add("hidden");
    }

    const lockEl = document.getElementById("lockedPreapprovedNotice");
    if (act.locked_preapproved) {
      lockEl.classList.remove("hidden");
      lockEl.innerHTML =
        "<strong>已明确人工验收基线（8 帧）：</strong>此动作（黑服 FIX-BLACK 新版 <code>running-right</code>）已由用户明确人工验收通过，工程规则禁止重做。";
    } else {
      lockEl.classList.add("hidden");
    }

    const qaEl = document.getElementById("qaWatchNotice");
    if (act.qa_attention) {
      qaEl.classList.remove("hidden");
      qaEl.innerHTML = `<strong>离线 QA 重点复核提示：</strong>${act.qa_attention_note || act.agy_visual_notes}`;
    } else {
      qaEl.classList.add("hidden");
    }

    for (const btn of document.querySelectorAll("#decisionStatusGroup [data-set-status]")) {
      btn.classList.toggle("active", btn.dataset.setStatus === rec.status);
    }

    const commentBox = document.getElementById("reviewerComment");
    if (commentBox.value !== rec.comment) {
      commentBox.value = rec.comment;
    }
    renderDecisionMeta();

    // Asset binding metadata
    const kv = document.getElementById("assetBindingMeta");
    kv.innerHTML = `
      <dt>候选版本</dt><dd>${act.selected_version} (${act.origin_phase})</dd>
      <dt>产出方</dt><dd>${act.produced_by}</dd>
      <dt>离线结构 QA</dt><dd>${act.structure_qa}（不代表人工验收）</dd>
      <dt>冻结帧时序</dt><dd>[${act.durations_ms.join(", ")}] ms</dd>
      <dt>动作绑定哈希</dt><dd>${act.action_asset_hash}</dd>
      <dt>原始条带哈希</dt><dd>${act.source_sha256}</dd>
      <dt>QA 视觉记录</dt><dd>${act.agy_visual_notes || "—"}</dd>
    `;

    document.getElementById("hashFrameCount").textContent = act.frame_count;
    const hashList = document.getElementById("frameHashList");
    hashList.innerHTML = act.frames
      .map(
        (f) =>
          `<div class="hash-item">F${f.index} (${f.duration_ms}ms) · ${f.repo_path}<br/>SHA-256: ${f.sha256}</div>`
      )
      .join("");
  }

  function renderSingleView() {
    const act = getActiveAction();
    const frameObj = act.frames[state.currentFrame];

    const viewport = document.getElementById("singleStageViewport");
    viewport.className = `stage-viewport ${bgClassName()}`;

    const stage = document.getElementById("singleSpriteStage");
    stage.className = `sprite-stage zoom-${state.zoom}` + (state.pixelated ? " pixelated" : "");

    const img = document.getElementById("singleFrameImg");
    if (img.getAttribute("src") !== frameObj.src) {
      img.setAttribute("src", frameObj.src);
    }
    document.getElementById("singleGuideOverlay").classList.toggle("hidden", !state.guides);
    document.getElementById("singleFrameSha").textContent = `F${frameObj.index} SHA-256: ${frameObj.sha256}`;

    // Frame strip
    const strip = document.getElementById("singleFrameStrip");
    if (strip.dataset.renderedKey !== act.key || strip.dataset.renderedBg !== state.bg) {
      strip.dataset.renderedKey = act.key;
      strip.dataset.renderedBg = state.bg;
      strip.innerHTML = "";
      act.frames.forEach((f, idx) => {
        const card = document.createElement("button");
        card.type = "button";
        card.className = "frame-thumb" + (idx === state.currentFrame ? " active" : "");
        card.dataset.frameIdx = String(idx);
        card.innerHTML = `
          <div class="frame-thumb-box ${bgClassName()}">
            <img src="${f.src}" alt="F${idx}" />
          </div>
          <span class="frame-thumb-meta">F${idx} · ${f.duration_ms}ms</span>
        `;
        card.addEventListener("click", () => {
          setPlaying(false);
          state.currentFrame = idx;
          renderFrameViews();
        });
        strip.appendChild(card);
      });
    } else {
      for (const el of strip.querySelectorAll(".frame-thumb")) {
        el.classList.toggle("active", Number(el.dataset.frameIdx) === state.currentFrame);
      }
    }
  }

  function renderSideBySide() {
    const acts = getStateActions(state.activeState);
    const refAct = acts[0];
    document.getElementById("sbsStateName").textContent = `Row ${refAct.row} · ${refAct.state} (${refAct.frame_count} 帧)`;
    document.getElementById("sbsTimingsText").textContent = `[${refAct.durations_ms.join(", ")}] ms`;

    // State selector pills
    const pillsEl = document.getElementById("sbsStatePills");
    if (pillsEl.childElementCount === 0) {
      for (const r of DATA.rows) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "chip";
        b.dataset.sbsState = r.state;
        b.textContent = `${r.row}:${r.state}`;
        b.addEventListener("click", () => selectAction(state.activeForm, r.state, "side-by-side"));
        pillsEl.appendChild(b);
      }
    }
    for (const b of pillsEl.querySelectorAll("[data-sbs-state]")) {
      b.classList.toggle("active", b.dataset.sbsState === state.activeState);
    }

    const grid = document.getElementById("sbsGrid");
    grid.innerHTML = "";
    const sbsZoom = state.zoom === 4 ? 2 : state.zoom; // keep 3 columns ergonomic, allow full 4x in single view

    for (const act of acts) {
      const formMeta = formById.get(act.id);
      const rec = state.reviews[act.key];
      const frameObj = act.frames[state.currentFrame % act.frame_count];

      const card = document.createElement("div");
      card.className = "sbs-card";
      card.dataset.sbsForm = act.id;
      card.innerHTML = `
        <div class="card-title">
          <h3>${formMeta.label} <span class="mono-dim">(${act.id})</span></h3>
          <span class="badge badge-${rec.status}">${rec.status}</span>
        </div>
        <div class="sbs-stage-box ${bgClassName()}">
          <div class="sprite-stage zoom-${sbsZoom}${state.pixelated ? " pixelated" : ""}">
            <img src="${frameObj.src}" alt="${act.key} F${frameObj.index}" data-sbs-img="${act.id}" />
            <div class="guide-overlay ${state.guides ? "" : "hidden"}">
              <div class="guide-line-x"></div>
              <div class="guide-line-y"></div>
              <div class="guide-anchor-dot"></div>
            </div>
          </div>
        </div>
        <div class="mono-dim">版本: ${act.selected_version} · 哈希: ${act.action_asset_hash.slice(0, 12)}</div>
        ${act.qa_attention ? `<div class="alert alert-warn" style="margin:0;padding:6px 8px;">QA关注: ${act.qa_attention_note}</div>` : ""}
      `;

      const quickBar = document.createElement("div");
      quickBar.className = "sbs-quick-bar";
      for (const st of VALID_STATUSES) {
        const sb = document.createElement("button");
        sb.type = "button";
        sb.className = "chip" + (rec.status === st ? " active" : "");
        sb.textContent = st;
        sb.addEventListener("click", () => setActionStatus(act.key, st));
        quickBar.appendChild(sb);
      }
      const openSingle = document.createElement("button");
      openSingle.type = "button";
      openSingle.className = "btn btn-xs btn-secondary";
      openSingle.textContent = "进入精审";
      openSingle.addEventListener("click", () => selectAction(act.id, act.state, "single"));
      quickBar.appendChild(openSingle);

      card.appendChild(quickBar);
      grid.appendChild(card);
    }
  }

  function updateSideBySideImagesOnly() {
    const acts = getStateActions(state.activeState);
    for (const act of acts) {
      const img = document.querySelector(`[data-sbs-img="${act.id}"]`);
      if (img) {
        const frameObj = act.frames[state.currentFrame % act.frame_count];
        img.setAttribute("src", frameObj.src);
      }
    }
  }

  function renderCompareView() {
    const act = getActiveAction();
    const formMeta = formById.get(act.id);
    const frameObj = act.frames[state.currentFrame];
    const container = document.getElementById("compareContent");
    container.innerHTML = "";

    // 1. Historical Rejected vs Current Candidate comparison (if present for this action)
    if (act.historical_comparison) {
      const hc = act.historical_comparison;
      const section = document.createElement("div");
      section.className = "card";
      section.innerHTML = `
        <div class="card-title">
          <h3>历史拒收候选 vs 当前候选：${formMeta.label} / ${act.state}</h3>
          <span class="badge badge-REJECTED">历史版本已排除，严禁入集</span>
        </div>
        <p class="dim">${hc.reason}</p>
      `;

      const pair = document.createElement("div");
      pair.className = "compare-pair";

      if (hc.type === "animated-frames") {
        const oldFrame = hc.old_frames[state.currentFrame % hc.old_frames.length];
        pair.innerHTML = `
          <div class="compare-box">
            <div class="card-title">
              <h3>旧版（已拒收）· ${hc.old_version}</h3>
              <span class="badge badge-REJECTED">REJECTED</span>
            </div>
            <div class="sbs-stage-box ${bgClassName()}">
              <div class="sprite-stage zoom-${Math.min(state.zoom, 2)}${state.pixelated ? " pixelated" : ""}">
                <img src="${oldFrame.src}" alt="Old rejected frame" data-compare-old-img="1" />
              </div>
            </div>
            <div class="mono-dim" style="margin-top:8px;">原条带 SHA-256: ${hc.old_source_sha256}</div>
          </div>
          <div class="compare-box">
            <div class="card-title">
              <h3>新版（当前采用）· ${act.selected_version}</h3>
              <span class="badge badge-${state.reviews[act.key].status}">${state.reviews[act.key].status}</span>
            </div>
            <div class="sbs-stage-box ${bgClassName()}">
              <div class="sprite-stage zoom-${Math.min(state.zoom, 2)}${state.pixelated ? " pixelated" : ""}">
                <img src="${frameObj.src}" alt="New current frame" data-compare-new-img="1" />
              </div>
            </div>
            <div class="mono-dim" style="margin-top:8px;">原条带 SHA-256: ${act.source_sha256}</div>
          </div>
        `;
      } else if (hc.type === "source-strips") {
        pair.innerHTML = `
          <div class="compare-box">
            <div class="card-title">
              <h3>旧版原条带（已拒收）· ${hc.old_version}</h3>
              <span class="badge badge-REJECTED">REJECTED_NATIVE_ALPHA</span>
            </div>
            <div class="sbs-stage-box ${bgClassName()}" style="min-height:180px;">
              <img class="strip-img" src="${hc.old_strip_src}" alt="Rejected attempt-01 strip" />
            </div>
            <div class="mono-dim" style="margin-top:8px;">SHA-256: ${hc.old_source_sha256}</div>
          </div>
          <div class="compare-box">
            <div class="card-title">
              <h3>新版修复原条带 · ${act.selected_version}</h3>
              <span class="badge badge-${state.reviews[act.key].status}">${state.reviews[act.key].status}</span>
            </div>
            <div class="sbs-stage-box ${bgClassName()}" style="min-height:180px;">
              <img class="strip-img" src="${hc.new_strip_src}" alt="Fixed attempt-02 strip" />
            </div>
            <div class="mono-dim" style="margin-top:8px;">SHA-256: ${act.source_sha256}</div>
          </div>
        `;
      }
      section.appendChild(pair);
      container.appendChild(section);
    }

    // 2. Current Active Action vs Locked P3/P3-FIX Master comparison (available for ALL 27 actions)
    const masterSection = document.createElement("div");
    masterSection.className = "card";
    masterSection.innerHTML = `
      <div class="card-title">
        <h3>当前动作帧 vs 已锁定 P3 / P3-FIX 派生母版：${formMeta.label} / ${act.state}</h3>
        <span class="mono-dim">母版 SHA-256: ${formMeta.master_sha256.slice(0, 16)}...</span>
      </div>
      <div class="compare-pair">
        <div class="compare-box">
          <div class="card-title">
            <h3>锁定派生母版（${formMeta.master_label}）</h3>
            <span class="badge badge-ACCEPTED">LOCKED MASTER</span>
          </div>
          <div class="sbs-stage-box ${bgClassName()}">
            <img class="compare-master-img" src="${formMeta.master_src}" alt="Locked master" />
          </div>
        </div>
        <div class="compare-box">
          <div class="card-title">
            <h3>当前动态候选（${act.selected_version} · F${frameObj.index}）</h3>
            <span class="badge badge-${state.reviews[act.key].status}">${state.reviews[act.key].status}</span>
          </div>
          <div class="sbs-stage-box ${bgClassName()}">
            <div class="sprite-stage zoom-${Math.min(state.zoom, 2)}${state.pixelated ? " pixelated" : ""}">
              <img src="${frameObj.src}" alt="Current action frame" data-compare-master-live="1" />
            </div>
          </div>
        </div>
      </div>
    `;
    container.appendChild(masterSection);
  }

  function updateCompareLiveImagesOnly() {
    const act = getActiveAction();
    const frameObj = act.frames[state.currentFrame];
    const liveImg = document.querySelector('[data-compare-master-live="1"]');
    if (liveImg) liveImg.setAttribute("src", frameObj.src);
    const newImg = document.querySelector('[data-compare-new-img="1"]');
    if (newImg) newImg.setAttribute("src", frameObj.src);
    if (act.historical_comparison && act.historical_comparison.type === "animated-frames") {
      const oldImg = document.querySelector('[data-compare-old-img="1"]');
      if (oldImg) {
        const oldFrames = act.historical_comparison.old_frames;
        oldImg.setAttribute("src", oldFrames[state.currentFrame % oldFrames.length].src);
      }
    }
  }

  function renderDetailsView() {
    const act = getActiveAction();
    const frameObj = act.frames[state.currentFrame];

    document.getElementById("loupeSourceWrap").className = `loupe-source-wrap ${bgClassName()}`;
    document.getElementById("loupeZoomWrap").className = `loupe-zoom-wrap ${bgClassName()}`;

    for (const b of document.querySelectorAll("#loupeZoomGroup [data-loupe]")) {
      b.classList.toggle("active", Number(b.dataset.loupe) === state.loupeZoom);
    }

    // Draw interactive source + magnified crop canvas
    getLoadedImage(frameObj.src, (img) => {
      const srcCanvas = document.getElementById("loupeSourceCanvas");
      const sctx = srcCanvas.getContext("2d");
      sctx.clearRect(0, 0, srcCanvas.width, srcCanvas.height);
      sctx.imageSmoothingEnabled = false;
      sctx.drawImage(img, 0, 0, 192, 208, 0, 0, 384, 416);

      const boxSize = Math.round(384 / state.loupeZoom);
      const sx = Math.max(0, Math.min(192 - boxSize, Math.round(state.loupeCenter.x - boxSize / 2)));
      const sy = Math.max(0, Math.min(208 - boxSize, Math.round(state.loupeCenter.y - boxSize / 2)));

      // Draw focus rectangle on source preview (2x scale)
      sctx.strokeStyle = "#ef4444";
      sctx.lineWidth = 2;
      sctx.strokeRect(sx * 2, sy * 2, boxSize * 2, boxSize * 2);

      // Draw zoomed loupe
      const zCanvas = document.getElementById("loupeZoomCanvas");
      const zctx = zCanvas.getContext("2d");
      zctx.clearRect(0, 0, zCanvas.width, zCanvas.height);
      zctx.imageSmoothingEnabled = false;
      zctx.drawImage(img, sx, sy, boxSize, boxSize, 0, 0, 384, 384);

      document.getElementById("loupeCoordLabel").textContent =
        `${act.id}/${act.state} F${frameObj.index} · 中心 (${state.loupeCenter.x}, ${state.loupeCenter.y}) · ${state.loupeZoom}×`;
    });

    // Marking QA sheet
    const sheet = DATA.marking_sheets[state.markingSheet];
    for (const b of document.querySelectorAll("#markingSheetTabs [data-marking]")) {
      b.classList.toggle("active", b.dataset.marking === state.markingSheet);
    }
    const imgEl = document.getElementById("markingSheetImg");
    if (imgEl.getAttribute("src") !== sheet.src) {
      imgEl.setAttribute("src", sheet.src);
    }
    document.getElementById("markingSheetMeta").textContent =
      `${sheet.title} · 文件: ${sheet.repo_path} · SHA-256: ${sheet.sha256}`;
  }

  function renderFrameViews() {
    renderTimingBar();
    if (state.mode === "single") {
      renderSingleView();
    } else if (state.mode === "side-by-side") {
      updateSideBySideImagesOnly();
    } else if (state.mode === "compare") {
      updateCompareLiveImagesOnly();
    } else if (state.mode === "details") {
      renderDetailsView();
    }
  }

  function renderAll() {
    updateTransportUI();
    renderProgress();
    renderIndex();
    renderTimingBar();

    document.getElementById("viewSingle").classList.toggle("hidden", state.mode !== "single");
    document.getElementById("viewSideBySide").classList.toggle("hidden", state.mode !== "side-by-side");
    document.getElementById("viewCompare").classList.toggle("hidden", state.mode !== "compare");
    document.getElementById("viewDetails").classList.toggle("hidden", state.mode !== "details");

    if (state.mode === "single") {
      renderSingleView();
      renderInspector();
    } else if (state.mode === "side-by-side") {
      renderSideBySide();
    } else if (state.mode === "compare") {
      renderCompareView();
    } else if (state.mode === "details") {
      renderDetailsView();
    }
  }

  function downloadFile(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  // Wire up events
  function bindEvents() {
    document.getElementById("metaSubtitle").textContent =
      `基线 Commit: ${DATA.baseline_commit.slice(0, 12)} · 资产指纹: ${DATA.manifest_fingerprint.slice(0, 16)} · 27 动作 / 171 帧 (${DATA.bundle_mode})`;

    // Mode tabs
    for (const btn of document.querySelectorAll(".mode-tabs [data-mode]")) {
      btn.addEventListener("click", () => {
        state.mode = btn.dataset.mode;
        renderAll();
      });
    }

    // Filters
    for (const btn of document.querySelectorAll("#statusFilterGroup [data-filter-status]")) {
      btn.addEventListener("click", () => {
        state.filterStatus = btn.dataset.filterStatus;
        for (const b of document.querySelectorAll("#statusFilterGroup [data-filter-status]")) {
          b.classList.toggle("active", b === btn);
        }
        renderIndex();
      });
    }
    for (const btn of document.querySelectorAll("#formFilterGroup [data-filter-form]")) {
      btn.addEventListener("click", () => {
        state.filterForm = btn.dataset.filterForm;
        for (const b of document.querySelectorAll("#formFilterGroup [data-filter-form]")) {
          b.classList.toggle("active", b === btn);
        }
        renderIndex();
      });
    }

    // Playback & view controls
    document.getElementById("btnPlayPause").addEventListener("click", () => setPlaying(!state.playing));
    document.getElementById("btnPrevFrame").addEventListener("click", () => stepFrame(-1));
    document.getElementById("btnNextFrame").addEventListener("click", () => stepFrame(1));
    document.getElementById("chkLoop").addEventListener("change", (e) => {
      state.loop = e.target.checked;
    });
    document.getElementById("chkPixelated").addEventListener("change", (e) => {
      state.pixelated = e.target.checked;
      renderAll();
    });
    document.getElementById("chkGuides").addEventListener("change", (e) => {
      state.guides = e.target.checked;
      renderAll();
    });

    for (const btn of document.querySelectorAll("#bgSwitchGroup [data-bg]")) {
      btn.addEventListener("click", () => {
        state.bg = btn.dataset.bg;
        renderAll();
      });
    }
    for (const btn of document.querySelectorAll("#zoomSwitchGroup [data-zoom]")) {
      btn.addEventListener("click", () => {
        state.zoom = Number(btn.dataset.zoom);
        renderAll();
      });
    }

    // Decision status buttons
    for (const btn of document.querySelectorAll("#decisionStatusGroup [data-set-status]")) {
      btn.addEventListener("click", () => {
        const act = getActiveAction();
        setActionStatus(act.key, btn.dataset.setStatus);
      });
    }

    // Quick comment tags
    for (const btn of document.querySelectorAll(".quick-tags [data-tag]")) {
      btn.addEventListener("click", () => {
        const act = getActiveAction();
        const box = document.getElementById("reviewerComment");
        const tag = btn.dataset.tag;
        const cur = box.value.trim();
        box.value = cur ? `${cur}；${tag}` : tag;
        setActionComment(act.key, box.value);
      });
    }

    document.getElementById("reviewerComment").addEventListener("input", (e) => {
      const act = getActiveAction();
      setActionComment(act.key, e.target.value);
    });

    document.getElementById("btnCopyActionHash").addEventListener("click", () => {
      const act = getActiveAction();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(act.action_asset_hash).then(() => showToast("已复制动作绑定 SHA-256"));
      } else {
        showToast("SHA-256: " + act.action_asset_hash);
      }
    });

    // Compare shortcuts
    for (const btn of document.querySelectorAll("[data-jump-compare]")) {
      btn.addEventListener("click", () => {
        const [f, s] = btn.dataset.jumpCompare.split("::");
        selectAction(f, s, "compare");
      });
    }

    // Loupe controls
    for (const btn of document.querySelectorAll("#loupeZoomGroup [data-loupe]")) {
      btn.addEventListener("click", () => {
        state.loupeZoom = Number(btn.dataset.loupe);
        renderDetailsView();
      });
    }
    for (const btn of document.querySelectorAll("#loupePresetRow [data-focus]")) {
      btn.addEventListener("click", () => {
        const p = LOUPE_PRESETS[btn.dataset.focus];
        if (!p) return;
        state.loupeCenter = { x: p.x, y: p.y };
        for (const b of document.querySelectorAll("#loupePresetRow [data-focus]")) {
          b.classList.toggle("active", b === btn);
        }
        renderDetailsView();
      });
    }
    const srcCanvas = document.getElementById("loupeSourceCanvas");
    let dragging = false;
    function updateLoupeFromEvent(ev) {
      const rect = srcCanvas.getBoundingClientRect();
      const x = Math.round(((ev.clientX - rect.left) / rect.width) * 192);
      const y = Math.round(((ev.clientY - rect.top) / rect.height) * 208);
      state.loupeCenter = { x: Math.max(0, Math.min(191, x)), y: Math.max(0, Math.min(207, y)) };
      renderDetailsView();
    }
    srcCanvas.addEventListener("pointerdown", (ev) => {
      dragging = true;
      updateLoupeFromEvent(ev);
    });
    window.addEventListener("pointerup", () => {
      dragging = false;
    });
    srcCanvas.addEventListener("pointermove", (ev) => {
      if (dragging) updateLoupeFromEvent(ev);
    });

    for (const btn of document.querySelectorAll("#markingSheetTabs [data-marking]")) {
      btn.addEventListener("click", () => {
        state.markingSheet = btn.dataset.marking;
        renderDetailsView();
      });
    }

    // Import / Export / Markdown / Reset
    document.getElementById("btnExportJson").addEventListener("click", () => {
      const payload = buildExportPayload();
      const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
      downloadFile(`rei-art-review-${stamp}.json`, JSON.stringify(payload, null, 2) + "\n", "application/json;charset=utf-8");
      showToast("已导出人工验收 JSON 记录");
    });

    document.getElementById("importJsonInput").addEventListener("change", (e) => {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const parsed = JSON.parse(String(reader.result));
          applyImportedPayload(parsed, file.name);
        } catch (err) {
          showToast("导入失败：" + err.message);
        } finally {
          e.target.value = "";
        }
      };
      reader.readAsText(file, "utf-8");
    });

    document.getElementById("btnShowMarkdown").addEventListener("click", () => {
      document.getElementById("markdownOutput").value = buildMarkdownSummary();
      document.getElementById("markdownModal").classList.remove("hidden");
    });
    document.getElementById("btnCloseMarkdown").addEventListener("click", () => {
      document.getElementById("markdownModal").classList.add("hidden");
    });
    document.getElementById("btnCopyMarkdown").addEventListener("click", () => {
      const text = document.getElementById("markdownOutput").value;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => showToast("已复制 Markdown 摘要"));
      }
    });
    document.getElementById("btnDownloadMarkdown").addEventListener("click", () => {
      const text = document.getElementById("markdownOutput").value;
      const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
      downloadFile(`REI_ART_REVIEW_SUMMARY_${stamp}.md`, text, "text/markdown;charset=utf-8");
    });

    document.getElementById("btnResetBaseline").addEventListener("click", () => {
      state.reviews = buildBaselineReviews();
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (_) {}
      renderAll();
      showToast("已恢复归档的人工验收基线");
    });

    // Keyboard shortcuts
    window.addEventListener("keydown", (e) => {
      if (e.target && (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT")) return;
      if (e.code === "Space") {
        e.preventDefault();
        setPlaying(!state.playing);
      } else if (e.code === "ArrowLeft") {
        e.preventDefault();
        stepFrame(-1);
      } else if (e.code === "ArrowRight") {
        e.preventDefault();
        stepFrame(1);
      } else if (e.key === "1" || e.key === "2" || e.key === "4") {
        state.zoom = Number(e.key);
        renderAll();
      } else if (e.key === "l" || e.key === "L") {
        state.bg = state.bg === "light" ? "dark" : "light";
        renderAll();
      }
    });
  }

  // Expose deterministic test/automation hooks for T5 Playwright verification
  window.__REI_REVIEW_API__ = {
    getState: () => ({
      mode: state.mode,
      activeForm: state.activeForm,
      activeState: state.activeState,
      currentFrame: state.currentFrame,
      playing: state.playing,
      loop: state.loop,
      bg: state.bg,
      zoom: state.zoom,
      lastScheduledDurationMs: state.lastScheduledDurationMs,
      summary: computeSummary(),
    }),
    getData: () => DATA,
    selectAction,
    setPlaying,
    stepFrame,
    setActionStatus,
    setActionComment,
    exportPayload: buildExportPayload,
    importPayload: (payload, label = "API") => applyImportedPayload(payload, label),
    generateMarkdown: buildMarkdownSummary,
    resetBaseline: () => {
      state.reviews = buildBaselineReviews();
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (_) {}
      renderAll();
    },
  };

  // Boot
  bindEvents();
  loadInitialReviews();
  renderAll();
  scheduleNextTick();
})();
