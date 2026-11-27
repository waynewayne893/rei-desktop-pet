window.REI_REVIEW_DATA = {
  "schema_version": 1,
  "project": "rei-desktop-pet",
  "tool": "Rei Review Center V1.0",
  "stage": "P4-B PARTIAL",
  "bundle_mode": "repo-relative",
  "baseline_commit": "b51100a162eaea16bd7237878d801733b623f4c4",
  "manifest_fingerprint": "56f30e4c5a5d6fa5b088e3b321fbb0d484f8ce4845f168c444b3958415248767",
  "total_actions": 27,
  "total_frames": 171,
  "forms": [
    {
      "id": "rei-school",
      "label": "校服绫波丽",
      "short_label": "校服",
      "master_label": "P3 派生 RGBA 母版",
      "master_repo_path": "02_标准化母版/rei-school/master-rgba.png",
      "master_sha256": "38b2db6fabc1daf5ad5b368152a12cc0a92a22a0abb12ce0dafcd588f61e8528",
      "master_src": "../../02_标准化母版/rei-school/master-rgba.png"
    },
    {
      "id": "rei-white",
      "label": "白色战斗服 (00)",
      "short_label": "白服",
      "master_label": "P3-FIX 透明修复母版",
      "master_repo_path": "02_标准化母版/P3-FIX/rei-white-master-rgba-p3-fix.png",
      "master_sha256": "92ff3c4d9c33534a58d4c54d0556bef7d98dfe49cea6804f9b29ec90ff174c5c",
      "master_src": "../../02_标准化母版/P3-FIX/rei-white-master-rgba-p3-fix.png"
    },
    {
      "id": "rei-black",
      "label": "黑色战斗服 (09)",
      "short_label": "黑服",
      "master_label": "P3 派生 RGBA 母版",
      "master_repo_path": "02_标准化母版/rei-black/master-rgba.png",
      "master_sha256": "a19715e0c2e4df83b206f30ee03d6044b0665c911ee85aa31899f118ecad81ce",
      "master_src": "../../02_标准化母版/rei-black/master-rgba.png"
    }
  ],
  "rows": [
    {
      "state": "idle",
      "row": 0,
      "expected_frames": 6,
      "durations_ms": [
        280,
        110,
        110,
        140,
        140,
        320
      ]
    },
    {
      "state": "running-right",
      "row": 1,
      "expected_frames": 8,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ]
    },
    {
      "state": "running-left",
      "row": 2,
      "expected_frames": 8,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ]
    },
    {
      "state": "waving",
      "row": 3,
      "expected_frames": 4,
      "durations_ms": [
        140,
        140,
        140,
        280
      ]
    },
    {
      "state": "jumping",
      "row": 4,
      "expected_frames": 5,
      "durations_ms": [
        140,
        140,
        140,
        140,
        280
      ]
    },
    {
      "state": "failed",
      "row": 5,
      "expected_frames": 8,
      "durations_ms": [
        140,
        140,
        140,
        140,
        140,
        140,
        140,
        240
      ]
    },
    {
      "state": "waiting",
      "row": 6,
      "expected_frames": 6,
      "durations_ms": [
        150,
        150,
        150,
        150,
        150,
        260
      ]
    },
    {
      "state": "running",
      "row": 7,
      "expected_frames": 6,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        220
      ]
    },
    {
      "state": "review",
      "row": 8,
      "expected_frames": 6,
      "durations_ms": [
        150,
        150,
        150,
        150,
        150,
        280
      ]
    }
  ],
  "marking_sheets": {
    "white": {
      "title": "白色战斗服 00 胸前标识高分专检拼图",
      "repo_path": "07_QA验收/P4-B/p4b-chest-markings-qa-white.png",
      "sha256": "a1f3053305c59823725e0f6f41405a2b4e2f2b6101f79b16ad168f06b9f0d6e5",
      "src": "../../07_QA验收/P4-B/p4b-chest-markings-qa-white.png"
    },
    "black": {
      "title": "黑色战斗服 09 胸前标识高分专检拼图",
      "repo_path": "07_QA验收/P4-B/p4b-chest-markings-qa-black.png",
      "sha256": "d22254e8e1fda1ecae3fe9ddd61e3312bd423455303f8b176c38e141cf7652a3",
      "src": "../../07_QA验收/P4-B/p4b-chest-markings-qa-black.png"
    }
  },
  "actions": [
    {
      "key": "rei-school::idle",
      "id": "rei-school",
      "state": "idle",
      "row": 0,
      "frame_count": 6,
      "durations_ms": [
        280,
        110,
        110,
        140,
        140,
        320
      ],
      "selected_version": "P4-A/attempt-01",
      "origin_phase": "P4-A",
      "produced_by": "Codex",
      "protected_p4a_baseline": true,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-A/originals/idle/attempt-01/source.png",
      "source_sha256": "376d787ff16f08c5d7f7dab27ea3440455c420931f4a497b581de59e83d73d85",
      "action_asset_hash": "6de56d6d21ef38f61e554853e0603095b588fc003b8d117ea180285429c19bb3",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "Protected P4-A baseline; hash-verified identical to REI_P4A_ASSET_MANIFEST_FIX_BLACK.json.",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-A/selected/idle/frames/00.png",
          "sha256": "1060459b3f468e8302fd40d6bb6b3892df95b4351695274c6a714353a722d1dc",
          "bytes": 18474,
          "duration_ms": 280,
          "src": "../../03_校服绫波丽/P4-A/selected/idle/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-A/selected/idle/frames/01.png",
          "sha256": "210a1e7955ea7ccb0c74e3d3c069ed3f4959815143f130ddf8cb18f5ebb1c300",
          "bytes": 18559,
          "duration_ms": 110,
          "src": "../../03_校服绫波丽/P4-A/selected/idle/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-A/selected/idle/frames/02.png",
          "sha256": "481874ee79839dabe2ebae19c55115f16ea4fb1b02df78c176d05717d8bb1416",
          "bytes": 18565,
          "duration_ms": 110,
          "src": "../../03_校服绫波丽/P4-A/selected/idle/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-A/selected/idle/frames/03.png",
          "sha256": "df966e8ee3f8e79be77bf38366206869ad43dee8c9ba62f53593e48e81627bd5",
          "bytes": 18461,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-A/selected/idle/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "03_校服绫波丽/P4-A/selected/idle/frames/04.png",
          "sha256": "0ed679baecc7b0d1870c4a57bd50bea333e7f8d3a3d3e6a20f0c16821ef1a0c3",
          "bytes": 18540,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-A/selected/idle/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "03_校服绫波丽/P4-A/selected/idle/frames/05.png",
          "sha256": "c9443243ef3bd80b4031e6cd324f369017c1e4988916ac373f93d66867d26af4",
          "bytes": 18515,
          "duration_ms": 320,
          "src": "../../03_校服绫波丽/P4-A/selected/idle/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::idle",
      "id": "rei-white",
      "state": "idle",
      "row": 0,
      "frame_count": 6,
      "durations_ms": [
        280,
        110,
        110,
        140,
        140,
        320
      ],
      "selected_version": "P4-A/attempt-02",
      "origin_phase": "P4-A-CONTINUE",
      "produced_by": "Codex",
      "protected_p4a_baseline": true,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-A/originals/idle/attempt-02/source.png",
      "source_sha256": "a21608225d4a405b63da386ad4b841a757e0e4a1705edfbb7d7d086ce5ad9287",
      "action_asset_hash": "7195ffd1469f22152d561ccfd2cb79d963e263bb889cf89d7c78a82e600d8f73",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "Protected P4-A baseline; hash-verified identical to REI_P4A_ASSET_MANIFEST_FIX_BLACK.json.",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-A/selected/idle/frames/00.png",
          "sha256": "8ae73126ca709d93ebd4e6d2cca519bbec0b06486905d1fe83117f4e29cd0137",
          "bytes": 21695,
          "duration_ms": 280,
          "src": "../../04_白色战斗服/P4-A/selected/idle/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-A/selected/idle/frames/01.png",
          "sha256": "40f4d81cfe3aa94b4f27b67bf6ff585b0523433385f9673c97929a5599d6b982",
          "bytes": 21483,
          "duration_ms": 110,
          "src": "../../04_白色战斗服/P4-A/selected/idle/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-A/selected/idle/frames/02.png",
          "sha256": "d9abfbe30f1b300f3802f76abf96f08774bdf0a9d798bfcfd59d4ffa0f8df104",
          "bytes": 21776,
          "duration_ms": 110,
          "src": "../../04_白色战斗服/P4-A/selected/idle/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-A/selected/idle/frames/03.png",
          "sha256": "473eb159adc1b95fa91c53b007fcaeaba540ab815371ae14fbaa246ccedb7729",
          "bytes": 21595,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-A/selected/idle/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "04_白色战斗服/P4-A/selected/idle/frames/04.png",
          "sha256": "ec86538bffb26271c40627ab36ca32d696d72b1833b73292017d61f5f3bbaaff",
          "bytes": 21434,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-A/selected/idle/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "04_白色战斗服/P4-A/selected/idle/frames/05.png",
          "sha256": "a08f798d4d16470cb73dda7c90699ab43e0eaba98e92ea96eb2955f738d3b13b",
          "bytes": 21220,
          "duration_ms": 320,
          "src": "../../04_白色战斗服/P4-A/selected/idle/frames/05.png"
        }
      ],
      "historical_comparison": {
        "type": "source-strips",
        "old_version": "P4-A/attempt-01 (透明背景缺陷拒收)",
        "old_source_sha256": "2327a2e1b1ea908d1e90f84ee89b2ccda22e5cb4f9c920241f8c165844183cd4",
        "old_strip_src": "../../04_白色战斗服/P4-A/originals/idle/attempt-01/source.png",
        "new_strip_src": "../../04_白色战斗服/P4-A/originals/idle/attempt-02/source.png",
        "reason": "白服 idle attempt-01 因原生透明通道缺陷被拒收，已由 attempt-02 原生真透明条带修复并锁定为 P4-A 受保护基线。"
      }
    },
    {
      "key": "rei-black::idle",
      "id": "rei-black",
      "state": "idle",
      "row": 0,
      "frame_count": 6,
      "durations_ms": [
        280,
        110,
        110,
        140,
        140,
        320
      ],
      "selected_version": "P4-A/attempt-01",
      "origin_phase": "P4-A",
      "produced_by": "Codex",
      "protected_p4a_baseline": true,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-A/originals/idle/attempt-01/source.png",
      "source_sha256": "0ce48630d0b4e366d45d9277d0369a494064e89139b0ca1c482f44a78be8d5ac",
      "action_asset_hash": "902176408e5a1b4e435a537dfa8a7265dc10c31c9e7f48a841d8e2b9e1125a85",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "Protected P4-A baseline; hash-verified identical to REI_P4A_ASSET_MANIFEST_FIX_BLACK.json.",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-A/selected/idle/frames/00.png",
          "sha256": "e46d9facdf2c6045eed6f031d3fcf8cfffbf434f1ad690a6118e5c5bb3d03455",
          "bytes": 17554,
          "duration_ms": 280,
          "src": "../../05_黑色战斗服/P4-A/selected/idle/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-A/selected/idle/frames/01.png",
          "sha256": "3cf61021ca7bcd0a6bca6405bb20b498d9ffe305b0a82ab4319fae8e83d19930",
          "bytes": 17470,
          "duration_ms": 110,
          "src": "../../05_黑色战斗服/P4-A/selected/idle/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-A/selected/idle/frames/02.png",
          "sha256": "09860803125df4c2eac34c64877d28cae98b4c2901a97da931e1e21d4bf09b28",
          "bytes": 17468,
          "duration_ms": 110,
          "src": "../../05_黑色战斗服/P4-A/selected/idle/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-A/selected/idle/frames/03.png",
          "sha256": "66c3a767068c6189efb42367a8ee50eb42b76e7aaca2e157fa739693b9cf696f",
          "bytes": 17542,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-A/selected/idle/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "05_黑色战斗服/P4-A/selected/idle/frames/04.png",
          "sha256": "fa6b66526b64a04f5789c7bb3c7976ee5bcc3560eec22f2368b351d818556c9c",
          "bytes": 17594,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-A/selected/idle/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "05_黑色战斗服/P4-A/selected/idle/frames/05.png",
          "sha256": "cc4cf523b941bf23a8240f2695d9a3ab41f2bf68b47da61620a40fb710ced371",
          "bytes": 17540,
          "duration_ms": 320,
          "src": "../../05_黑色战斗服/P4-A/selected/idle/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-school::running-right",
      "id": "rei-school",
      "state": "running-right",
      "row": 1,
      "frame_count": 8,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-A/attempt-01",
      "origin_phase": "P4-A",
      "produced_by": "Codex",
      "protected_p4a_baseline": true,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-A/originals/running-right/attempt-01/source.png",
      "source_sha256": "e9b7ce6efc3162931a9657be50724d0045e761d43a42b332462ebe08c18cba9f",
      "action_asset_hash": "44ad5ade40472d616e9605621b39442feb5ef0e67d4cd472ec11ec4b01a12b4f",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "Protected P4-A baseline; hash-verified identical to REI_P4A_ASSET_MANIFEST_FIX_BLACK.json.",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-A/selected/running-right/frames/00.png",
          "sha256": "4d6495559253a9cffcfc6b47676963fd497f2f026adad969124b01ebfeae3b00",
          "bytes": 18787,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-A/selected/running-right/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-A/selected/running-right/frames/01.png",
          "sha256": "feec8a714f98d079e49695800e3164d1964d12fd7cc49a24e311bdebf35b7e79",
          "bytes": 18643,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-A/selected/running-right/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-A/selected/running-right/frames/02.png",
          "sha256": "52edaddc6bbb56ee34c497a3ced4abe19817ddee23f8aa624f8ad5fb74b943cd",
          "bytes": 18280,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-A/selected/running-right/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-A/selected/running-right/frames/03.png",
          "sha256": "eece125185b95bc8ad4954dd9e1a201cf5d7b2c72b49dc96bbc33b1f93aebd02",
          "bytes": 18833,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-A/selected/running-right/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "03_校服绫波丽/P4-A/selected/running-right/frames/04.png",
          "sha256": "450bf1ca604e126b17d0a4dbff8273c17232190e050a7235e06abfada2150dc7",
          "bytes": 18333,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-A/selected/running-right/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "03_校服绫波丽/P4-A/selected/running-right/frames/05.png",
          "sha256": "2a74819e0d2b1c9c4b29d4b8e8f4906b23dc36165f431e3254b6d89450c2b5d6",
          "bytes": 18560,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-A/selected/running-right/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "03_校服绫波丽/P4-A/selected/running-right/frames/06.png",
          "sha256": "651e46cb86062cf8745b915eb9f3a970c4055e574a1cc96dff7b948ad31d7e30",
          "bytes": 17866,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-A/selected/running-right/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "03_校服绫波丽/P4-A/selected/running-right/frames/07.png",
          "sha256": "18ffade9aa9e008fbe409d861a98a9254a173f232c31808936c89745b0a627f2",
          "bytes": 18768,
          "duration_ms": 220,
          "src": "../../03_校服绫波丽/P4-A/selected/running-right/frames/07.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::running-right",
      "id": "rei-white",
      "state": "running-right",
      "row": 1,
      "frame_count": 8,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-A/attempt-01",
      "origin_phase": "P4-A-CONTINUE",
      "produced_by": "Codex",
      "protected_p4a_baseline": true,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-A/originals/running-right/attempt-01/source.png",
      "source_sha256": "73b7cb3747810ec7fc7f8f751b84a21fed86b8a479e174a106d1c37288dc57d9",
      "action_asset_hash": "d77884814b02217ea8301306133f69a588070b5bfb713bb5aede7d2d668e4e8a",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "Protected P4-A baseline; hash-verified identical to REI_P4A_ASSET_MANIFEST_FIX_BLACK.json.",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-A/selected/running-right/frames/00.png",
          "sha256": "863746c4f09ce762f21c86e0d31183da80466b79e41417496b7b4ef84bbfa816",
          "bytes": 19197,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-A/selected/running-right/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-A/selected/running-right/frames/01.png",
          "sha256": "6626a4efe1696683e6658bc1477b47c835da3301805247c69bf507d850e0d8d6",
          "bytes": 18757,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-A/selected/running-right/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-A/selected/running-right/frames/02.png",
          "sha256": "29520493b74cc96cfb28690e8c7b8aec5dd6162aa1019c9c6aa0dd6b8c6bb323",
          "bytes": 18351,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-A/selected/running-right/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-A/selected/running-right/frames/03.png",
          "sha256": "70a0372ea1dcb8d022f5592d57f4b87b10c0656cbd24220f281c2f1eb3ef8dc8",
          "bytes": 18844,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-A/selected/running-right/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "04_白色战斗服/P4-A/selected/running-right/frames/04.png",
          "sha256": "1e9f0395a93fe180b88255fb905ed6f5ca89df9ee8eeb26ff898dfdac27080cc",
          "bytes": 18246,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-A/selected/running-right/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "04_白色战斗服/P4-A/selected/running-right/frames/05.png",
          "sha256": "6b08100482181b07513626ee2fdc8656275362c295c9514578e58b63dec837d2",
          "bytes": 18765,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-A/selected/running-right/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "04_白色战斗服/P4-A/selected/running-right/frames/06.png",
          "sha256": "44a387c625ea483e22610e5a63be4348be58db5afe9cccfe8c0f41a69435c4a5",
          "bytes": 18404,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-A/selected/running-right/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "04_白色战斗服/P4-A/selected/running-right/frames/07.png",
          "sha256": "9140769f0eded3e3e92d6489a88c86c21f9e15da593d4b2fcd830eef540c42fd",
          "bytes": 19070,
          "duration_ms": 220,
          "src": "../../04_白色战斗服/P4-A/selected/running-right/frames/07.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-black::running-right",
      "id": "rei-black",
      "state": "running-right",
      "row": 1,
      "frame_count": 8,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-A/FIX-BLACK/attempt-01",
      "origin_phase": "P4-A-FIX-BLACK",
      "produced_by": "Codex",
      "protected_p4a_baseline": true,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-A/FIX-BLACK/originals/attempt-01/source.png",
      "source_sha256": "28f6579909d79599fd268c008ec85e33da3f4c4bad7e4e9fd52ae51bea6a5e1d",
      "action_asset_hash": "3546dc58a1460749a54d6c770a9c52202cc2db6a5b79e987acebdaaf7202f3aa",
      "initial_status": "ACCEPTED",
      "initial_comment": "用户已明确人工验收通过的 FIX-BLACK 新版黑服右跑（8 帧），禁止重做。",
      "initial_updated_at": "2026-11-27T00:00:00Z",
      "locked_preapproved": true,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "Protected P4-A baseline; hash-verified identical to REI_P4A_ASSET_MANIFEST_FIX_BLACK.json.",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/00.png",
          "sha256": "a1a69caac3d1459dac003979776b7e273862ba9968a7b74decd6a6ba67cd5d5d",
          "bytes": 17645,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/01.png",
          "sha256": "e2854f440f90c5cc45ba2352498f1efaef81fa0ba59c7257e364259cf47b982a",
          "bytes": 16784,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/02.png",
          "sha256": "85c2eeb9167a6a68229036fc9d670e773715b2f4f993e481f1d1a806e4b36123",
          "bytes": 16181,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/03.png",
          "sha256": "3d2e87e028f78acd8bdb887210feb23fe5c994f34f142b0dca90484e31ba4ac1",
          "bytes": 17104,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/04.png",
          "sha256": "d547604f40b9a195dd4f34acaa2d64dedad83868e1b47e0541e0ba72766578ed",
          "bytes": 15587,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/05.png",
          "sha256": "26ab5f2082f8b5aa7fe7380464776ddf01e207e74dc87317a8cc8af2fcbcdeed",
          "bytes": 17450,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/06.png",
          "sha256": "401280e3fcc2718f6796c3e6591c9ddc70bb0dfac75f9aef32c1bb94c4c0c690",
          "bytes": 16312,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/07.png",
          "sha256": "6ab05bdb72ee5e0a1e8b92ff57ec63e232a6459706bcae133fb3c3a3e34f86c6",
          "bytes": 17544,
          "duration_ms": 220,
          "src": "../../05_黑色战斗服/P4-A/FIX-BLACK/selected/running-right/frames/07.png"
        }
      ],
      "historical_comparison": {
        "type": "animated-frames",
        "old_version": "P4-A/attempt-01 (已拒收旧版)",
        "old_source_sha256": "11711472443a06c866a699046c3cb28f40a536558c2fb622ad683be0d945ea30",
        "reason": "用户人工验收拒收旧版黑服右跑，已由 FIX-BLACK 新版替代并人工验收通过（8 帧 ACCEPTED）；旧版原图与帧仅保留供新旧对照，严禁进入图集。",
        "old_frames": [
          {
            "index": 0,
            "repo_path": "05_黑色战斗服/P4-A/selected/running-right/frames/00.png",
            "sha256": "155d861b81b59253059834a3b32585dd662503f29432c342fea8902a8099924d",
            "src": "../../05_黑色战斗服/P4-A/selected/running-right/frames/00.png"
          },
          {
            "index": 1,
            "repo_path": "05_黑色战斗服/P4-A/selected/running-right/frames/01.png",
            "sha256": "59827a05dee9a7455a72bd917966d6998f51c5077e548c8c30514a315cddf54a",
            "src": "../../05_黑色战斗服/P4-A/selected/running-right/frames/01.png"
          },
          {
            "index": 2,
            "repo_path": "05_黑色战斗服/P4-A/selected/running-right/frames/02.png",
            "sha256": "ffdd01daeae428a88a103fdd3bbd0476a45a07f9ad6b9eda451cd3fa23dd9615",
            "src": "../../05_黑色战斗服/P4-A/selected/running-right/frames/02.png"
          },
          {
            "index": 3,
            "repo_path": "05_黑色战斗服/P4-A/selected/running-right/frames/03.png",
            "sha256": "62e59b72a02d7fa32ab7adbdf3024432de8d99a6ce8ce71d1529a930bf1f3e14",
            "src": "../../05_黑色战斗服/P4-A/selected/running-right/frames/03.png"
          },
          {
            "index": 4,
            "repo_path": "05_黑色战斗服/P4-A/selected/running-right/frames/04.png",
            "sha256": "6ab54abaa2a8ffd1fa7edc9e3fe01c14b849a4cd1eaa9d9f6ef8c5ba056db437",
            "src": "../../05_黑色战斗服/P4-A/selected/running-right/frames/04.png"
          },
          {
            "index": 5,
            "repo_path": "05_黑色战斗服/P4-A/selected/running-right/frames/05.png",
            "sha256": "f4f1036b2fe3b1bee4f7276117656052d90bdc059f67188971094c008c24bbaf",
            "src": "../../05_黑色战斗服/P4-A/selected/running-right/frames/05.png"
          },
          {
            "index": 6,
            "repo_path": "05_黑色战斗服/P4-A/selected/running-right/frames/06.png",
            "sha256": "73b1d0b6920a1af8c601efa34f71bce004e26294a4ede718c196aa31517ba8f9",
            "src": "../../05_黑色战斗服/P4-A/selected/running-right/frames/06.png"
          },
          {
            "index": 7,
            "repo_path": "05_黑色战斗服/P4-A/selected/running-right/frames/07.png",
            "sha256": "a4a629875790964f0fab78b44b89b7e26c42b20f450fd9af8bc5c9fecf401a7e",
            "src": "../../05_黑色战斗服/P4-A/selected/running-right/frames/07.png"
          }
        ]
      }
    },
    {
      "key": "rei-school::running-left",
      "id": "rei-school",
      "state": "running-left",
      "row": 2,
      "frame_count": 8,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-B/originals/running-left/attempt-01/source.png",
      "source_sha256": "1050c32767cf353b02e85c15844fdee82faad1f4cd83f107612178cd004c1582",
      "action_asset_hash": "7237238e5c8d2665eea94a7e45c9fff8d47744fc7f22e641d7a65eb23a641272",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "8/8 frames facing left, natural alternating stride and arm swing, skirt sway, white clips and red bow preserved, min_top=4px, clean alpha on dark and light.",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/00.png",
          "sha256": "ab4f0f7dfe77ecf3e59f7cb3d64cd9d9ce6464151e0f59dac05dd05f25630539",
          "bytes": 20022,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/01.png",
          "sha256": "fddc2daa67fece166f1852d226aa175c76870756208421a7fe93d330515d9bc5",
          "bytes": 19853,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/02.png",
          "sha256": "e8eef67f65fa9d01409a1d50cdc5560ada402e9fd1f727aad50fe2c5d8921e6d",
          "bytes": 20102,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/03.png",
          "sha256": "b2f0c161ab67d26a354cdae59a8ff22622d9e315405b869774df8109255912b2",
          "bytes": 20675,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/04.png",
          "sha256": "ae63f2494431601fd48af69776002cd91afdf69eb373083f9e81bf67f70fb6b2",
          "bytes": 19461,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/05.png",
          "sha256": "66678fccaec6b4c1827fbd2e7d2a75960d8f1c0f5be61e57e487b7e73abaab2c",
          "bytes": 19970,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/06.png",
          "sha256": "39532fe50ea9ac4b789036816624741f7a3fd32fe7b519a756d80b43788c47ef",
          "bytes": 19662,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/07.png",
          "sha256": "9b0a1217bea89391d0fb50ae164c469c10ecfde3b30ac720ae0cc090562ba6f8",
          "bytes": 20525,
          "duration_ms": 220,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running-left/frames/07.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::running-left",
      "id": "rei-white",
      "state": "running-left",
      "row": 2,
      "frame_count": 8,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-B/originals/running-left/attempt-01/source.png",
      "source_sha256": "cde6c349fb6f788bb3da9a4aeb01dd523650d1fb7bdea7463ca0f29330d37a5f",
      "action_asset_hash": "1d4159aa0e6b1fc4852869a0f186056985d30ddcd38429f576a25bbe66a10044",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "8/8 frames facing left, natural stride with airborne frame 4 (bottom=180), upright unmirrored 00 verified on high-res source, orange wrist rings and green accents intact, min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/00.png",
          "sha256": "d244c17c579c69d93198a55d5a6cace508eaa9abf5385b7120fbdc740e96113d",
          "bytes": 20400,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/01.png",
          "sha256": "9aa079e8ef9ccd9367122350f3844a27d57233d972677596718c3f9d5a7cc99d",
          "bytes": 19443,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/02.png",
          "sha256": "4f3fa1e424e6a9cd19b8dbab51dc058da006cc1e04a268de399ebde12206efb7",
          "bytes": 19560,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/03.png",
          "sha256": "15a2d96773c1b3dae3f5aa8cd0e168992bd24daa40a3dc09378f0d08e5a4f690",
          "bytes": 19305,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/04.png",
          "sha256": "daa80e194e75943b19a5457cd093e03fd2b3c66f4b01712f3c2173bc0fc6f3ea",
          "bytes": 19854,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/05.png",
          "sha256": "9933a0dd7d5661e9f1b5d3d80a636c79548b8774ed398ecfb0c7ee382660aff9",
          "bytes": 19644,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/06.png",
          "sha256": "e704e1981a6c4d1d174ebeebd5072dcbe2694b228a7f545b2e542627ebbbe84a",
          "bytes": 19520,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/07.png",
          "sha256": "2c416b6dba8843ddfbe488faebd4b5d42da40fc84ddfe0bb0cdeb4badd487031",
          "bytes": 19615,
          "duration_ms": 220,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running-left/frames/07.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-black::running-left",
      "id": "rei-black",
      "state": "running-left",
      "row": 2,
      "frame_count": 8,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-B/originals/running-left/attempt-01/source.png",
      "source_sha256": "f2d2167a7fff906179961dc5491d82caa223d81f43b97b530a767113cbf42b2b",
      "action_asset_hash": "b74ab3777fd3f8496cee92d33dd0dfa814d94d008f99164d452148fc6d92450b",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "8/8 frames facing left, arm-holding released with natural arm swing matching FIX-BLACK running-right kinematics, upright unmirrored red 09 verified across all 8 source poses, red boot trim intact, min_top=5px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/00.png",
          "sha256": "868ebfe4a5ad3f6ac8fe4f93139061e5ff2f6e85a64cb9629dffd10d5485455e",
          "bytes": 18897,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/01.png",
          "sha256": "c6969dee1fa7190c10cade0ed114003a3d4dda45cb5c0ab3822916e712f74b20",
          "bytes": 17169,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/02.png",
          "sha256": "a35edfec9a70144c06678a06e990729c051ec8fd352fb51d831d6744ba0dcaf4",
          "bytes": 17041,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/03.png",
          "sha256": "f7447d25daf7cb022a91775a78472e2023ab02c5f456d953824c5288863ab725",
          "bytes": 16691,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/04.png",
          "sha256": "52aea46b960a46a759ef40c530a403dc9dea9bf2e678cd4d86684e7ecb8bef02",
          "bytes": 16675,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/05.png",
          "sha256": "d644cc391a15dfd28756db11a19b9dc6712f1a9941a248f7ebee9f15780c3c2d",
          "bytes": 17037,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/06.png",
          "sha256": "21567ec5bd5c754ebbd5a7dbdf8f66953f4511a30e1e885f9b07806b61dd22cc",
          "bytes": 17251,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/07.png",
          "sha256": "1cfdad1a087f38e0c3414cfce44fa238ee09a2766203631f2f5e158292f4d02c",
          "bytes": 18474,
          "duration_ms": 220,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running-left/frames/07.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-school::waving",
      "id": "rei-school",
      "state": "waving",
      "row": 3,
      "frame_count": 4,
      "durations_ms": [
        140,
        140,
        140,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-B/originals/waving/attempt-01/source.png",
      "source_sha256": "f5d912e0512801f733fb3e00d35341e7bb48885549f384f0c07d337182ade373",
      "action_asset_hash": "f8d10a5c310d0dab3bead9eb117f86b3105a5f0c340b321ab77475be96f8634f",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "4/4 frames: F1 clasped hands, F2-F3 clear right-hand wave with gentle expression, F4 returns to clasped hands; clean loop and alpha, min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waving/frames/00.png",
          "sha256": "0618583cc278ff907c2fdf02e1e1ca38749c6638baa61a94ff8bd359302ad225",
          "bytes": 18890,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waving/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waving/frames/01.png",
          "sha256": "ffc2ed2eecf05d2b3840f8648934a3c1ef4c7f76b358b6f1f6e7281d53f532df",
          "bytes": 19803,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waving/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waving/frames/02.png",
          "sha256": "8cafa87cf922f7b468ef1155a1cdb9e1019121d378e392eabdeb348cfc07dbb8",
          "bytes": 19790,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waving/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waving/frames/03.png",
          "sha256": "004849ad6501abe1d9b32f832fbf71a6320ef175d08608f44e0e01a26c1880db",
          "bytes": 18736,
          "duration_ms": 280,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waving/frames/03.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::waving",
      "id": "rei-white",
      "state": "waving",
      "row": 3,
      "frame_count": 4,
      "durations_ms": [
        140,
        140,
        140,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-B/originals/waving/attempt-01/source.png",
      "source_sha256": "4061d98ce9c35187932ff127f61a4d7c3de8bd5faa46031f924a6f122715c513",
      "action_asset_hash": "3393ac46fb99c4d46207e014b60fb3c84ae5a8eb010c7282ca19281c5b40f436",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "4/4 frames: F1 arms down, F2-F3 clear right-hand wave, F4 returns to arms down; upright 00 and five-finger silhouette intact, min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waving/frames/00.png",
          "sha256": "0206e5e434a670863e9d2ef8994a648fdfdb82ae04e7581a21b5a46ce5b79784",
          "bytes": 20001,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waving/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waving/frames/01.png",
          "sha256": "c5f8e2da657d6d7f0688a4794ba5975d19510dc1455f1de74a57ca3f517eef9b",
          "bytes": 20803,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waving/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waving/frames/02.png",
          "sha256": "bd5d3d9265bbfb32cdd4c26cc9ba31cc7dfc35f951d414be13f9e99e851c26c2",
          "bytes": 20590,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waving/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waving/frames/03.png",
          "sha256": "f8ea76f4e1f8d3110d9d4251cb3199ebd0eb5c2d43a35ed1b182e102d201ced3",
          "bytes": 19882,
          "duration_ms": 280,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waving/frames/03.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-black::waving",
      "id": "rei-black",
      "state": "waving",
      "row": 3,
      "frame_count": 4,
      "durations_ms": [
        140,
        140,
        140,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-B/originals/waving/attempt-01/source.png",
      "source_sha256": "c03589bb17791d2c7de3bad4894677dac90bb69bc78e8fe4d77a2d06545dd94f",
      "action_asset_hash": "207bcd01642b577f773ce5a37dca5a51fabcdd966213547c13080384bf84ad55",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": true,
      "qa_attention_note": "F1/F4 双臂放松垂放（未保持扶臂默认姿态），请确认是否接受该姿态设定。",
      "agy_visual_notes": "4/4 frames: F1/F4 relaxed arms at sides, F2-F3 clear right-hand wave; red 09 intact, min_top=6px. Note for art review: F1/F4 release static forearm-hold.",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waving/frames/00.png",
          "sha256": "0f78086607cdef1171b67a24510429f8b341859446b6dc35bdbe848733a1ad71",
          "bytes": 18484,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waving/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waving/frames/01.png",
          "sha256": "a809b13e861a45a9c5c7f235b6232c97fc888025d33d53e77aedc87d187d5957",
          "bytes": 19224,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waving/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waving/frames/02.png",
          "sha256": "0c02a107cb91bd3af0411586733de1ed677b89c732d63bc1dc5f09a24f4211f3",
          "bytes": 19249,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waving/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waving/frames/03.png",
          "sha256": "a6ea26435f5bebff4132edd5b471fc1cd84c3afec7e8fc6cc7a72a953c49cc0b",
          "bytes": 18317,
          "duration_ms": 280,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waving/frames/03.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-school::jumping",
      "id": "rei-school",
      "state": "jumping",
      "row": 4,
      "frame_count": 5,
      "durations_ms": [
        140,
        140,
        140,
        140,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-B/originals/jumping/attempt-01/source.png",
      "source_sha256": "822683b5ea610eef753b51154c995f14506a0e83eccbf84850121251ed01f948",
      "action_asset_hash": "678d7e17289950b34110fbe9f2d6a746a703210174e666f48606c153729b86c4",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "5/5 frames: crouch (h=171), takeoff, airborne peak (bottom=183, 12px lift), landing crouch, clasped standing recovery (h=188); no top clipping (min_top=4px).",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/00.png",
          "sha256": "8345534b6ad18683cc924604c22c87e5e52441f1a8da2af52dfd8693698d7879",
          "bytes": 20607,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/01.png",
          "sha256": "e4160b549a7d6bb93a9599fd53623063a33242c4d0f23531ef42dc7d72ed8761",
          "bytes": 22314,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/02.png",
          "sha256": "f97b6c073805399d6e4a60bbaa8069222b671a39f2e8bdbaa2b90477d972c276",
          "bytes": 22424,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/03.png",
          "sha256": "41a34724210135b27c15b90c460024efe2ddc18b1d21d134fbf3bdf9a862c3a6",
          "bytes": 22613,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/04.png",
          "sha256": "9e2589e9cbd32df5854130ff7343d4d3d40ac95c1bc6248da6017e71259d0794",
          "bytes": 19598,
          "duration_ms": 280,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/jumping/frames/04.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::jumping",
      "id": "rei-white",
      "state": "jumping",
      "row": 4,
      "frame_count": 5,
      "durations_ms": [
        140,
        140,
        140,
        140,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-B/originals/jumping/attempt-01/source.png",
      "source_sha256": "520c682bd24b246c29244e3d73123b7f4fd0f8fb25d0965ed72af580b00ace3a",
      "action_asset_hash": "6839fdc808b30befc85e356ab29840b3022974e238be720fe31d57d5cb8f6716",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "5/5 frames: crouch (h=170), takeoff, airborne peak (bottom=178, 17px lift), landing crouch, standing recovery (h=182); upright 00 intact, no top clipping (min_top=4px).",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/00.png",
          "sha256": "422f2706c693b29c3c55eb5ff79aa421e9a7461cbfe55376412215ee8d7290eb",
          "bytes": 20625,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/01.png",
          "sha256": "144e63806ba5901824cf9cb9531932444925f62eb9de7018523bc81457b4dccd",
          "bytes": 19649,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/02.png",
          "sha256": "5dbdcc85e1dd4e1ac357d89a8f28f73d010507f589095206359a22e516fb27c3",
          "bytes": 19412,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/03.png",
          "sha256": "08809d025d6f6fbac90865d6d7db5190807d6b49d55090ea9b3490e2406e54a7",
          "bytes": 20575,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/04.png",
          "sha256": "7aeeddc3e8dcc3d92ffc9908350877d12e2fb24ad10293331649f62e64e0900d",
          "bytes": 20664,
          "duration_ms": 280,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/jumping/frames/04.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-black::jumping",
      "id": "rei-black",
      "state": "jumping",
      "row": 4,
      "frame_count": 5,
      "durations_ms": [
        140,
        140,
        140,
        140,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-B/originals/jumping/attempt-01/source.png",
      "source_sha256": "b6686cbcf4806d08a17c6f43d1dcc27fbaa7ac3d12e08317368ca33f53102b69",
      "action_asset_hash": "88f126a36238a96084cf6292b52b7104c5462a304bf9a6cd2951b3fd2ff36492",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "5/5 frames: crouch (h=162), takeoff, airborne peak (bottom=182, 13px lift), landing crouch, standing recovery (h=189); red 09 intact, no top clipping (min_top=4px).",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/00.png",
          "sha256": "a623986c0c042a401227b8febea2a2e2bdcd7ef8b2b6b19d92097ec74752f9d7",
          "bytes": 18381,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/01.png",
          "sha256": "31d4db5e5d4f962e67a3fed69d6ba49820cfb8bae6767a6cd573ec6bc86da39b",
          "bytes": 19301,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/02.png",
          "sha256": "9508efb23d597624b588f9a42bf646e1cb4a75f4f7b91cab81fbecf8c2a5fa32",
          "bytes": 18746,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/03.png",
          "sha256": "56b016f8a98e7c4b92bc0ce9810d52bca28b9a5bbbac3f2c029bac41463beb97",
          "bytes": 19185,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/04.png",
          "sha256": "c0b23dea6e4eb3389766f8827972f6849fd7baf74997062639da4faffe27eab1",
          "bytes": 19587,
          "duration_ms": 280,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/jumping/frames/04.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-school::failed",
      "id": "rei-school",
      "state": "failed",
      "row": 5,
      "frame_count": 8,
      "durations_ms": [
        140,
        140,
        140,
        140,
        140,
        140,
        140,
        240
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-B/originals/failed/attempt-01/source.png",
      "source_sha256": "8db340b9d75539d41884324995bb68e0670aa3268cd139419c29515e528d919b",
      "action_asset_hash": "9281dc25a0a3921f595632f51737d06e454fce4690624d92a6e18776bb9c5a94",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "8/8 frames: gradual head bow with downcast/closed eyes F3-F5 and calm recovery F6-F8 while maintaining clasped hands; min_top=4px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/00.png",
          "sha256": "647e7dba809095f8372655a4f987042d6bf54f46b4b65d78cd3668759949a887",
          "bytes": 19666,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/01.png",
          "sha256": "bd45847583ffe9c8000e1c352858a4a001130485ea9aa26387364de27c404993",
          "bytes": 19097,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/02.png",
          "sha256": "1c03c4cc373df156dd9d0368eee95e6728e83091fc3b293f4795ff7f8b918a2b",
          "bytes": 19344,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/03.png",
          "sha256": "b8d99f7a9fc37cd17fcce30c7ac44569a0686d0ef488f5b1f4bddb807a5839d8",
          "bytes": 18895,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/04.png",
          "sha256": "f816aa982b6a24e3b01298b2275d88ee23077911c922584f0d9e7455ec87e8bb",
          "bytes": 18900,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/05.png",
          "sha256": "dcf505ab47de099468bdad059d983a8bda854ccd079ae63888e25bcc0647eead",
          "bytes": 19120,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/06.png",
          "sha256": "f83116f9e6377c740b6c8e2b004188562f7079d5635804d3ceee42df80cdaedd",
          "bytes": 19196,
          "duration_ms": 140,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/07.png",
          "sha256": "be65a3f55bde239bfa91c40fd221708db7c4960cc638fb09085c66003a0e7423",
          "bytes": 19102,
          "duration_ms": 240,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/failed/frames/07.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::failed",
      "id": "rei-white",
      "state": "failed",
      "row": 5,
      "frame_count": 8,
      "durations_ms": [
        140,
        140,
        140,
        140,
        140,
        140,
        140,
        240
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-B/originals/failed/attempt-01/source.png",
      "source_sha256": "52de6d4b494e0dd6409bcb447d56a8ed9d400bd14754f6cdc2184261739413b6",
      "action_asset_hash": "b629c22f02de14dc3f3c6983b6dac697a7ae4f8fd408450cc8d02d807a0a2adf",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "8/8 frames: eyes lower and head bows F3-F6 with subtle hand curl, recovers F7-F8; upright 00 intact, min_top=4px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/00.png",
          "sha256": "5cee434ec359b5e0653c6721d92823d41635d5fa343637b107772e869e287fe8",
          "bytes": 19629,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/01.png",
          "sha256": "b89ac721e49ad3e173dec392e698f7f0a96936525130361260485e3aa774847f",
          "bytes": 19434,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/02.png",
          "sha256": "dee573a5665bf635a9bf3a7af3ec4e3f0a01aab6fe9e8fe0c640d97ae8859b56",
          "bytes": 19449,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/03.png",
          "sha256": "03a7d1a8cd4e250c7ee43066435cfd1eb11be691441f867a6577ddc0f2658878",
          "bytes": 19121,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/04.png",
          "sha256": "c71adecf2b06bffcf4d1912a8d18fadf8a5fb2c7746909838379467120e67431",
          "bytes": 18844,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/05.png",
          "sha256": "eba7b79288024bc8c66093efe921c57ed3d90d77165a7aa16e11822a5333374e",
          "bytes": 18714,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/06.png",
          "sha256": "f3b2ceabdad37fc29b3afb93385e6013fe84625780d7f2d6f75fa8cc9c9165f4",
          "bytes": 19326,
          "duration_ms": 140,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/07.png",
          "sha256": "44f9ca9aa52d61986e6190319bd8d1ddf2751b4f431e3bd929acdfaa70f1b77a",
          "bytes": 19205,
          "duration_ms": 240,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/failed/frames/07.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-black::failed",
      "id": "rei-black",
      "state": "failed",
      "row": 5,
      "frame_count": 8,
      "durations_ms": [
        140,
        140,
        140,
        140,
        140,
        140,
        140,
        240
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-B/originals/failed/attempt-01/source.png",
      "source_sha256": "4d9aadd34fa598cc81f23f7c34f539bfd9e37950a7bbaa5ba7bab359f60e3460",
      "action_asset_hash": "dd7f3ecac76f6cd66800a4084a0b749d1d10b731591ca71197239739ee1e14f0",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "8/8 frames: retains right-hand-on-left-arm posture, bows head with closed/downcast eyes F3-F5 and slowly recovers F6-F8; red 09 intact, min_top=4px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/00.png",
          "sha256": "2a94b76c70ad9d7412e34d405b8d0bc29b5c556b717d01b3dafa2820adaea666",
          "bytes": 18077,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/01.png",
          "sha256": "21056485888b62cfee37f10762db28c5062b941eff3d200811f408b66404ccb0",
          "bytes": 17763,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/02.png",
          "sha256": "1c58bbfebd306212aaa047840639729b1c9ef24f72215af10db74a3c8a4ce3db",
          "bytes": 17707,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/03.png",
          "sha256": "c85dc33091c2717dcb9a2de9484b4b33f7be5da1f431dc228f8c2324e7d31acc",
          "bytes": 17689,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/04.png",
          "sha256": "7c404c37b88311611670719855c46848b497f0cb495e7ea63c53e0c3ef1f48aa",
          "bytes": 17632,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/05.png",
          "sha256": "c87da6da9d0c2d79ca04aa32783ac0ed797db324a3112d1622fbaa02d57084e8",
          "bytes": 17633,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/05.png"
        },
        {
          "index": 6,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/06.png",
          "sha256": "4e594236e2daea854c2c284e55f256a716919902fc0e8e87242f379ccbcf616c",
          "bytes": 17734,
          "duration_ms": 140,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/06.png"
        },
        {
          "index": 7,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/07.png",
          "sha256": "7eefad9c5fb0a9bceba8f5f5c2a4609762affde93f41692698b5b5f79c00b2ea",
          "bytes": 17783,
          "duration_ms": 240,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/failed/frames/07.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-school::waiting",
      "id": "rei-school",
      "state": "waiting",
      "row": 6,
      "frame_count": 6,
      "durations_ms": [
        150,
        150,
        150,
        150,
        150,
        260
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-B/originals/waiting/attempt-01/source.png",
      "source_sha256": "f19efac284e80c3d2ac242fac507b162a8085ecb458e3de5b89345f6a98abcc7",
      "action_asset_hash": "6a8c2043bad88bf1500a832d47684cc0e61c5e7b4d42f292ba3f411f2defc6f9",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": true,
      "qa_attention_note": "F6 举掌状态切回 F1 双手交握的循环过渡较直接，请重点复核循环观感。",
      "agy_visual_notes": "6/6 frames: head tilt F2, left hand palm-up inviting input F3-F6 with blink on F5; min_top=6px. Note for art review: F6 holds palm-up before looping to F1 clasped hands.",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/00.png",
          "sha256": "60fae5f8619315c18c9f885fd9665da64fd29f3dca4c475ea1e57571b84333d6",
          "bytes": 18948,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/01.png",
          "sha256": "6f2e3a27e2566324ee3c6930d35c93a9ca6091f28c5d9db39c7f5dbce2f0a3a7",
          "bytes": 19137,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/02.png",
          "sha256": "c227245353c2ad84fd31e02a78db393fdef34506911cb47f11d410a5fb35921f",
          "bytes": 19351,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/03.png",
          "sha256": "2a28e392ba01d0083a26c8f8901814f8bb8235b76cdfe5c886be9f751378edfe",
          "bytes": 19265,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/04.png",
          "sha256": "422030aa32515f677e2b812d353f49ebed0bad4043879d153783a4840f426db0",
          "bytes": 19320,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/05.png",
          "sha256": "0e12bc4093cd99c483963999ec5ed2096ebf051aecd28bbe24b83d819f78a371",
          "bytes": 19070,
          "duration_ms": 260,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/waiting/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::waiting",
      "id": "rei-white",
      "state": "waiting",
      "row": 6,
      "frame_count": 6,
      "durations_ms": [
        150,
        150,
        150,
        150,
        150,
        260
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-B/originals/waiting/attempt-01/source.png",
      "source_sha256": "b1fb0624055ac88ceb2857bd1a88c848b456eebfa4d8ff54f75766b2eaf7fa61",
      "action_asset_hash": "b772bb07091623db729a1822b6ff34734926d6889c671f898c4305e592c7f0f8",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "6/6 frames: slight tilt F2, right palm-up inviting gesture F3, front clasped waiting F4-F5 with blink, returns to neutral F6; upright 00 intact, min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/00.png",
          "sha256": "dd2e0c4cf9e6d71049045e8d1fd050a50435cc132fac42acfb1b851a58048319",
          "bytes": 20775,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/01.png",
          "sha256": "389996cd8768d16a4be69e3a07d1944436fb2094cd661972872d951823aac6ec",
          "bytes": 20552,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/02.png",
          "sha256": "646bf286e218b87c0b82ee6556126448f29dd5cab6c3a43f2de739ed37916995",
          "bytes": 20962,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/03.png",
          "sha256": "ff67ee640502a481ad7d0916751d97f2a026dc3cf035a94d9d5dca0b37649bef",
          "bytes": 19204,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/04.png",
          "sha256": "57918ee2c21cd3c1f2bef52ea93c22405df3ab5c22ec8ac0fc207b0fd532e8c2",
          "bytes": 19210,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/05.png",
          "sha256": "90baf42550ba609e97e27319127b355ad29ac0966b897e642f4ecbf7c256608d",
          "bytes": 20679,
          "duration_ms": 260,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/waiting/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-black::waiting",
      "id": "rei-black",
      "state": "waiting",
      "row": 6,
      "frame_count": 6,
      "durations_ms": [
        150,
        150,
        150,
        150,
        150,
        260
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-B/originals/waiting/attempt-01/source.png",
      "source_sha256": "30ff123b875281bdae4764a1287f95bfdf0f046fe046997363cda56d8a57f53e",
      "action_asset_hash": "0efd20a241604b247c15f1119025d015c72eb5fd397f1c4616a9c22a73daaa55",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "6/6 frames: arm-hold F1-F2 with subtle head tilt, brief right palm-up prompt F3, returns to arm-hold F4-F6 with blink on F5; red 09 intact, min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/00.png",
          "sha256": "487110ccb999b2454ca22e82bd521a274f8abbc3ee5a3bacd0c4f704702211c6",
          "bytes": 18128,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/01.png",
          "sha256": "7329405a82be00400a14a8d9344db18ae362bc3d976323dc405efb61aa46c679",
          "bytes": 18245,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/02.png",
          "sha256": "a88c3d7155c7706d15a3e69d557e8dd20a29ecda4748807b469acfe34062810a",
          "bytes": 19747,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/03.png",
          "sha256": "6e2c69aaf8d3543e8d731a4863aedc6b63e3a575459acc1ef29a6f7fef41bfbb",
          "bytes": 18362,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/04.png",
          "sha256": "f2f4d49466f5d94802ee62f6b77d7a8c077070fff60b52aad829499075e85bc9",
          "bytes": 18062,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/05.png",
          "sha256": "c42292df7b7d2401bc9688235e949c5dd163e576e6f050d4f58811b6f28b1c62",
          "bytes": 18095,
          "duration_ms": 260,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/waiting/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-school::running",
      "id": "rei-school",
      "state": "running",
      "row": 7,
      "frame_count": 6,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-B/originals/running/attempt-01/source.png",
      "source_sha256": "a0363ce03798cd63ea67f20be7d465d93bcba8ed4b20c73a7d6c094ec19c4fc7",
      "action_asset_hash": "d95ced0f187265d7b3cb0a77ffa18fa19a1b14706619ad3073b4525d8df756a9",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "6/6 frames: focused working/thinking state (not lateral run); right hand raised near chin/collar F2-F6 with blink F4 and subtle finger motion; min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/00.png",
          "sha256": "9f68cc97aacb1ad03183e6924e7603a3f2a62c138aeb1d998822a708a83f53ff",
          "bytes": 18804,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/01.png",
          "sha256": "a5e9cbe096966b0df538de0fc62f7f39d126bbbe8714c15ceb2e02095bd92066",
          "bytes": 18638,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/02.png",
          "sha256": "0927a8d52018c171bee9ad9388eca91d1b63f0f3ce61fb81d128a06f56cfadec",
          "bytes": 18838,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/03.png",
          "sha256": "14c3fd6fc6c95335a57df0a19e2a65303d1504cf5174ac3b61d87e2558faa662",
          "bytes": 18818,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/04.png",
          "sha256": "44872f11ff115539c962bde1601f648ea6ab92e950b3a8e5c3c3d8409ca869c8",
          "bytes": 19147,
          "duration_ms": 120,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/05.png",
          "sha256": "256ff54f8358c520e1637979c802ae717f13120bffdebb7e88bc27909bcda7ce",
          "bytes": 19057,
          "duration_ms": 220,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/running/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::running",
      "id": "rei-white",
      "state": "running",
      "row": 7,
      "frame_count": 6,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-B/originals/running/attempt-01/source.png",
      "source_sha256": "979fbc33e540edd7666d1234c778d50ff33f07c0fd1e7ee2e8254873d334aca6",
      "action_asset_hash": "d0b9df0fff3a7c336b6dd6ba1f8f28a1523bd06c32b439e72e7c3c89897434e0",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "6/6 frames: focused working/monitoring pose (not lateral run); right hand raised near chest/chin F2-F6 with gaze focus; upright 00 intact, min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running/frames/00.png",
          "sha256": "097b08b20192520119f4a0927266b6452438ef7147fbed1d9fb4210c9f12de93",
          "bytes": 19859,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running/frames/01.png",
          "sha256": "eec164b0f8dda1fa0007b96abc010da0ccdee796b16446066f2372eeebc5f1f0",
          "bytes": 19509,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running/frames/02.png",
          "sha256": "a2b91fc137e93e2f21bdc4d422ff4bb41222e55918ebcbc4babefcefbe8a60b4",
          "bytes": 19691,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running/frames/03.png",
          "sha256": "38b1ed1576728d34292fdd109805155ba08d354948ce336ebce3e4d6b9d8907b",
          "bytes": 19821,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running/frames/04.png",
          "sha256": "ab888b3696433632c30c8eab583def49be42efaa7e038d2c9b011ea4e540bbac",
          "bytes": 19626,
          "duration_ms": 120,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/running/frames/05.png",
          "sha256": "ad44969c6767aec43a18e5391f6b07d91129ec127a9fe363251fd93304a78fbe",
          "bytes": 19711,
          "duration_ms": 220,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/running/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-black::running",
      "id": "rei-black",
      "state": "running",
      "row": 7,
      "frame_count": 6,
      "durations_ms": [
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-B/originals/running/attempt-01/source.png",
      "source_sha256": "6ccc29640f1f21bf650286d29b7f879b01b1fd5df80c4423f22c9cd6aaccbcc8",
      "action_asset_hash": "7f8bd42b42dd291b530a8316fcc0ef2a8eb3e3c1c0fb0092250d3ebc648cf835",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "6/6 frames: quiet working/thinking pose (not lateral run); right hand near chin/collar F2-F6 with blink F4; red 09 intact, min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/00.png",
          "sha256": "975cdcb0d35aa3a324e65e09c32ac8872eab8ef296653dda3195574ef4d6eb81",
          "bytes": 19449,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/01.png",
          "sha256": "36aa0c616a1d62ce5765f64d816abef6c6ce73fd0183d5f56a4d96891fc3f38b",
          "bytes": 18834,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/02.png",
          "sha256": "51d094ce2dfe19a6413fedf7a0622486673e53ad417a4a40689af6c04c9b404b",
          "bytes": 18927,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/03.png",
          "sha256": "1ab409e54423f18cd60468f2fc54f023d33ba6ab8d1377ffc88a88400ecbd187",
          "bytes": 18622,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/04.png",
          "sha256": "28e8240eb675d1f5e605093684c933f760a3303d7fbc5863e480d5376d95e394",
          "bytes": 18550,
          "duration_ms": 120,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/05.png",
          "sha256": "40bd3528bfa3cdc10c1d0705b371cd2f828c6777c458e51ebb313ade84337352",
          "bytes": 18500,
          "duration_ms": 220,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/running/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-school::review",
      "id": "rei-school",
      "state": "review",
      "row": 8,
      "frame_count": 6,
      "durations_ms": [
        150,
        150,
        150,
        150,
        150,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "03_校服绫波丽/P4-B/originals/review/attempt-01/source.png",
      "source_sha256": "f206d391d1ba00af8ef54e42d7423272fb72eb026c9a06d152ece4c1865d27da",
      "action_asset_hash": "57a44d7db516a2c456fc283632716b1ba80812812f93466c0d018661522efcae",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "6/6 frames: attentive glance F1-F2, forward inspecting nod F3, eyes-closed confirmation F4, slight lift F5, neutral return F6; min_top=5px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/00.png",
          "sha256": "eca5ad735723103f1be5afa59bcc5886860e4c2217b06041722ed399b03e72b2",
          "bytes": 19639,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/01.png",
          "sha256": "d9801b942b5b1749b2019748401b02f489e1632aec4e386d8a9b4dcde59a1434",
          "bytes": 19450,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/02.png",
          "sha256": "6db73cecbc4042265267d11d23f037c056dc8aabd309cc6495a9aaf31c2aa5b5",
          "bytes": 19640,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/03.png",
          "sha256": "2e1425fb6f6d47876de8437c2284d1b12f653dade6edb4c07d9d3f6751fb595b",
          "bytes": 19322,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/04.png",
          "sha256": "25939edfd469b6b04a11a6a30b66b27282a16ed7d429ed49eb3d0d64a4b080ae",
          "bytes": 20288,
          "duration_ms": 150,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/05.png",
          "sha256": "5041def737aa3cc647e810a57138eea90f336a28014852ca72371538e05d84a1",
          "bytes": 19509,
          "duration_ms": 280,
          "src": "../../03_校服绫波丽/P4-B/candidates/attempt-01/review/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-white::review",
      "id": "rei-white",
      "state": "review",
      "row": 8,
      "frame_count": 6,
      "durations_ms": [
        150,
        150,
        150,
        150,
        150,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "04_白色战斗服/P4-B/originals/review/attempt-01/source.png",
      "source_sha256": "bfa67dcc7df30b36e4819cf066e31d7e28b58d311dcfa51df020027287bfae61",
      "action_asset_hash": "2a81aa6578a7129e2c594e6a1d6e158ba485a7e363cf947491b74ee8edb27cfa",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": false,
      "qa_attention_note": null,
      "agy_visual_notes": "6/6 frames: attentive gaze F1-F2, downward inspect F3, eyes-closed confirm F4, slight chin lift with waist-touch confirm F5, neutral return F6; upright 00 intact, min_top=6px.",
      "frames": [
        {
          "index": 0,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/review/frames/00.png",
          "sha256": "081546aef0782ff1611ff2a4b3e7a8a2abaf5e4c68bd21d226b7a405e06fbd5b",
          "bytes": 20304,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/review/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/review/frames/01.png",
          "sha256": "8a5c68e60618617855f513388d0c4f70f652230addf9a73d9bb3446c4c7b22d1",
          "bytes": 20401,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/review/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/review/frames/02.png",
          "sha256": "d6102a9e34cb22013d1f4efaa2da97599b32ef20e2f1225677433404ed81781f",
          "bytes": 20841,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/review/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/review/frames/03.png",
          "sha256": "0405b871331281b0d97f86fc2bdc86f54810283009206fc5a10efb0fb3c1bfb5",
          "bytes": 20395,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/review/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/review/frames/04.png",
          "sha256": "825a2ae9ab61ef991ef2842aea1647ebf0609eaf99796bf396660ec29d48898f",
          "bytes": 20385,
          "duration_ms": 150,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/review/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "04_白色战斗服/P4-B/candidates/attempt-01/review/frames/05.png",
          "sha256": "3ae5d48f4304d989987e58cbfff232612b54f807792f9f49c6a9c5f1a7a51389",
          "bytes": 20400,
          "duration_ms": 280,
          "src": "../../04_白色战斗服/P4-B/candidates/attempt-01/review/frames/05.png"
        }
      ],
      "historical_comparison": null
    },
    {
      "key": "rei-black::review",
      "id": "rei-black",
      "state": "review",
      "row": 8,
      "frame_count": 6,
      "durations_ms": [
        150,
        150,
        150,
        150,
        150,
        280
      ],
      "selected_version": "P4-B/attempt-01",
      "origin_phase": "P4-B",
      "produced_by": "Codex (reused & assembled by Antigravity)",
      "protected_p4a_baseline": false,
      "structure_qa": "PASS",
      "source_path": "05_黑色战斗服/P4-B/originals/review/attempt-01/source.png",
      "source_sha256": "faff066c8746f815a996d1355379d91c8a753fc66626d5ea507b7c24bee2c5c8",
      "action_asset_hash": "c3f7a6b6ae0077045b4308e46a4d1cc8cb3b78218a550109075c09370b81bae1",
      "initial_status": "PENDING",
      "initial_comment": "",
      "initial_updated_at": null,
      "locked_preapproved": false,
      "qa_attention": true,
      "qa_attention_note": "F1–F4 保持扶臂、F5–F6 转为垂臂，循环回 F1 存在姿态切换，请重点复核。",
      "agy_visual_notes": "6/6 frames: arm-hold attentive gaze F1-F2, inspecting lean F3, eyes-closed nod F4, releases arms to sides F5-F6; red 09 intact, min_top=6px. Note for art review: F6->F1 transitions from arms down to arm-hold.",
      "frames": [
        {
          "index": 0,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/00.png",
          "sha256": "88ab156a6e0763542828b5c4adcf562f99284c312c9659d864721e92e5e182ff",
          "bytes": 17807,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/00.png"
        },
        {
          "index": 1,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/01.png",
          "sha256": "2c32b1fb63b334312a088d909ad7bb1b950f503076730c71450d72fe7c18a303",
          "bytes": 17784,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/01.png"
        },
        {
          "index": 2,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/02.png",
          "sha256": "170cffdc4aaa85f142de821c11075d62e34b834a9c74a86d246490c3ffc833c3",
          "bytes": 17868,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/02.png"
        },
        {
          "index": 3,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/03.png",
          "sha256": "80c1df5d422cb706e6ed82c8cbbe5438c5b3b604e634e3b45bbdf3d6fff0fccf",
          "bytes": 17818,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/03.png"
        },
        {
          "index": 4,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/04.png",
          "sha256": "685b8989d69d0b6c71ccd26731dbeb78c0811c608d3de29d30b22d69e0e3cde5",
          "bytes": 18656,
          "duration_ms": 150,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/04.png"
        },
        {
          "index": 5,
          "repo_path": "05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/05.png",
          "sha256": "36b1723e6b923269eb58c97de7997f0969399f5a857ff9889ea1a0af31587ae9",
          "bytes": 18478,
          "duration_ms": 280,
          "src": "../../05_黑色战斗服/P4-B/candidates/attempt-01/review/frames/05.png"
        }
      ],
      "historical_comparison": null
    }
  ]
};
