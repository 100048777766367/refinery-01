from chamber_cleanroom.decontamination import DecontaminationChamber

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
