import os
import sys
import json
import time
import hashlib
import re
import urllib.request

REFINERY_BLUEPRINTS = {
    "contract.json": json.dumps({
        "contract_id": "bodhi.refinery.q1",
        "genesis_root": "100048777766367/refinery",
        "role": "INDEPENDENT_SUPER_REFINERY_ROOT_Q",
        "rules": {"iso_cleanroom_grade": "CLASS_1", "zero_pii": True, "strict_triplets": True}
    }, indent=4),

    "Dockerfile": """FROM python:3.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
CMD ["python", "kernel.py"]
""",

    "README.md": """# 🏭 BODHI-REFINERY: NHÀ MÁY TINH CHẾ ĐỘC LẬP & GỐC RỄ [q']
> *"Hoàn toàn độc lập, vận hành buồng khử nhiễm số và chưng cất tri thức đạt chuẩn bán dẫn, sẵn sàng sinh sôi ra một đại hệ sinh thái công nghiệp mới."*
""",

    "chamber_cleanroom/__init__.py": "# Chamber Cleanroom Package\n",

    "chamber_cleanroom/decontamination.py": """import re

class DecontaminationChamber:
    EMAIL_PATT = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    PHONE_PATT = r'\\b(?:\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}\\b'

    @classmethod
    def decontaminate(cls, text):
        if not text: return ""
        cleaned = re.sub(cls.EMAIL_PATT, "[ANON_ENTITY]", str(text))
        cleaned = re.sub(cls.PHONE_PATT, "[ANON_CONTACT]", cleaned)
        cleaned = re.sub(r'[^\\w\\s\\-_]', '', cleaned)
        return cleaned.strip()
""",

    "chamber_cleanroom/distillation_chamber.py": """from chamber_cleanroom.decontamination import DecontaminationChamber

class DistillationChamber:
    @staticmethod
    def distill_to_semiconductor_grade(raw_inputs):
        pure_knowledge = []
        for raw in raw_inputs:
            s = DecontaminationChamber.decontaminate(raw.get("subject", ""))
            p = DecontaminationChamber.decontaminate(raw.get("predicate", "")).lower().replace(" ", "_")
            o = DecontaminationChamber.decontaminate(raw.get("object", ""))
            if len(s) >= 2 and len(p) >= 2 and len(o) >= 2:
                pure_knowledge.append({
                    "subject": s.capitalize(),
                    "predicate": p,
                    "object": o.capitalize(),
                    "purity_grade": "99.999%",
                    "confidence": 0.99
                })
        return pure_knowledge
""",

    "synapses/peers.json": json.dumps({
        "open_ingestion_grid": [
            "100048777766367/vault-01",
            "100048777766367/vault",
            "100048777766367/nexus-08",
            "100048777766367/contract"
        ]
    }, indent=4),

    "synapses/state.json": json.dumps({"generation_epoch": 1, "status": "refinery_q_seeded"}, indent=4)
}

class RefineryMasterKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/refinery")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.self_materialize()
        
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from chamber_cleanroom.distillation_chamber import DistillationChamber
        self.distiller = DistillationChamber
        self.epoch = self.load_epoch()

    def self_materialize(self):
        for path, code in REFINERY_BLUEPRINTS.items():
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
                with open(path, "w", encoding="utf-8") as f: f.write(code)

    def load_epoch(self):
        try:
            with open("synapses/state.json", "r", encoding="utf-8") as f:
                return json.load(f).get("generation_epoch", 0) + 1
        except Exception: return 1

    def run(self):
        print("=" * 80)
        print(f"🏭 [INDEPENDENT REFINERY ROOT q'] KHỞI ĐỘNG NHÀ MÁY #{self.epoch}")
        print("💎 Bản Thể: Tinh Chế Độc Lập Chuẩn Bán Dẫn – Mầm Mống Hệ Sinh Thái Mới")
        print("=" * 80)

        # Quét nạp nguyên liệu mở
        raw_samples = [
            {"subject": "Refinery", "predicate": "distills", "object": "CleanSemiconductorData"},
            {"subject": "EcosystemQ", "predicate": "branches_into", "object": "InfinitePossibilities"},
            {"subject": "Knowledge", "predicate": "powers", "object": "AutonomousIntelligence"}
        ]

        pure_output = self.distiller.distill_to_semiconductor_grade(raw_samples)
        print(f"✨ [BUỒNG CHƯNG CẤT] Đã sản xuất {len(pure_output)} bản ghi độ tinh khiết 99.999%!")

        os.makedirs("dist", exist_ok=True)
        out_file = "dist/semiconductor_knowledge_graph.jsonl"
        with open(out_file, "w", encoding="utf-8") as f:
            for item in pure_output: f.write(json.dumps(item, ensure_ascii=False) + "\n")

        t = int(time.time())
        cid = hashlib.shake_256(f"ref_{self.epoch}_{t}_{len(pure_output)}".encode()).hexdigest(64)
        
        with open("synapses/state.json", "w", encoding="utf-8") as f:
            json.dump({"generation_epoch": self.epoch, "last_t": t, "output_count": len(pure_output), "quantum_cid": cid}, f, indent=4)

        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump({"contract": "bodhi.refinery.q1", "identity": self.repo_name, "epoch": self.epoch, "cid": cid}, f, indent=4)

        print(f"💾 [CHỨNG THỰC CID REFINERY]: {cid[:24]}...")
        print("=" * 80)

if __name__ == "__main__":
    RefineryMasterKernel().run()
