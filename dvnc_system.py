# dvnc_system.py
import random
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class FineTunedSLM:
    domain: str
    knowledge: Dict[str, str]
    temperature: float = 0.6
    system_prompt: str = field(init=False)

    def __post_init__(self):
        self.system_prompt = (
            f"You are a specialized SLM for {self.domain}. "
            f"Use concise, actionable language. Cite a Da Vinci study when relevant. "
            f"Prefer design heuristics and constraints over vague generalities."
        )

    def generate_insight(self, prompt_keywords: List[str], user_prompt: str) -> str:
        if not prompt_keywords:
            concept = random.choice(list(self.knowledge.keys()))
        else:
            chosen_kw = random.choice(prompt_keywords) if prompt_keywords else ""
            concept = None
            for k in self.knowledge.keys():
                if chosen_kw.lower() in k.lower():
                    concept = k
                    break
            if not concept:
                concept = random.choice(list(self.knowledge.keys()))
        
        study = self.knowledge[concept]
        return (
            f"**{concept}** (Da Vinci's *{study}*): "
            f"Define constraints, objectives, and validation metrics."
        )

class DVNCSystem:
    def __init__(self):
        self.physics_knowledge = {
            "Fluid Dynamics": "water screws and canal studies",
            "Aerodynamics": "ornithopter sketches and airflow notes",
            "Lever Mechanics": "gear trains, pulleys, cranes",
            "Structural Integrity": "bridges and fortification stress studies",
        }
        self.biomech_knowledge = {
            "Joint Articulation": "elbow/shoulder motion notebooks",
            "Muscular Force": "layered muscle drawings",
            "Biological Levers": "limb lever ratios and gait notes",
            "Skeletal Structure": "Vitruvian proportions and load paths",
        }
        self.anatomy_knowledge = {
            "Human Proportionality": "Vitruvian Man proportional canon",
            "Muscular Systems": "detailed musculature sheets",
            "Circulatory System": "venous and arterial mapping",
            "Body Mechanics": "posture, stance, and motion sequences",
        }
        
        self.models = {
            "Physics": FineTunedSLM("Physics", self.physics_knowledge),
            "Biomechanics": FineTunedSLM("Biomechanics", self.biomech_knowledge),
            "Anatomy": FineTunedSLM("Anatomy", self.anatomy_knowledge)
        }

    def analyze_prompt(self, prompt: str) -> Dict:
        """Analyze user prompt and generate insights"""
        keywords = self.extract_keywords(prompt)
        insights = self.generate_insights(prompt, keywords)
        synthesis = self.synthesize_design(prompt, insights)
        
        return {
            'keywords': keywords,
            'insights': insights,
            'synthesis': synthesis
        }

    def extract_keywords(self, prompt: str) -> Dict[str, List[str]]:
        prompt_low = prompt.lower()
        result = {}
        for domain, model in self.models.items():
            kws = []
            for concept in model.knowledge.keys():
                parts = concept.lower().replace("-", " ").split()
                if any(p in prompt_low for p in parts):
                    kws.append(concept)
            result[domain] = list(set(kws))
        return result

    def generate_insights(self, prompt: str, keywords: Dict[str, List[str]]) -> Dict[str, str]:
        insights = {}
        for domain, model in self.models.items():
            insights[domain] = model.generate_insight(keywords.get(domain, []), prompt)
        return insights

    def synthesize_design(self, prompt: str, insights: Dict[str, str]) -> str:
        lines = [
            f"## 🎨 Da Vinci-Inspired Innovation Synthesis\n",
            f"**Challenge:** {prompt}\n",
            "### 📊 Multidisciplinary Insights\n",
        ]
        
        for domain, insight in insights.items():
            emoji = {"Physics": "⚙️", "Biomechanics": "🦾", "Anatomy": "🧬"}.get(domain, "🔬")
            lines.append(f"{emoji} **{domain}**: {insight}\n")
        
        lines.extend([
            "\n### 🚀 Integrated Design Concept\n",
            "- **Architecture**: Bio-inspired modular framework with adaptive joints",
            "- **Mechanics**: Leverage ratios optimized from natural systems",
            "- **Validation**: Multi-domain KPIs aligned with Da Vinci's principles",
            "\n### 📋 Next Steps",
            "1. Transform constraints into parametric design variables",
            "2. Build rapid prototypes for cross-domain validation",
            "3. Iterate using Leonardo's observation-experimentation cycle"
        ])
        
        return "\n".join(lines)