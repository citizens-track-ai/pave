---
layout: default
title: Videos
show_banner: false
permalink: /videos/
menus: []
---

<!-- Import Modern Premium Fonts and Libraries -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>

<div class="video-playlist-layout">
  
  <!-- LEFT SIDEBAR (20% screen width) -->
  <aside class="playlist-sidebar">
    <div class="sidebar-brand">
      <a href="{{ '/' | relative_url }}">
        <img src="{{ '/assets/images/pave-case-book-logo.png' | relative_url }}" alt="PAVE Logo" class="sidebar-logo">
      </a>
      <div class="sidebar-explanation-box">
        <p>See participation and public voice in action: videos from participatory AI projects around the world.</p>
      </div>
    </div>

    <div class="playlist-container">
      <!-- Sidebar Transport Controls -->
      <div class="playlist-header-controls">
        <div class="transport-controls">
          <button id="btn-prev" class="transport-btn" title="Previous">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg>
          </button>
          <button id="btn-play-pause" class="transport-btn transport-btn-main" title="Play">
            <svg id="icon-play" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z"></path>
            </svg>
            <svg id="icon-pause" viewBox="0 0 24 24" fill="currentColor" style="display: none;">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"></path>
            </svg>
          </button>
          <button id="btn-next" class="transport-btn" title="Next">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg>
          </button>
          <button id="btn-shuffle" class="transport-btn" title="Shuffle">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M10.59 9.17L5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41l-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z"/></svg>
          </button>
        </div>
      </div>

      <div class="playlist-tabs">
        <button class="playlist-tab-btn active" id="tab-btn-queue">Play Queue</button>
        <button class="playlist-tab-btn" id="tab-btn-edit">Edit Playlist</button>
      </div>

      <!-- Tab 1: Queue (Case hierarchy) -->
      <div class="tab-pane active" id="pane-queue">
        <div id="playlist-queue-list" class="queue-list">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Tab 2: Edit (Flat sortable list) -->
      <div class="tab-pane" id="pane-edit">
        <div class="playlist-controls">
          <h3 class="controls-title">Playlist Controls</h3>
          <div class="controls-btn-group">
            <button id="playlist-btn-featured" class="control-btn accent">Add Featured</button>
            <button id="playlist-btn-all" class="control-btn secondary">Add All</button>
            <button id="playlist-btn-clear" class="control-btn danger">Clear</button>
          </div>
        </div>
        <div id="playlist-edit-list" class="edit-list">
          <!-- Populated by JS -->
        </div>
      </div>
    </div>
  </aside>

  <!-- RIGHT CONTENT AREA (80% screen width) -->
  <main class="playlist-main-content">
    
    <!-- Top-Right: Embedded Video Player -->
    <section id="player-section" class="player-section" style="display: none;">
      <div class="player-aspect-container">
        <div id="video-player-frame" class="player-iframe-target"></div>
        <button id="btn-close-player" class="close-player-btn" title="Close Player">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </section>

    <!-- Bottom Case Details Footer (Revealed during playback) -->
    <section id="case-details-footer" class="case-details-footer" style="display: none;">
      <div class="case-details-info">
        <div class="case-details-title-row">
          <h2 id="footer-case-title" class="case-details-title"></h2>
        </div>
        <p id="footer-case-desc" class="case-details-desc"></p>
        <div id="footer-case-stats" class="case-details-stats-block"></div>
      </div>
      
      <div class="case-details-widgets">
        <div class="case-details-qr">
          <span class="case-details-qr-label">Scan to View Case</span>
          <div id="footer-qr-code" class="qr-container"></div>
        </div>
        <div class="case-details-map">
          <span class="case-details-map-label">Case Locations</span>
          <div id="footer-mini-map" class="map-container"></div>
        </div>
      </div>
    </section>

    <!-- Available Videos Grid (Featured above Others) -->
    <section class="gallery-grids-section">
      <div class="gallery-section-header">
        <h1 class="browse-title">Browse Project Videos</h1>
      </div>

      <!-- Featured Section -->
      <div class="video-grid-category">
        <h3 class="category-title featured-header">
          <svg viewBox="0 0 24 24" fill="currentColor" class="star-icon">
            <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
          </svg>
          Featured Videos
        </h3>
        <div class="video-grid" id="featured-grid">
          {% for res in site.resources %}
            {% if res.select == "Video" and res.featured-video-resource == true %}
              {% include video_card_template.html res=res %}
            {% endif %}
          {% endfor %}
        </div>
      </div>

      <!-- Others Section -->
      <div class="video-grid-category">
        <h3 class="category-title">Other Videos</h3>
        <div class="video-grid" id="others-grid">
          {% for res in site.resources %}
            {% if res.select == "Video" and res.featured-video-resource != true %}
              {% include video_card_template.html res=res %}
            {% endif %}
          {% endfor %}
        </div>
      </div>
    </section>

  </main>
</div>

