# Contributing Guide

[English](#english-guide) | [Français](#guide-francais)

## 🤖 For AI Agents

If you are a CLI AI agent contributing to this project, you MUST read these documents first:

1. [AGENTS.md](AGENTS.md) - Development contract for AI agents
2. [INDEX.md](INDEX.md) - Main documentation index
3. [docs/DOCUMENTATION-GUIDE-FOR-AGENTS.md](docs/DOCUMENTATION-GUIDE-FOR-AGENTS.md) - Documentation workflow

---

<a id="english-guide"></a>
## English Guide

Thank you for your interest in Trading Bot Open Source! This guide outlines what we expect from contributors so everyone can collaborate effectively.

### 1. Before You Start

- Read the [Code of Conduct](CODE_OF_CONDUCT.md) and agree to follow it.
- Review the existing issues and roadmap in `docs/domains/7_standards/project-evaluation.md` to identify current priorities.
- Open an issue if you want to discuss a new feature or major change before you begin coding.

### 2. Set Up Your Environment

```bash
git clone https://github.com/decarvalhoe/trading-bot-open-source.git
cd trading-bot-open-source
make setup           # install development dependencies
make dev-up          # start PostgreSQL, Redis, and core services
```

Consult the `Makefile` and the `docs/` directory for other useful commands (E2E tests, import scripts, etc.).

### 3. Git Strategy

- Use feature branches: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`.
- Keep `main` stable; use `develop` (if available) for intermediate integrations.
- Rebase regularly on `main` to limit conflicts.

### 4. Code Style and Commits

- Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) convention.
- Formatting and quality are enforced by `black`, `isort`, `flake8`, and strict `mypy`.
- Before pushing, run:

```bash
pre-commit run -a
pytest -q            # add tests when you modify or introduce features
make e2e             # optional but recommended to validate the auth flow
```

Document new commands, environment variables, or schemas in `docs/`.

### 4ter. Documentation Workflow

- Place documentation in `docs/domains/<domain>/` and follow [INDEX.md](INDEX.md).
- Add YAML front matter to every markdown file (see [DOCUMENTATION-GUIDE-FOR-AGENTS.md](docs/DOCUMENTATION-GUIDE-FOR-AGENTS.md)).
- Validate metadata before submitting:

```bash
python3 scripts/validate_docs_metadata.py --strict
```

- (Optional) Regenerate domain indexes:

```bash
# v2: Recursive generation for domains and subdirectories
python3 scripts/generate_index_v2.py

# Legacy v1: Domain-level only
python3 scripts/generate_index.py
```

See [docs/domains/7_standards/generate-index-v2-guide.md](docs/domains/7_standards/generate-index-v2-guide.md) for advanced usage.

- CI validates docs via `.github/workflows/validate-docs.yml`.

### 4bis. Release Process & Changelog

- Quarterly milestones are tracked in [`docs/ROADMAP.md`](docs/ROADMAP.md) and mirrored as GitHub milestones.
- Every release candidate must update [`CHANGELOG.md`](CHANGELOG.md) with features, fixes, and breaking changes.
- Tag releases following semantic versioning (`vX.Y.Z`) and publish the associated notes on GitHub.
- Reference the relevant milestone and changelog entry directly in the pull request description when preparing a release branch.

### 5. Submit a Pull Request

1. Ensure tests pass locally and CI runs cleanly.
2. Fill in the PR description with the motivation, implementation details, and potential impacts.
3. Attach screenshots or relevant logs if your change affects the UI or observability.
4. Mention related issues (`Fixes #123`).
5. Be ready to iterate based on review feedback.

### 6. Code Review

- Maintainers validate technical coherence, security, and documentation.
- Feedback must remain respectful and constructive; feel free to ask for clarifications.
- At least two approvals are recommended for significant changes (services, data schemas, infrastructure).

### 7. Security Review Checklist

Before merging or approving a pull request, ensure that:

- [ ] Secrets and credentials are retrieved via `libs.secrets` (no secrets in git diffs or plaintext `.env`).
- [ ] New environment variables or secret keys are documented in `docs/` or service READMEs.
- [ ] JWT/TOTP changes follow the [rotation guide](docs/domains/4_security/jwt-totp-key-rotation.md).
- [ ] External dependencies introduced are vetted for licenses and minimum versions.
- [ ] Logs or metrics added do not leak sensitive data (PII, secrets, access tokens).

### 8. Non-Code Contributions

Documentation, translations, project management, and testing are equally appreciated. Please surface them via dedicated issues or discussions.

### 9. Retro-Contribution

We encourage sharing tools, patterns, and workflows developed in this project with the broader community. This practice, called **retro-contribution**, helps other projects benefit from our solutions.

**What to Share**:
- Documentation patterns and tools (e.g., `generate_index_v2.py`)
- CI/CD workflows and automation scripts
- Architecture patterns and best practices
- Development tooling and utilities

**How to Share**:
- See [Retro-Contribution Guide](docs/domains/5_community/retro-contribution-guide.md) for complete guidelines
- See [Retro-Contribution Tooling Guide](docs/domains/7_standards/retro-contribution-rbok-tooling.md) for technical details
- Always credit contributors and maintain proper licensing
- Ensure tools are well-documented and tested before sharing

---

<a id="guide-francais"></a>
## Guide français

Merci de votre intérêt pour Trading Bot Open Source ! Ce guide résume les attentes pour contribuer dans les meilleures conditions.

### 1. Avant de commencer

- Lisez le [Code de conduite](CODE_OF_CONDUCT.md) et engagez-vous à le respecter.
- Parcourez les issues existantes et la feuille de route dans `docs/domains/7_standards/project-evaluation.md` pour identifier les priorités actuelles.
- Ouvrez une issue si vous souhaitez discuter d'une nouvelle fonctionnalité ou d'un changement majeur avant de démarrer le développement.

### 2. Préparer votre environnement

```bash
git clone https://github.com/decarvalhoe/trading-bot-open-source.git
cd trading-bot-open-source
make setup           # installe les dépendances de développement
make dev-up          # lance PostgreSQL, Redis et les services principaux
```

Consultez le `Makefile` et le dossier `docs/` pour d'autres commandes utiles (tests E2E, scripts d'import, etc.).

