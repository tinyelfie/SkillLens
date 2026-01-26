from collections import defaultdict
from embeddings.domain_embeddings.embedder import embed_text
from matching.ranking_scoring.similarity import cosine_similarity


class SkillInferenceEngine:
    def __init__(self, skill_graph):
        self.skill_graph = skill_graph

    def infer_parent_skills(self, observed_skills, max_depth=2):
        inferred = defaultdict(float)

        for skill in observed_skills:
            skill = self.skill_graph.normalize(skill)
            current_skills = [(skill, 1.0)]

            for _ in range(max_depth):
                next_skills = []
                for s, confidence in current_skills:
                    parents = self.skill_graph.get_parents(s)
                    for parent in parents:
                        new_conf = confidence * 0.7
                        inferred[parent] = max(inferred[parent], new_conf)
                        next_skills.append((parent, new_conf))
                current_skills = next_skills

        return dict(inferred)

    def soft_infer_skills(self, observed_skills, threshold=0.75):
        inferred = {}
        ontology_terms = list(self.skill_graph.graph.keys())

        for skill in observed_skills:
            skill_emb = embed_text(skill)

            for term in ontology_terms:
                term_emb = embed_text(term)
                sim = cosine_similarity(skill_emb, term_emb)

                if sim >= threshold:
                    parents = self.skill_graph.get_parents(term)
                    for parent in parents:
                        inferred[parent] = max(
                            inferred.get(parent, 0.0),
                            round(sim * 0.5, 2)
                        )

        return inferred
