window.REI_PILOT_DATA = {
  "frameCount": 10,
  "blackMaster": {
    "version": "P3 派生 RGBA 母版",
    "sha256": "a19715e0c2e4df83b206f30ee03d6044b0665c911ee85aa31899f118ecad81ce"
  },
  "samples": [
    {
      "id": "waiting",
      "version": "codex-cloud-pilot/attempt-01",
      "sourceSha256": "f68e585c5b73214a41d38585aa394d42fcb0961840bbc6e28b33d3024b232b89",
      "frames": [
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/waiting/attempt-01/01.png",
          "sha256": "5580b4b1749467f7770e39a5dbe2c9e19100431ee5e6b82a84522b015ccb3f56"
        },
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/waiting/attempt-01/02.png",
          "sha256": "03a03495ca1b4d131b03c8e96d4c8e365db2890c48e1c4dbbaba4b02e148af64"
        },
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/waiting/attempt-01/03.png",
          "sha256": "71f15dbd0b52d77c8d4a7764638d88449437cee15cb57078e34694645fb59efa"
        },
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/waiting/attempt-01/04.png",
          "sha256": "368f644cc9430c464c8548f5c365a5c93095a7acee8a16a7c7f48e17e034ef94"
        },
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/waiting/attempt-01/05.png",
          "sha256": "63f782be6f799df94129ccdc7ba2a297f7a3ad61df083940c0f69a6c608c280b"
        },
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/waiting/attempt-01/06.png",
          "sha256": "b0dfc778e4e5428001112acb7a08a8e0d7ecd6c3e23b6f10c86714acdf64b2af"
        }
      ]
    },
    {
      "id": "000",
      "version": "codex-cloud-pilot/attempt-02",
      "sourceSha256": "5e07e68eaa870e4ff2cf425597ce3e3af599a136624ec24d5651444528471a5a",
      "frames": [
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/directions/attempt-02/000.png",
          "sha256": "b315906ecff13dfe97402886a0ee4c86fb340b52903748340e22ef37e384873b"
        }
      ]
    },
    {
      "id": "090",
      "version": "codex-cloud-pilot/attempt-02",
      "sourceSha256": "5e07e68eaa870e4ff2cf425597ce3e3af599a136624ec24d5651444528471a5a",
      "frames": [
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/directions/attempt-02/090.png",
          "sha256": "3d18e479d038ba17a46938a1fc46c059ea0d678f174a520d77be1c7035efcba4"
        }
      ]
    },
    {
      "id": "180",
      "version": "codex-cloud-pilot/attempt-02",
      "sourceSha256": "5e07e68eaa870e4ff2cf425597ce3e3af599a136624ec24d5651444528471a5a",
      "frames": [
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/directions/attempt-02/180.png",
          "sha256": "9c4cc7626c6462eaf723ee7f853ba032f0f66169e4bff78181506bf5bc345c9a"
        }
      ]
    },
    {
      "id": "270",
      "version": "codex-cloud-pilot/attempt-02",
      "sourceSha256": "5e07e68eaa870e4ff2cf425597ce3e3af599a136624ec24d5651444528471a5a",
      "frames": [
        {
          "src": "../CODEX-CLOUD-ART-PILOT/frames/directions/attempt-02/270.png",
          "sha256": "cdd2cdaa480cd1cb85771c875d300a913f870887ff34a526ef2a7d7a571dd3c1"
        }
      ]
    }
  ],
  "links": {
    "waiting": [
      {
        "label": "原始 RGBA 条带",
        "src": "../CODEX-CLOUD-ART-PILOT/raw/waiting-attempt-01.png"
      },
      {
        "label": "浅底对比 GIF",
        "src": "../CODEX-CLOUD-ART-PILOT/evidence/waiting-attempt-01-comparison-light.gif"
      },
      {
        "label": "深底对比 GIF",
        "src": "../CODEX-CLOUD-ART-PILOT/evidence/waiting-attempt-01-comparison-dark.gif"
      },
      {
        "label": "明暗底边缘",
        "src": "../CODEX-CLOUD-ART-PILOT/evidence/waiting-attempt-01-edges.png"
      },
      {
        "label": "手部细节",
        "src": "../CODEX-CLOUD-ART-PILOT/evidence/waiting-attempt-01-hands.png"
      }
    ],
    "directions": [
      {
        "label": "原始 RGBA 条带",
        "src": "../CODEX-CLOUD-ART-PILOT/raw/directions-attempt-02.png"
      },
      {
        "label": "明暗底四方向接触表",
        "src": "../CODEX-CLOUD-ART-PILOT/evidence/directions-attempt-02-contact.png"
      },
      {
        "label": "面部、视线与 09 细节",
        "src": "../CODEX-CLOUD-ART-PILOT/evidence/directions-attempt-02-face-and-09.png"
      },
      {
        "label": "首次失败原图",
        "src": "../CODEX-CLOUD-ART-PILOT/raw/directions-attempt-01.png"
      },
      {
        "label": "首次失败检测记录",
        "src": "../CODEX-CLOUD-ART-PILOT/evidence/directions-attempt-01-qa.json"
      }
    ]
  },
  "acceptance": {
    "sha256": "5e7c66e74183beaedb610fa8b789f83bbe8b40163328d5b2589f671f247e907b",
    "payload": {
      "type": "rei-codex-cloud-art-pilot",
      "schema_version": 1,
      "decisions": [
        {
          "id": "waiting",
          "status": "ACCEPTED",
          "comment": "",
          "binding": {
            "candidate": {
              "version": "codex-cloud-pilot/attempt-01",
              "source": "f68e585c5b73214a41d38585aa394d42fcb0961840bbc6e28b33d3024b232b89",
              "frames": [
                "5580b4b1749467f7770e39a5dbe2c9e19100431ee5e6b82a84522b015ccb3f56",
                "03a03495ca1b4d131b03c8e96d4c8e365db2890c48e1c4dbbaba4b02e148af64",
                "71f15dbd0b52d77c8d4a7764638d88449437cee15cb57078e34694645fb59efa",
                "368f644cc9430c464c8548f5c365a5c93095a7acee8a16a7c7f48e17e034ef94",
                "63f782be6f799df94129ccdc7ba2a297f7a3ad61df083940c0f69a6c608c280b",
                "b0dfc778e4e5428001112acb7a08a8e0d7ecd6c3e23b6f10c86714acdf64b2af"
              ]
            },
            "reference": {
              "version": "P4-B/attempt-01",
              "source": "f19efac284e80c3d2ac242fac507b162a8085ecb458e3de5b89345f6a98abcc7",
              "frames": [
                "60fae5f8619315c18c9f885fd9665da64fd29f3dca4c475ea1e57571b84333d6",
                "6f2e3a27e2566324ee3c6930d35c93a9ca6091f28c5d9db39c7f5dbce2f0a3a7",
                "c227245353c2ad84fd31e02a78db393fdef34506911cb47f11d410a5fb35921f",
                "2a28e392ba01d0083a26c8f8901814f8bb8235b76cdfe5c886be9f751378edfe",
                "422030aa32515f677e2b812d353f49ebed0bad4043879d153783a4840f426db0",
                "0e12bc4093cd99c483963999ec5ed2096ebf051aecd28bbe24b83d819f78a371"
              ]
            }
          }
        },
        {
          "id": "000",
          "status": "ACCEPTED",
          "comment": "",
          "binding": {
            "candidate": {
              "version": "codex-cloud-pilot/attempt-02",
              "source": "5e07e68eaa870e4ff2cf425597ce3e3af599a136624ec24d5651444528471a5a",
              "frames": [
                "b315906ecff13dfe97402886a0ee4c86fb340b52903748340e22ef37e384873b"
              ]
            },
            "reference": {
              "version": "P3 派生 RGBA 母版",
              "source": "a19715e0c2e4df83b206f30ee03d6044b0665c911ee85aa31899f118ecad81ce",
              "frames": []
            }
          }
        },
        {
          "id": "090",
          "status": "ACCEPTED",
          "comment": "",
          "binding": {
            "candidate": {
              "version": "codex-cloud-pilot/attempt-02",
              "source": "5e07e68eaa870e4ff2cf425597ce3e3af599a136624ec24d5651444528471a5a",
              "frames": [
                "3d18e479d038ba17a46938a1fc46c059ea0d678f174a520d77be1c7035efcba4"
              ]
            },
            "reference": {
              "version": "P3 派生 RGBA 母版",
              "source": "a19715e0c2e4df83b206f30ee03d6044b0665c911ee85aa31899f118ecad81ce",
              "frames": []
            }
          }
        },
        {
          "id": "180",
          "status": "ACCEPTED",
          "comment": "",
          "binding": {
            "candidate": {
              "version": "codex-cloud-pilot/attempt-02",
              "source": "5e07e68eaa870e4ff2cf425597ce3e3af599a136624ec24d5651444528471a5a",
              "frames": [
                "9c4cc7626c6462eaf723ee7f853ba032f0f66169e4bff78181506bf5bc345c9a"
              ]
            },
            "reference": {
              "version": "P3 派生 RGBA 母版",
              "source": "a19715e0c2e4df83b206f30ee03d6044b0665c911ee85aa31899f118ecad81ce",
              "frames": []
            }
          }
        },
        {
          "id": "270",
          "status": "ACCEPTED",
          "comment": "",
          "binding": {
            "candidate": {
              "version": "codex-cloud-pilot/attempt-02",
              "source": "5e07e68eaa870e4ff2cf425597ce3e3af599a136624ec24d5651444528471a5a",
              "frames": [
                "cdd2cdaa480cd1cb85771c875d300a913f870887ff34a526ef2a7d7a571dd3c1"
              ]
            },
            "reference": {
              "version": "P3 派生 RGBA 母版",
              "source": "a19715e0c2e4df83b206f30ee03d6044b0665c911ee85aa31899f118ecad81ce",
              "frames": []
            }
          }
        }
      ]
    }
  }
};