### 3. Stratégie Git

- Branche par fonctionnalité : `feat/<slug>`, `fix/<slug>`, `chore/<slug>`.
- `main` : branche stable ; `develop` (si existante) pour les intégrations intermédiaires.
- Rebasez-vous régulièrement sur `main` pour limiter les conflits.

### 4. Style de code et commits

- Suivez les conventions [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/).
- Le formatage et la qualité sont automatisés via `black`, `isort`, `flake8` et `mypy` (mode strict).
- Avant de pousser, exécutez :

```bash
pre-commit run -a
pytest -q            # ajoutez des tests lorsqu'une fonctionnalité est modifiée ou introduite
make e2e             # optionnel mais recommandé pour valider le parcours auth
```

Documentez les nouvelles commandes, variables d'environnement ou schémas dans `docs/`.

### 4ter. Workflow de documentation

- Placez la documentation dans `docs/domains/<domaine>/` et suivez [INDEX.md](INDEX.md).
- Ajoutez un en-tete YAML a chaque fichier markdown (voir [DOCUMENTATION-GUIDE-FOR-AGENTS.md](docs/DOCUMENTATION-GUIDE-FOR-AGENTS.md)).
- Verifiez les metadonnees avant soumission :

```bash
python3 scripts/validate_docs_metadata.py --strict
```

- (Optionnel) Regenerez les index de domaine :

```bash
python3 scripts/generate_index.py
```

- La CI valide la documentation via `.github/workflows/validate-docs.yml`.

### 4bis. Processus de release & changelog

- Les jalons trimestriels sont décrits dans [`docs/ROADMAP.md`](docs/ROADMAP.md) et synchronisés avec les jalons GitHub.
- Chaque release candidate doit mettre à jour [`CHANGELOG.md`](CHANGELOG.md) avec les fonctionnalités, correctifs et ruptures.
- Tagguez les releases selon le versionnage sémantique (`vX.Y.Z`) et publiez les notes associées sur GitHub.
- Mentionnez le jalon et l'entrée du changelog correspondants dans la description de la pull request lors de la préparation d'une branche de release.

### 5. Soumettre une Pull Request

1. Vérifiez que les tests passent localement et que la CI s'exécute sans erreur.
2. Remplissez la description en expliquant la motivation, l'implémentation et les impacts éventuels.
3. Ajoutez des captures ou extraits de logs pertinents si votre changement touche l'UI ou l'observabilité.
4. Mentionnez les issues liées (`Fixes #123`).
5. Soyez prêt·e à itérer suite aux retours de revue.

### 6. Revue de code

- Les mainteneurs valident la cohérence technique, la sécurité et la documentation.
- Les retours doivent rester respectueux et constructifs ; n'hésitez pas à poser des questions.
- Un minimum de deux approbations est recommandé pour les changements significatifs (services, schémas de données, infrastructure).

### 7. Checklist de revue sécurité

Avant de fusionner ou d'approuver une pull request, vérifiez :

- [ ] Les secrets et identifiants sont récupérés via `libs.secrets` (pas de secret en clair dans Git ou `.env`).
- [ ] Les nouvelles variables d'environnement ou clés secrètes sont documentées dans `docs/` ou les READMEs de service.
- [ ] Les modifications JWT/TOTP respectent le [guide de rotation](docs/domains/4_security/jwt-totp-key-rotation.md).
- [ ] Les dépendances externes ajoutées sont auditées (licence, version minimale, maintenance).
- [ ] Les logs/metrics n'exposent aucune donnée sensible (PII, secrets, tokens).

### 8. Contribution non-code

Les contributions sur la documentation, les traductions, la gestion de projet et les tests sont tout autant appréciées. Signalez-les via des issues dédiées ou des discussions.

### 9. Rétro-contribution

Nous encourageons le partage d'outils, de patterns et de workflows développés dans ce projet avec la communauté open source au sens large. Cette pratique, appelée **rétro-contribution**, aide d'autres projets à bénéficier de nos solutions.

**Quoi partager** :
- Patterns et outils de documentation (ex: `generate_index_v2.py`)
- Workflows CI/CD et scripts d'automatisation
- Patterns d'architecture et bonnes pratiques
- Outils de développement et utilitaires

**Comment partager** :
- Voir [Guide de Rétro-contribution](docs/domains/5_community/retro-contribution-guide.md) pour les lignes directrices complètes
- Voir [Guide Technique de Rétro-contribution](docs/domains/7_standards/retro-contribution-rbok-tooling.md) pour les détails techniques
- Toujours créditer les contributeurs et maintenir les licences appropriées
- S'assurer que les outils sont bien documentés et testés avant de les partager

---

Merci de contribuer à faire de Trading Bot Open Source une plateforme fiable et collaborative !
