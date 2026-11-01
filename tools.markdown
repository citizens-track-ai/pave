---
layout: default
title: Tools
description: "Explore interactive tools and presentations from the PAVE Case Book, designed to showcase public recommendations and citizen perspectives on AI."
permalink: /tools/
menus: [header]
menu_order: 3
---

<div class="tools-page-wrapper">
  <div class="tools-header-section">
    <h1>Case Book Tools</h1>
    <p class="tools-subtitle">These are useful ways of displaying the case book, developed for the case book presence at the AI for Good Expo.</p>
  </div>

  <div class="tools-grid">
    <!-- Messages Viewer Card -->
    <div class="tool-card">
      <div class="tool-card-icon">
        <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/></svg>
      </div>
      <div class="tool-card-content">
        <h2>Messages Viewer</h2>
        <p>Explore aggregated public voices, values, recommendations, and issues regarding AI governance. Developed to present public inputs dynamically and interactively.</p>
        <div class="tool-card-actions">
          <a href="{{ '/messages/run/' | relative_url }}" class="tool-btn">Run Slide Presentation</a>
        </div>
      </div>
    </div>

    <!-- Videos Card -->
    <div class="tool-card">
      <div class="tool-card-icon">
        <svg viewBox="0 0 24 24"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4zM14 13h-3v3H9v-3H6v-2h3V8h2v3h3v2z"/></svg>
      </div>
      <div class="tool-card-content">
        <h2>Videos Collection</h2>
        <p>Watch video documentation, case-study presentations, and participant interviews captured for the PAVE project and the AI for Good Expo.</p>
        <div class="tool-card-actions">
          <a href="{{ '/videos/' | relative_url }}" class="tool-btn">Browse Videos</a>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
.tools-page-wrapper {
  max-width: 1000px;
  margin: 3rem auto;
  padding: 0 1.5rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.tools-header-section {
  text-align: center;
  margin-bottom: 4rem;
}

.tools-header-section h1 {
  font-size: 2.5rem;
  color: #243f1f;
  margin-bottom: 1rem;
  font-weight: 800;
}

.tools-subtitle {
  font-size: 1.15rem;
  color: #556b2f;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.tools-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }
}

.tool-card {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.12);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  box-shadow: 0 4px 20px rgba(73, 106, 64, 0.04);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.tool-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(73, 106, 64, 0.08);
}

.tool-card-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: rgba(73, 106, 64, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #496a40;
}

.tool-card-icon svg {
  width: 32px;
  height: 32px;
  fill: currentColor;
}

.tool-card-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex-grow: 1;
}

.tool-card-content h2 {
  font-size: 1.5rem;
  color: #243f1f;
  margin: 0;
  font-weight: 700;
}

.tool-card-content p {
  font-size: 0.95rem;
  color: #555555;
  line-height: 1.6;
  margin: 0;
}

.tool-card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: auto;
  padding-top: 1rem;
}

.tool-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none !important;
  background: #496a40 !important;
  color: #ffffff !important;
  transition: background 0.2s ease, transform 0.1s ease;
  border: 1px solid transparent;
}

.tool-btn:hover {
  background: #385331 !important;
  color: #ffffff !important;
}

.tool-btn.btn-secondary {
  background: transparent !important;
  color: #496a40 !important;
  border-color: rgba(73, 106, 64, 0.3) !important;
}

.tool-btn.btn-secondary:hover {
  background: rgba(73, 106, 64, 0.05) !important;
  border-color: #496a40 !important;
  color: #496a40 !important;
}
</style>
