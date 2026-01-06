import React from "react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { UserMenu } from "../components/auth/UserMenu.jsx";
import LanguageSwitcher from "../components/LanguageSwitcher.jsx";

const NAV_LINKS = [
  { to: "/dashboard", labelKey: "Tableau de bord" },
  { to: "/trading/orders", labelKey: "Ordres" },
  { to: "/trading/positions", labelKey: "Positions" },
  { to: "/trading/execute", labelKey: "Passer un ordre" },
  { to: "/market", labelKey: "Marché temps réel" },
  { to: "/alerts", labelKey: "Alertes" },
  { to: "/reports", labelKey: "Rapports" },
  { to: "/marketplace", labelKey: "Marketplace" },
  { to: "/dashboard/followers", labelKey: "Suivi copies" },
  { to: "/strategies", labelKey: "Stratégies" },
  { to: "/strategies/designer", labelKey: "Éditeur de stratégies" },
  { to: "/strategies/backtest", labelKey: "Console backtest" },
  { to: "/strategies/ai-assistant", labelKey: "Assistant IA" },
  { to: "/strategies/new", labelKey: "Stratégie express" },
  { to: "/strategies/documentation", labelKey: "Documentation stratégies" },
  { to: "/onboarding", labelKey: "Parcours d'onboarding" },
  { to: "/help", labelKey: "Aide & formation" },
  { to: "/status", labelKey: "Statut services" },
  { to: "/account/settings", labelKey: "Compte & API" },
];

export default function DashboardLayout() {
  const { t } = useTranslation();
  const location = useLocation();

  return (
    <div className="app-shell">
      <aside className="app-sidebar" aria-label={t("Navigation principale")}>
        <div className="app-sidebar__brand">Trading Bot</div>
        <nav className="app-sidebar__nav app-nav">
          {NAV_LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => `app-nav__link${isActive ? " app-nav__link--active" : ""}`}
            >
              {t(link.labelKey)}
            </NavLink>
          ))}
        </nav>
        <LanguageSwitcher />
      </aside>
      <div className="app-content">
        <header className="layout__header">
          <div className="layout__header-meta">
            <UserMenu />
          </div>
        </header>
        <main key={location.pathname} className="layout__main">
          <Outlet />
        </main>
        <footer className="layout__footer">
          <p className="text text--muted">{t("Données d'exemple pour la démonstration du service.")}</p>
        </footer>
      </div>
    </div>
  );
}
