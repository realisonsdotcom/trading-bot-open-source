---
domain: 6_quality
title: Risk Checklist
description: Checklist for daily risk metrics and exposure review.
keywords: quality, risk, checklist, notebook
last_updated: 2026-01-06
---

### Métriques analysées

- **Value-at-Risk journalier** avec rééchantillonnage à 95 %.
- **Exposition par classe d'actifs** avec seuils configurables.
- **Stress tests** basés sur les pires sessions historiques agrégées.

### Comment l'utiliser ?

1. Ouvrez le notebook dans `nbviewer` puis exécutez la cellule d'initialisation.
2. Importez vos historiques en CSV ou via l'API `reports-service`.
3. Exportez la synthèse en Markdown pour l'ajouter à la base de connaissances.