<!-- Custom High-Aesthetic Styling (Vanilla CSS) -->
<style>
  /* 1. Immersive full-screen CSS setup */
  .site-header, .site-footer {
    display: none !important;
  }
  .page-content {
    padding: 0 !important;
    margin: 0 !important;
    background: #fcfcf9 !important;
  }
  .page-content .wrapper {
    max-width: none !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  .video-playlist-layout {
    display: flex;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1e293b;
    height: 100vh;
    overflow: hidden;
  }

  /* 2. Left Sidebar Styling */
  .playlist-sidebar {
    width: 20%;
    background: #ffffff;
    border-right: 1px solid rgba(73, 106, 64, 0.12);
    display: flex;
    flex-direction: column;
    height: 100%;
    flex-shrink: 0;
  }

  .sidebar-brand {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(73, 106, 64, 0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  .sidebar-logo {
    height: 38px;
    display: block;
  }

  /* Sidebar Explanation Box */
  .sidebar-explanation-box {
    background: rgba(73, 106, 64, 0.06);
    border: 1px solid rgba(73, 106, 64, 0.15);
    border-radius: 12px;
    padding: 0.85rem;
    font-size: 0.75rem;
    line-height: 1.4;
    color: #243f1f;
    margin-top: 0.75rem;
    text-align: left;
    width: 100%;
  }
  .sidebar-explanation-box p {
    margin: 0;
  }

  /* Transport Control Bar */
  .playlist-header-controls {
    padding: 0.75rem 1.25rem;
    border-bottom: 1px solid rgba(73, 106, 64, 0.08);
    background: rgba(73, 106, 64, 0.01);
  }
  .transport-controls {
    display: flex;
    gap: 0.35rem;
    justify-content: center;
  }
  .transport-btn {
    font-family: inherit;
    border: 1px solid rgba(73, 106, 64, 0.2);
    background: #ffffff;
    color: #496a40;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
    border-radius: 8px;
    transition: all 0.2s ease;
    flex: 1;
  }
  .transport-btn:hover {
    background: rgba(73, 106, 64, 0.06);
    border-color: #496a40;
  }
  .transport-btn svg {
    width: 16px;
    height: 16px;
  }
  .transport-btn-main {
    background: #496a40;
    color: #ffffff;
    border-color: #496a40;
    flex: 1.5;
  }
  .transport-btn-main:hover {
    background: #3c5734;
    border-color: #3c5734;
    color: #ffffff;
  }
  .transport-btn.active {
    background: #496a40;
    color: #ffd700;
    border-color: #496a40;
  }
  .transport-btn.active:hover {
    background: #3c5734;
    border-color: #3c5734;
  }

  .playlist-controls {
    padding: 0 0 1rem 0;
    border-bottom: 1px solid rgba(73, 106, 64, 0.08);
    margin-bottom: 1rem;
  }
  .controls-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #556c50;
    margin: 0 0 0.75rem 0;
  }
  .controls-btn-group {
    display: flex;
    gap: 0.5rem;
  }
  .control-btn {
    flex: 1;
    font-family: inherit;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.5rem 0.25rem;
    border-radius: 6px;
    border: 1px solid rgba(73, 106, 64, 0.15);
    cursor: pointer;
    background: none;
    transition: all 0.2s ease;
  }
  .control-btn.accent {
    background: #496a40;
    color: #ffffff;
    border-color: #496a40;
  }
  .control-btn.accent:hover {
    background: #3c5734;
  }
  .control-btn.secondary {
    background: rgba(73, 106, 64, 0.05);
    color: #496a40;
  }
  .control-btn.secondary:hover {
    background: rgba(73, 106, 64, 0.1);
  }
  .control-btn.danger {
    color: #ef4444;
    border-color: rgba(239, 68, 68, 0.2);
    background: rgba(239, 68, 68, 0.03);
  }
  .control-btn.danger:hover {
    background: rgba(239, 68, 68, 0.08);
    border-color: #ef4444;
  }

  /* Playlist container & tabs */
  .playlist-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .playlist-tabs {
    display: flex;
    border-bottom: 1px solid rgba(73, 106, 64, 0.08);
    background: rgba(73, 106, 64, 0.02);
  }
  .playlist-tab-btn {
    flex: 1;
    background: none;
    border: none;
    padding: 0.9rem 0;
    font-family: inherit;
    font-size: 0.8rem;
    font-weight: 600;
    color: #7a9476;
    cursor: pointer;
    transition: all 0.2s ease;
    border-bottom: 2.5px solid transparent;
  }
  .playlist-tab-btn:hover {
    color: #496a40;
  }
  .playlist-tab-btn.active {
    color: #496a40;
    border-bottom-color: #496a40;
    background: #ffffff;
    font-weight: 700;
  }

  .tab-pane {
    display: none;
    flex: 1;
    overflow-y: auto;
    padding: 1rem 1.25rem;
  }
  .tab-pane.active {
    display: flex;
    flex-direction: column;
  }

  /* Queue tab elements */
  .queue-list {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }
  .queue-case-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    border-left: 2px solid rgba(73, 106, 64, 0.08);
    padding-left: 0.75rem;
    transition: border-color 0.25s ease;
  }
  .queue-case-group.active-case {
    border-left-color: #496a40;
  }
  .queue-case-title {
    font-size: 0.725rem;
    font-weight: 700;
    color: #8c9f88;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    margin: 0;
    transition: color 0.25s ease;
  }
  .queue-case-group.active-case .queue-case-title {
    color: #496a40;
  }
  .queue-video-item {
    font-size: 0.825rem;
    font-weight: 500;
    color: #475569;
    padding: 0.35rem 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .queue-video-item:hover {
    background: rgba(73, 106, 64, 0.04);
    color: #496a40;
  }
  .queue-video-item.active {
    background: rgba(73, 106, 64, 0.08);
    color: #496a40;
    font-weight: 700;
  }

  /* Edit playlist tab */
  .edit-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .playlist-edit-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    background: #ffffff;
    border: 1px solid rgba(73, 106, 64, 0.1);
    border-radius: 6px;
    font-size: 0.8rem;
    cursor: grab;
    transition: all 0.2s ease;
  }
  .playlist-edit-item.dragging {
    opacity: 0.4;
    border-style: dashed;
    background: rgba(73, 106, 64, 0.02);
  }
  .playlist-edit-item.drag-over {
    border-color: #496a40;
    background: rgba(73, 106, 64, 0.04);
  }
  .drag-handle {
    color: #94a3b8;
    cursor: grab;
    font-weight: bold;
    user-select: none;
  }
  .edit-item-info {
    flex: 1;
    overflow: hidden;
  }
  .edit-item-title {
    font-weight: 600;
    color: #334155;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .edit-item-case {
    font-size: 0.675rem;
    color: #64748b;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .btn-remove-item {
    background: none;
    border: none;
    color: #cbd5e1;
    font-size: 1.1rem;
    cursor: pointer;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    transition: all 0.15s ease;
  }
  .btn-remove-item:hover {
    color: #ef4444;
    background: rgba(239, 68, 68, 0.05);
  }

  /* Empty cues */
  .playlist-empty-state {
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    margin-top: 3rem;
  }

  /* 3. Right Content Area Styling */
  .playlist-main-content {
    width: 80%;
    height: 100%;
    overflow-y: auto;
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
  }

  /* Video player wrapper */
  .player-section {
    width: 100%;
  }
  .player-aspect-container {
    position: relative;
    width: 100%;
    padding-top: 56.25%; /* 16:9 Aspect Ratio */
    background: #0f172a;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
  }
  .player-iframe-target {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
    z-index: 1;
  }
  .close-player-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    z-index: 10;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #ffffff;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    transition: all 0.25s ease;
  }
  .player-aspect-container:hover .close-player-btn {
    opacity: 1;
  }
  .close-player-btn:hover {
    background: rgba(15, 23, 42, 0.9);
    border-color: #ffffff;
    transform: scale(1.08);
  }
  .close-player-btn svg {
    width: 18px;
    height: 18px;
  }
  .player-placeholder-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    color: #ffffff;
    padding: 2rem;
    text-align: center;
    z-index: 2;
  }
  .placeholder-icon {
    width: 64px;
    height: 64px;
    color: rgba(73, 106, 64, 0.4);
    margin-bottom: 1rem;
  }
  .placeholder-icon svg {
    width: 100%;
    height: 100%;
  }
  .player-placeholder-overlay h3 {
    font-family: 'Outfit', sans-serif;
    font-size: 1.35rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
  }
  .player-placeholder-overlay p {
    font-size: 0.875rem;
    color: #94a3b8;
    margin: 0;
    max-width: 380px;
  }

  /* 4. Case Details Footer Styling */
  .case-details-footer {
    display: flex;
    background: #ffffff;
    border: 1px solid rgba(73, 106, 64, 0.12);
    border-radius: 16px;
    padding: 1.75rem;
    box-shadow: 0 4px 20px rgba(73, 106, 64, 0.03);
    gap: 2.5rem;
    align-items: stretch;
    width: 95%;
    animation: slideUpFade 0.4s ease forwards;
  }
  @keyframes slideUpFade {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .case-details-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }
  .case-details-title-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }
  .case-details-badge {
    background: rgba(73, 106, 64, 0.08);
    color: #496a40;
    font-size: 0.625rem;
    font-weight: 700;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .case-details-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #1a2f16;
    margin: 0;
  }
  .case-details-desc {
    font-size: 0.85rem;
    line-height: 1.5;
    color: #556c50;
    margin: 0;
  }
  .case-details-stats-block {
    font-size: 0.8rem;
    color: #7a9476;
    line-height: 1.4;
    border-top: 1px dashed rgba(73, 106, 64, 0.12);
    padding-top: 0.65rem;
    margin-top: 0.25rem;
  }
  .stats-light {
    font-weight: 600;
    color: #496a40;
  }

  .case-details-widgets {
    display: flex;
    gap: 1.5rem;
    align-items: center;
  }
  .case-details-qr, .case-details-map {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.4rem;
  }
  .case-details-qr-label, .case-details-map-label {
    font-size: 0.625rem;
    font-weight: 700;
    color: #7a9476;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .case-details-qr {
    flex-shrink: 0;
  }
  #footer-qr-code {
    padding: 0.35rem;
    background: #ffffff;
    border: 1px solid rgba(73, 106, 64, 0.12);
    border-radius: 8px;
    width: 90px;
    height: 90px;
    box-sizing: border-box;
    overflow: hidden;
  }
  #footer-qr-code canvas,
  #footer-qr-code img {
    display: block !important;
    width: 100% !important;
    height: auto !important;
    aspect-ratio: 1 / 1 !important;
    object-fit: contain !important;
  }
  .map-container {
    width: 145px;
    height: 98px;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid rgba(73, 106, 64, 0.15);
    z-index: 5;
  }

  /* 5. Video Grid layout below */
  .gallery-grids-section {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
  }
  .gallery-section-header {
    border-bottom: 2px solid rgba(73, 106, 64, 0.08);
    padding-bottom: 0.75rem;
  }
  .browse-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a2f16;
    margin: 0;
  }
  .video-grid-category {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .category-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #556c50;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .category-title.featured-header {
    color: #d97706; /* Curated amber featured color */
  }
  .star-icon {
    width: 16px;
    height: 16px;
  }

  .video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
    gap: 1.75rem;
  }

  /* Video card styling */
  .video-card {
    background: #ffffff;
    border: 1px solid rgba(73, 106, 64, 0.08);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 12px rgba(73, 106, 64, 0.01);
  }
  .video-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(73, 106, 64, 0.06);
    border-color: rgba(73, 106, 64, 0.15);
  }
  .video-card.featured {
    border: 1.5px solid rgba(217, 119, 6, 0.25);
    box-shadow: 0 4px 15px rgba(217, 119, 6, 0.02);
  }
  .video-card.featured:hover {
    border-color: rgba(217, 119, 6, 0.5);
    box-shadow: 0 8px 28px rgba(217, 119, 6, 0.08);
  }

  .video-cover-wrapper {
    position: relative;
    padding-top: 56.25%;
    overflow: hidden;
  }
  .video-cover-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
  }
  .video-media-target {
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
    transition: transform 0.4s ease;
  }
  .video-card:hover .video-media-target {
    transform: scale(1.03);
  }
  
  .play-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(20, 32, 17, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.25s ease;
  }
  .video-card:hover .play-overlay {
    opacity: 1;
  }

  .play-btn-circle {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.95);
    color: #496a40;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.2s ease;
  }
  .play-btn-circle:hover {
    transform: scale(1.1);
  }
  .play-svg, .external-svg {
    width: 18px;
    height: 18px;
  }

  .video-card-body {
    padding: 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
    flex: 1;
  }
  .case-tag-badge {
    font-size: 0.65rem;
    font-weight: 700;
    color: #7a9476;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }
  .video-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0;
    line-height: 1.35;
  }
  .video-description {
    font-size: 0.775rem;
    line-height: 1.45;
    color: #64748b;
    margin: 0;
  }

  .card-actions-row {
    margin-top: auto;
    display: flex;
    gap: 0.5rem;
    border-top: 1px solid rgba(73, 106, 64, 0.06);
    padding-top: 0.75rem;
  }
  .card-btn {
    flex: 1;
    font-family: inherit;
    font-size: 0.725rem;
    font-weight: 600;
    padding: 0.45rem;
    border-radius: 6px;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.25rem;
  }
  .card-btn.play {
    background: #496a40;
    color: #ffffff;
  }
  .card-btn.play:hover {
    background: #3c5734;
  }
  .card-btn.add {
    background: #ffffff;
    border-color: rgba(73, 106, 64, 0.25);
    color: #496a40;
  }
  .card-btn.add:hover {
    background: rgba(73, 106, 64, 0.05);
  }
  .card-btn svg {
    width: 12px;
    height: 12px;
  }

  /* Tooltip customization */
  .leaflet-tooltip.mini-map-tooltip {
    background: #1a2f16;
    border: 1px solid rgba(73, 106, 64, 0.2);
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  }
  .leaflet-tooltip-top.mini-map-tooltip::before {
    border-top-color: #1a2f16;
  }

  /* Responsive Design Overrides */
  @media (max-width: 768px) {
    /* Hide playlist sidebar completely */
    .playlist-sidebar {
      display: none !important;
    }
    
    /* Expand right content to full-width and let it flow */
    .playlist-main-content {
      width: 100% !important;
      padding: 1rem !important;
      gap: 1.5rem !important;
      height: auto !important;
      overflow-y: visible !important;
      box-sizing: border-box !important;
    }
    
    .video-playlist-layout {
      flex-direction: column !important;
      height: auto !important;
      overflow-y: auto !important;
    }
    
    /* Reformat case details card to hide QR code and map */
    .case-details-footer {
      flex-direction: column !important;
      width: 100% !important;
      padding: 1.25rem !important;
      gap: 1rem !important;
      box-sizing: border-box !important;
    }
    
    .case-details-widgets {
      display: none !important; /* Hide QR code and map on mobile */
    }
    
    .case-details-info {
      width: 100% !important;
    }
    
    /* Ensure gallery grid titles and spacing fit mobile well */
    .gallery-grids-section {
      padding: 0 !important;
    }
    
    .browse-title {
      font-size: 1.5rem !important;
    }
    
    /* Adjust play buttons / aspect wrapper for mobile screens */
    .close-video-btn {
      width: 32px !important;
      height: 32px !important;
      font-size: 1.1rem !important;
    }
  }
