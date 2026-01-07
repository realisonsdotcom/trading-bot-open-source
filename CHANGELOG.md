# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et ce projet adhère au versionnage sémantique.

## [Unreleased]
### Ajouté
- Script `generate_index_v2.py` pour génération récursive d'INDEX.md avec support Jinja2 (#52)
- Template Jinja2 pour personnalisation des index (`docs/templates/index-template.md.j2`)
- Guide d'utilisation complet pour `generate_index_v2.py` (`docs/GENERATE_INDEX_V2_GUIDE.md`)
- Tests unitaires pour le générateur d'index v2 (`tests/test_generate_index_v2.py`)
- Support de la génération d'index pour sous-domaines et répertoires imbriqués
- Panorama fonctionnel par domaine (stratégies, trading temps réel, reporting, notifications, marketplace) dans les README EN/FR.
- Documentation de statut et prérequis pour le Strategy Designer, l'assistant IA, les backtests et la stack streaming.
- Hub de tutoriels (`docs/domains/6_quality/tutorials/`) incluant notebook backtest et références vidéos.
- Journal de validation inter-services (`docs/domains/5_community/governance/release-approvals/2025-12.md`) et communication interne associée.
- Mise à jour du changelog synthétique et des guides service-specific (algo-engine, marketplace, market-data, inplay, notifications, streaming).

### Modifié
- Alignement du calendrier de releases avec des jalons trimestriels (clarifié dans `docs/domains/5_community/release-highlights/2025-12.md`).
- Documentation communautaire couvrant les rituels AMA et live coding.
- CONTRIBUTING.md avec référence au nouveau générateur d'index v2

## [0.2.0] - 2023-12-15
### Ajouté
- Intégration des premiers connecteurs de marché crypto.
- Documentation initiale sur les services de données et d'exécution.

## [0.1.0] - 2023-09-01
### Ajouté
- Publication initiale du bot de trading open-source.
- Mise en place de l'infrastructure de tests et des workflows CI.

[Unreleased]: https://github.com/your-org/trading-bot-open-source/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/your-org/trading-bot-open-source/releases/tag/v0.2.0
[0.1.0]: https://github.com/your-org/trading-bot-open-source/releases/tag/v0.1.0
