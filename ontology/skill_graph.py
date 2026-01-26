import json
from collections import defaultdict
from pathlib import Path


class SkillGraph:
    def __init__(self, ontology_path: Path, aliases_path: Path):
        with open(ontology_path, "r", encoding="utf-8") as f:
            self.graph = json.load(f)

        with open(aliases_path, "r", encoding="utf-8") as f:
            self.aliases = json.load(f)

        self.reverse_graph = self._build_reverse_graph()

    def _build_reverse_graph(self):
        reverse = defaultdict(list)
        for child, parents in self.graph.items():
            for parent in parents:
                reverse[parent].append(child)
        return reverse

    def get_parents(self, skill: str):
        return self.graph.get(skill, [])

    def get_children(self, skill: str):
        return self.reverse_graph.get(skill, [])

    def normalize(self, skill: str) -> str:
        key = skill.lower().strip()
        return self.aliases.get(key, skill)