</style>

<!-- Playlist behavior scripting -->
<script>
document.addEventListener('DOMContentLoaded', () => {
  // 1. Gather all video cards and construct data array
  const cards = document.querySelectorAll('.video-card');
  const allVideos = Array.from(cards).map(card => {
    let locations = [];
    try {
      locations = JSON.parse(card.dataset.caseLocations || '[]');
    } catch (e) {
      console.error("Error parsing case locations:", e);
    }
    return {
      id: card.dataset.id,
      title: card.dataset.title,
      url: card.dataset.url,
      caseTitle: card.dataset.caseTitle || '',
      caseDesc: card.dataset.caseDesc || '',
      caseUrl: card.dataset.caseUrl || '',
      caseStats: card.dataset.caseStats || '',
      caseLocations: locations,
      isFeatured: card.classList.contains('featured')
    };
  });

  // Extract YouTube ID Helper
  function getYouTubeId(url) {
    if (!url) return null;
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  }

  function isPlayableInline(video) {
    if (!video || !video.url) return false;
    return !!getYouTubeId(video.url);
  }

  // Bind thumbnails images dynamically on cards
  cards.forEach(card => {
    const url = card.dataset.url;
    const mediaTarget = card.querySelector('.video-media-target');
    const playSvg = card.querySelector('.play-svg');
    const externalSvg = card.querySelector('.external-svg');
    const ytId = getYouTubeId(url);

    if (ytId && mediaTarget) {
      mediaTarget.style.backgroundImage = `url('https://img.youtube.com/vi/${ytId}/maxresdefault.jpg')`;
    } else if (mediaTarget) {
      mediaTarget.style.background = 'linear-gradient(135deg, #7a9476 0%, #496a40 100%)';
      if (playSvg) playSvg.style.display = 'none';
      if (externalSvg) externalSvg.style.display = 'block';
    }
  });

  // 2. Playlist State variables
  let playlist = [];
  let currentPlaylistIndex = 0;
  let ytPlayer = null;
  let miniMap = null;
  let markerGroup = null;
  let qrInstance = null;
  let shuffleEnabled = false;

  // DOM Elements
  const queueListEl = document.getElementById('playlist-queue-list');
  const editListEl = document.getElementById('playlist-edit-list');
  const playerFrameEl = document.getElementById('video-player-frame');
  const footerEl = document.getElementById('case-details-footer');
  
  const tabBtnQueue = document.getElementById('tab-btn-queue');
  const tabBtnEdit = document.getElementById('tab-btn-edit');
  const paneQueue = document.getElementById('pane-queue');
  const paneEdit = document.getElementById('pane-edit');

  const btnFeatured = document.getElementById('playlist-btn-featured');
  const btnAll = document.getElementById('playlist-btn-all');
  const btnClear = document.getElementById('playlist-btn-clear');

  const btnPlayPause = document.getElementById('btn-play-pause');
  const iconPlay = document.getElementById('icon-play');
  const iconPause = document.getElementById('icon-pause');
  const btnNext = document.getElementById('btn-next');
  const btnPrev = document.getElementById('btn-prev');
  const btnShuffle = document.getElementById('btn-shuffle');
  const btnClosePlayer = document.getElementById('btn-close-player');

  // Transport button event listeners
  if (btnPlayPause) {
    btnPlayPause.addEventListener('click', () => {
      if (ytPlayer && typeof ytPlayer.getPlayerState === 'function') {
        const state = ytPlayer.getPlayerState();
        if (state === YT.PlayerState.PLAYING) {
          ytPlayer.pauseVideo();
        } else {
          ytPlayer.playVideo();
        }
      } else {
        if (playlist.length > 0) {
          playVideo(currentPlaylistIndex);
        }
      }
    });
  }

  if (btnNext) {
    btnNext.addEventListener('click', () => {
      playNext();
    });
  }

  if (btnPrev) {
    btnPrev.addEventListener('click', () => {
      playPrev();
    });
  }

  if (btnShuffle) {
    btnShuffle.addEventListener('click', () => {
      shuffleEnabled = !shuffleEnabled;
      btnShuffle.classList.toggle('active', shuffleEnabled);
      btnShuffle.title = shuffleEnabled ? 'Shuffle: On' : 'Shuffle: Off';
    });
  }

  if (btnClosePlayer) {
    btnClosePlayer.addEventListener('click', () => {
      if (ytPlayer && typeof ytPlayer.pauseVideo === 'function') {
        ytPlayer.pauseVideo();
      }
      const playerSection = document.getElementById('player-section');
      if (playerSection) {
        playerSection.style.display = 'none';
      }
      if (footerEl) {
        footerEl.style.display = 'none';
      }
    });
  }

  function updatePlayPauseButtonState(state) {
    if (!btnPlayPause) return;
    if (state === 'playing') {
      iconPlay.style.display = 'none';
      iconPause.style.display = 'block';
      btnPlayPause.title = 'Pause';
    } else {
      iconPlay.style.display = 'block';
      iconPause.style.display = 'none';
      btnPlayPause.title = 'Play';
    }
  }

  // 3. Tab Toggling
  tabBtnQueue.addEventListener('click', () => {
    tabBtnQueue.classList.add('active');
    tabBtnEdit.classList.remove('active');
    paneQueue.classList.add('active');
    paneEdit.classList.remove('active');
  });

  tabBtnEdit.addEventListener('click', () => {
    tabBtnEdit.classList.add('active');
    tabBtnQueue.classList.remove('active');
    paneEdit.classList.add('active');
    paneQueue.classList.remove('active');
  });

  // 4. Initialise Mini Map
  function initMiniMap() {
    const mapContainer = document.getElementById('footer-mini-map');
    if (!mapContainer || miniMap) return;

    miniMap = L.map('footer-mini-map', {
      zoomControl: false,
      attributionControl: false,
      dragging: false,
      scrollWheelZoom: false,
      doubleClickZoom: false,
      boxZoom: false
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(miniMap);

    markerGroup = L.layerGroup().addTo(miniMap);
  }

  // 5. Update Metadata Footer
  function updateMetadataFooter(video) {
    if (!video || !video.caseTitle) {
      footerEl.style.display = 'none';
      return;
    }

    footerEl.style.display = 'flex';

    // Update Text Elements
    document.getElementById('footer-case-title').textContent = video.caseTitle;
    document.getElementById('footer-case-desc').textContent = video.caseDesc;

    const statsBlock = document.getElementById('footer-case-stats');
    if (statsBlock) {
      statsBlock.innerHTML = video.caseStats;
    }

    // Update QR Code
    const qrContainer = document.getElementById('footer-qr-code');
    if (qrContainer && video.caseUrl) {
      qrContainer.innerHTML = '';
      qrInstance = new QRCode(qrContainer, {
        text: video.caseUrl,
        width: 80,
        height: 80,
        colorDark: '#1a2f16',
        colorLight: 'rgba(0,0,0,0)',
        correctLevel: QRCode.CorrectLevel.L
      });
    }

    // Update Map
    if (miniMap && markerGroup) {
      markerGroup.clearLayers();
      miniMap.invalidateSize();
      
      const locations = video.caseLocations;
      if (locations && locations.length > 0) {
        let bounds = [];
        locations.forEach(loc => {
          if (loc.lat && loc.lng) {
            const marker = L.circleMarker([loc.lat, loc.lng], {
              color: '#496a40',
              fillColor: '#ffd700',
              fillOpacity: 0.9,
              radius: 5,
              weight: 1.5
            });
            marker.bindTooltip(loc.name, {
              className: 'mini-map-tooltip',
              direction: 'top'
            });
            markerGroup.addLayer(marker);
            bounds.push([loc.lat, loc.lng]);
          }
        });
        
        if (bounds.length > 0) {
          miniMap.fitBounds(bounds, { padding: [10, 10], maxZoom: 10 });
        } else {
          miniMap.setView([20, 0], 1);
        }
      } else {
        miniMap.setView([20, 0], 1);
      }
    }
  }

  // 6. Playback Engine
  function playVideo(index) {
    if (playlist.length === 0) return;
    
    // Show player section
    const playerSection = document.getElementById('player-section');
    if (playerSection) {
      playerSection.style.display = 'block';
    }
    
    // Smooth scroll the content area to the top where the video player is
    const mainContent = document.querySelector('.playlist-main-content');
    if (mainContent) {
      mainContent.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Bounds check
    if (index < 0 || index >= playlist.length) {
      index = 0;
    }
    
    currentPlaylistIndex = index;
    const video = playlist[currentPlaylistIndex];
    const ytId = getYouTubeId(video.url);

    if (ytId) {
      if (btnPlayPause) {
        iconPlay.style.display = 'block';
        iconPause.style.display = 'none';
        btnPlayPause.title = 'Play';
      }

      // If player is not initialized yet
      if (!ytPlayer) {
        // Load YouTube API
        if (typeof YT === 'undefined' || typeof YT.Player === 'undefined') {
          window.onYouTubeIframeAPIReady = () => {
            createYTPlayer(ytId);
          };
          const tag = document.createElement('script');
          tag.src = "https://www.youtube.com/iframe_api";
          const firstScriptTag = document.getElementsByTagName('script')[0];
          firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        } else {
          createYTPlayer(ytId);
        }
      } else {
        ytPlayer.loadVideoById(ytId);
      }
    } else {
      if (btnPlayPause) {
        iconPlay.style.display = 'block';
        iconPause.style.display = 'none';
        btnPlayPause.title = 'Play';
      }

      // Non-YouTube External Links: display outbound panel in player aspect frame
      if (ytPlayer) {
        try { ytPlayer.destroy(); } catch (e) {}
        ytPlayer = null;
      }
      playerFrameEl.innerHTML = `
        <div class="player-placeholder-overlay" style="z-index: 3;">
          <div class="placeholder-icon" style="color: #ffd700;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </div>
          <h3>Outbound Video Link</h3>
          <p class="mb-3">${video.title}</p>
          <a href="${video.url}" target="_blank" class="control-btn accent" style="text-decoration: none; padding: 0.5rem 1.5rem; display: inline-block; width: auto;">Open Video Website</a>
          <button id="btn-skip-external" class="control-btn secondary" style="margin-top: 1rem; width: auto;">Skip to Next Video</button>
        </div>
      `;
      document.getElementById('btn-skip-external').addEventListener('click', playNext);
    }

    // Update layout highlights
    highlightPlayingVideo();

    // Update map & QR code footer
    initMiniMap();
    updateMetadataFooter(video);
  }

  function createYTPlayer(videoId) {
    ytPlayer = new YT.Player('video-player-frame', {
      videoId: videoId,
      playerVars: {
        autoplay: 1,
        rel: 0,
        modestbranding: 1,
        enablejsapi: 1
      },
      events: {
        'onStateChange': onPlayerStateChange,
        'onError': (e) => {
          console.error("YouTube Player error:", e);
          playNext();
        }
      }
    });
  }

  function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.ENDED) {
      playNext();
    } else if (event.data === YT.PlayerState.PLAYING) {
      updatePlayPauseButtonState('playing');
    } else if (event.data === YT.PlayerState.PAUSED) {
      updatePlayPauseButtonState('paused');
    }
  }

  function playNext() {
    if (playlist.length === 0) return;

    // Check if there is any playable video in the playlist to avoid infinite loops
    const hasPlayable = playlist.some(v => isPlayableInline(v));
    if (!hasPlayable) return;

    let targetIndex = currentPlaylistIndex;
    if (shuffleEnabled) {
      let rand;
      do {
        rand = Math.floor(Math.random() * playlist.length);
      } while ((rand === currentPlaylistIndex || !isPlayableInline(playlist[rand])) && playlist.length > 1);
      targetIndex = rand;
    } else {
      let found = false;
      let idx = currentPlaylistIndex;
      for (let i = 1; i <= playlist.length; i++) {
        let nextIdx = (idx + i) % playlist.length;
        if (isPlayableInline(playlist[nextIdx])) {
          targetIndex = nextIdx;
          found = true;
          break;
        }
      }
      if (!found) return;
    }
    playVideo(targetIndex);
  }

  function playPrev() {
    if (playlist.length === 0) return;

    const hasPlayable = playlist.some(v => isPlayableInline(v));
    if (!hasPlayable) return;

    let targetIndex = currentPlaylistIndex;
    if (shuffleEnabled) {
      let rand;
      do {
        rand = Math.floor(Math.random() * playlist.length);
      } while ((rand === currentPlaylistIndex || !isPlayableInline(playlist[rand])) && playlist.length > 1);
      targetIndex = rand;
    } else {
      let found = false;
      let idx = currentPlaylistIndex;
      for (let i = 1; i <= playlist.length; i++) {
        let prevIdx = (idx - i + playlist.length) % playlist.length;
        if (isPlayableInline(playlist[prevIdx])) {
          targetIndex = prevIdx;
          found = true;
          break;
        }
      }
      if (!found) return;
    }
    playVideo(targetIndex);
  }

  // 7. Playlist Rendering Functions
  function renderPlaylist() {
    renderQueueTab();
    renderEditTab();
  }

  // Tab 1: Render Queue Tab (Grouped by Case Study)
  function renderQueueTab() {
    queueListEl.innerHTML = '';
    if (playlist.length === 0) {
      queueListEl.innerHTML = '<div class="playlist-empty-state">No videos in playlist</div>';
      return;
    }

    // Group active playlist videos by Case Title
    const groups = {};
    const groupOrder = [];

    playlist.forEach((video, index) => {
      const caseName = video.caseTitle || "Other Videos";
      if (!groups[caseName]) {
        groups[caseName] = [];
        groupOrder.push(caseName);
      }
      groups[caseName].push({ video, index });
    });

    const activeVideo = playlist[currentPlaylistIndex];
    const activeCaseName = activeVideo ? (activeVideo.caseTitle || "Other Videos") : null;

    groupOrder.forEach(caseName => {
      const caseGroupDiv = document.createElement('div');
      caseGroupDiv.className = 'queue-case-group';
      if (caseName === activeCaseName) {
        caseGroupDiv.classList.add('active-case');
      }

      const caseH = document.createElement('h4');
      caseH.className = 'queue-case-title';
      caseH.textContent = caseName;
      caseGroupDiv.appendChild(caseH);

      groups[caseName].forEach(item => {
        const videoLink = document.createElement('div');
        videoLink.className = 'queue-video-item';
        if (item.index === currentPlaylistIndex) {
          videoLink.classList.add('active');
        }
        videoLink.textContent = item.video.title;
        videoLink.title = item.video.title;

        // Click plays immediately
        videoLink.addEventListener('click', () => {
          playVideo(item.index);
        });

        caseGroupDiv.appendChild(videoLink);
      });

      queueListEl.appendChild(caseGroupDiv);
    });
  }

  // Tab 2: Render Edit Tab (Flat list with Drag & Drop)
  function renderEditTab() {
    editListEl.innerHTML = '';
    if (playlist.length === 0) {
      editListEl.innerHTML = '<div class="playlist-empty-state">No videos in playlist</div>';
      return;
    }

    playlist.forEach((video, index) => {
      const editItem = document.createElement('div');
      editItem.className = 'playlist-edit-item';
      editItem.setAttribute('draggable', 'true');
      editItem.dataset.index = index;

      editItem.innerHTML = `
        <span class="drag-handle">:::</span>
        <div class="edit-item-info">
          <div class="edit-item-title" title="${video.title}">${video.title}</div>
          <div class="edit-item-case" title="${video.caseTitle || 'Project Video'}">${video.caseTitle || 'Project Video'}</div>
        </div>
        <button class="btn-remove-item" title="Remove video">&times;</button>
      `;

      // Drag & Drop Bindings
      editItem.addEventListener('dragstart', handleDragStart);
      editItem.addEventListener('dragover', handleDragOver);
      editItem.addEventListener('dragenter', handleDragEnter);
      editItem.addEventListener('dragleave', handleDragLeave);
      editItem.addEventListener('drop', handleDrop);
      editItem.addEventListener('dragend', handleDragEnd);

      // Remove Click
      editItem.querySelector('.btn-remove-item').addEventListener('click', (e) => {
        e.stopPropagation();
        removeVideo(index);
      });

      editListEl.appendChild(editItem);
    });
  }

  function highlightPlayingVideo() {
    // 1. Highlight in Queue View
    const queueLinks = queueListEl.querySelectorAll('.queue-video-item');
    queueLinks.forEach((link, idx) => {
      link.classList.remove('active');
    });
    const queueGroups = queueListEl.querySelectorAll('.queue-case-group');
    queueGroups.forEach(group => {
      group.classList.remove('active-case');
    });

    const activeVideo = playlist[currentPlaylistIndex];
    if (activeVideo) {
      // Re-render Queue is safest to update parent case active markers
      renderQueueTab();
    }

    // 2. Highlight in Edit View (no special highlight needed but ensures sync)
    const editItems = editListEl.querySelectorAll('.playlist-edit-item');
    editItems.forEach((item, idx) => {
      if (idx === currentPlaylistIndex) {
        item.style.borderColor = '#496a40';
        item.style.background = 'rgba(73, 106, 64, 0.03)';
      } else {
        item.style.borderColor = '';
        item.style.background = '';
      }
    });
  }

  // 8. Playlist Mutation Functions
  function removeVideo(index) {
    if (index < 0 || index >= playlist.length) return;
    
    playlist.splice(index, 1);
    
    // Adjust current index
    if (currentPlaylistIndex === index) {
      // If we removed currently playing, load the same index (which is now the next item)
      if (playlist.length > 0) {
        playVideo(currentPlaylistIndex);
      } else {
        // Queue is empty
        clearPlayer();
      }
    } else if (currentPlaylistIndex > index) {
      currentPlaylistIndex--;
      highlightPlayingVideo();
    } else {
      highlightPlayingVideo();
    }
    
    renderPlaylist();
  }

  function clearPlayer() {
    playlist = [];
    currentPlaylistIndex = 0;
    
    if (ytPlayer) {
      try { ytPlayer.destroy(); } catch (e) {}
      ytPlayer = null;
    }
    playerFrameEl.innerHTML = '';
    
    // Hide player section
    const playerSection = document.getElementById('player-section');
    if (playerSection) {
      playerSection.style.display = 'none';
    }

    footerEl.style.display = 'none';

    if (btnPlayPause) {
      iconPlay.style.display = 'block';
      iconPause.style.display = 'none';
      btnPlayPause.title = 'Play';
    }

    renderPlaylist();
  }

  // 9. HTML5 Drag & Drop Logic
  let dragSrcEl = null;

  function handleDragStart(e) {
    dragSrcEl = this;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', this.dataset.index);
    this.classList.add('dragging');
  }

  function handleDragOver(e) {
    if (e.preventDefault) {
      e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    return false;
  }

  function handleDragEnter(e) {
    this.classList.add('drag-over');
  }

  function handleDragEnd(e) {
    this.classList.remove('dragging');
    const items = editListEl.querySelectorAll('.playlist-edit-item');
    items.forEach(item => {
      item.classList.remove('drag-over');
    });
  }

  function handleDragLeave(e) {
    this.classList.remove('drag-over');
  }

  function handleDrop(e) {
    if (e.stopPropagation) {
      e.stopPropagation();
    }
    
    const srcIndex = parseInt(e.dataTransfer.getData('text/plain'));
    const destIndex = parseInt(this.dataset.index);

    if (srcIndex !== destIndex && !isNaN(srcIndex) && !isNaN(destIndex)) {
      // Reorder array
      const movedItem = playlist.splice(srcIndex, 1)[0];
      playlist.splice(destIndex, 0, movedItem);

      // Adjust currently playing index
      if (currentPlaylistIndex === srcIndex) {
        currentPlaylistIndex = destIndex;
      } else if (currentPlaylistIndex > srcIndex && currentPlaylistIndex <= destIndex) {
        currentPlaylistIndex--;
      } else if (currentPlaylistIndex < srcIndex && currentPlaylistIndex >= destIndex) {
        currentPlaylistIndex++;
      }

      renderPlaylist();
      highlightPlayingVideo();
    }
    return false;
  }

  // 10. Available Grid Bindings
  cards.forEach((card, idx) => {
    const videoObj = allVideos[idx];

    // Card Actions
    const btnPlay = card.querySelector('.card-btn.play');
    const btnAdd = card.querySelector('.card-btn.add');
    const coverClick = card.querySelector('.video-cover-container');

    // Helper: Add and play immediately
    const handleImmediatePlay = () => {
      // Check if already in playlist
      let existingIndex = playlist.findIndex(v => v.id === videoObj.id);
      if (existingIndex === -1) {
        playlist.splice(currentPlaylistIndex + 1, 0, videoObj);
        existingIndex = currentPlaylistIndex + 1;
        renderPlaylist();
      }
      playVideo(existingIndex);
    };

    // Helper: Add to playlist end
    const handleAddToPlaylist = (e) => {
      if (e) e.stopPropagation();
      let existingIndex = playlist.findIndex(v => v.id === videoObj.id);
      if (existingIndex === -1) {
        playlist.push(videoObj);
        renderPlaylist();
        
        // Visual feedback
        const originalText = btnAdd.innerHTML;
        btnAdd.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          Added
        `;
        setTimeout(() => {
          btnAdd.innerHTML = originalText;
        }, 1200);
      }
    };

    if (btnPlay) btnPlay.addEventListener('click', handleImmediatePlay);
    if (coverClick) coverClick.addEventListener('click', handleImmediatePlay);
    if (btnAdd) btnAdd.addEventListener('click', handleAddToPlaylist);
  });

  // 11. Playlist Global Buttons
  btnFeatured.addEventListener('click', () => {
    // Add all featured to playlist
    const featured = allVideos.filter(v => v.isFeatured);
    featured.forEach(v => {
      if (!playlist.some(p => p.id === v.id)) {
        playlist.push(v);
      }
    });
    renderPlaylist();
    if (playlist.length > 0 && document.getElementById('player-section').style.display === 'none') {
      playVideo(0);
    }
  });

  btnAll.addEventListener('click', () => {
    // Add all videos to playlist
    allVideos.forEach(v => {
      if (!playlist.some(p => p.id === v.id)) {
        playlist.push(v);
      }
    });
    renderPlaylist();
    if (playlist.length > 0 && document.getElementById('player-section').style.display === 'none') {
      playVideo(0);
    }
  });

  btnClear.addEventListener('click', clearPlayer);

  // 12. Page Load Initialization
  // Load featured videos by default
  const defaultFeatured = allVideos.filter(v => v.isFeatured);
  if (defaultFeatured.length > 0) {
    playlist = [...defaultFeatured];
    renderPlaylist();
  } else if (allVideos.length > 0) {
    playlist = [allVideos[0]];
    renderPlaylist();
  }
});
</script>
