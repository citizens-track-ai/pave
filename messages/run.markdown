---
layout: default
title: Messages Presentation
permalink: /messages/run/
show_banner: false
sitemap: false
leaflet: true
qrcode: true
---

<style>
  :root {
    --banner-height: 10vh;
  }

  /* 1. Hide default Jekyll theme header & footer on slideshow page for immersive view */
  .site-header, .site-footer {
    display: none !important;
  }
  .page-content {
    padding: 0 !important;
    margin: 0 !important;
    background: #496a40 !important;
  }
  .page-content .wrapper {
    max-width: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  body {
    overflow: hidden !important;
    background-color: #496a40 !important;
    margin: 0 !important;
  }

  /* 2. Slideshow Layout */
  .slideshow-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    color: #ffffff;
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: linear-gradient(135deg, #496a40 0%, #375030 100%);
  }

  /* Header Banner Layout */
  .header-banner {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 10vh;
    min-height: 10vh;
    background: rgba(10, 16, 8, 0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    padding: 0.5rem 2rem;
    box-sizing: border-box;
    z-index: 110;
    pointer-events: auto;
  }

  .header-left {
    justify-self: start;
    display: flex;
    align-items: center;
  }

  .header-right {
    justify-self: end;
    display: flex;
    align-items: center;
  }

  .header-banner-text {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(1.2rem, 3vh, 1.8rem);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #ffffff !important;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.7);
    margin: 0;
    text-align: center;
    justify-self: center;
    line-height: 1.2;
  }

  /* Back Link */
  .back-to-cases {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.5rem 1.25rem;
    border-radius: 9999px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.2s ease;
  }

  .back-to-cases:visited {
    color: #ffffff !important;
  }

  .back-to-cases:hover {
    background: rgba(255, 255, 255, 0.18);
    transform: translateY(-1px);
  }

  .back-to-cases svg {
    transition: transform 0.2s ease;
  }

  .back-to-cases:hover svg {
    transform: translateX(-3px);
  }

  /* Controls Section */
  .right-controls {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.35rem;
  }

  /* Autoplay Capsule */
  .autoplay-capsule {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.45rem 1.25rem;
    border-radius: 9999px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    color: #ffffff;
  }

  .play-pause-btn {
    background: none;
    border: none;
    color: #ffffff;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.2rem;
    transition: transform 0.2s;
  }

  .play-pause-btn:hover {
    transform: scale(1.15);
  }

  .play-pause-btn svg {
    width: 1.15rem;
    height: 1.15rem;
  }

  .speed-select {
    background: transparent;
    border: none;
    color: #ffffff;
    font-family: inherit;
    font-size: 0.8rem;
    font-weight: 600;
    outline: none;
    cursor: pointer;
    padding-right: 1.25rem;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right center;
  }

  .speed-select option {
    background: #375030;
    color: #ffffff;
  }

  .shuffle-btn {
    background: none;
    border: none;
    color: #ffffff;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.2rem;
    transition: all 0.2s;
    opacity: 0.5;
  }

  .shuffle-btn.active {
    opacity: 1;
    color: #ffd700; /* gold highlight color when random is active */
  }

  .shuffle-btn:hover {
    transform: scale(1.15);
  }

  .progress-bar-container {
    width: 80px;
    height: 4px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 2px;
    overflow: hidden;
  }

  .progress-bar-fill {
    height: 100%;
    width: 0%;
    background: #ffffff;
    border-radius: 2px;
  }

  .slide-counter {
    font-family: 'Outfit', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    min-width: 45px;
    text-align: center;
  }

  /* Case Selector Capsule */
  .case-select-capsule {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.45rem 1.25rem;
    border-radius: 9999px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }

  .case-select {
    background: transparent;
    border: none;
    color: #ffffff;
    font-family: inherit;
    font-size: 0.8rem;
    font-weight: 600;
    outline: none;
    cursor: pointer;
    padding-right: 1.5rem;
    max-width: 250px;
    text-overflow: ellipsis;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right center;
  }

  .case-select option {
    background: #375030;
    color: #ffffff;
  }

  /* Static/Fixed Header Info & Logo (Stays static unless changing) */
  .fixed-top-header {
    position: absolute;
    top: calc(3rem + var(--banner-height));
    left: 4.5rem;
    right: 4.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    z-index: 90;
    pointer-events: none;
  }

  .fixed-top-header * {
    pointer-events: auto;
  }

  .slide-case-info {
    max-width: 65%;
    opacity: 1;
    transition: opacity 0.2s ease-in-out;
  }

  .slide-case-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff !important;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.01em;
  }

  .slide-case-subtitle {
    font-size: 0.95rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.85);
    margin: 0;
    line-height: 1.45;
  }

  .slide-pave-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3.5rem;
    height: 3.5rem;
    background: transparent;
  }

  .slide-pave-logo img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  /* Slides Track */
  .slides-track {
    display: flex;
    width: 100%;
    height: 100%;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .slide-item {
    width: 100vw;
    height: 100vh;
    flex-shrink: 0;
    position: relative;
    box-sizing: border-box;
    padding: calc(7.5rem + var(--banner-height)) 4.5rem 5rem 4.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    z-index: 1;
    overflow: hidden;
  }

  /* Fixed Background Layers (sit on container, never move with slides) */
  .bg-layer {
    position: absolute;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    transition: opacity 0.7s ease;
  }

  .bg-layer-halftone {
    position: absolute;
    bottom: -60vw;
    right: -60vw;
    top: auto;
    left: auto;
    width: 100vw;
    height: 100vw;
    background-image: url('{{ "/assets/images/halftone-circle.png" | relative_url }}');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    opacity: inherit;
  }

  .bg-layer.has-image .bg-layer-halftone {
    display: none;
  }

  /* Main Quote Content Area */
  .slide-quote-content {
    flex: 1;
    min-height: 50vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    z-index: 5;
    padding-bottom: 4rem;
  }

  .quote-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 0.85rem;
    text-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
  }

  .quote-icon-open {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(3.5rem, 7vh, 6rem);
    color: #c3e4be;
    line-height: 1;
    font-weight: 700;
  }

  .quote-type {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(1.4rem, 2.8vh, 2.1rem);
    font-weight: 700;
    color: #c3e4be;
    letter-spacing: 0.02em;
  }

  .quote-body {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(1.6rem, 3.4vh, 2.75rem); /* Significantly larger to be prominent */
    font-weight: 700;
    line-height: 1.35;
    color: #ffffff;
    margin-bottom: 1.5rem;
    text-align: left;
    max-height: 48vh; /* Ensure quote fits and doesn't push into headers */
    overflow-y: auto;
    padding-right: 0.5rem;
    text-shadow: 0 4px 14px rgba(0, 0, 0, 0.65);
  }

  /* Custom subtle scrollbar for scrollable quotes */
  .quote-body::-webkit-scrollbar {
    width: 6px;
  }
  .quote-body::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 3px;
  }
  .quote-body::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.25);
    border-radius: 3px;
  }

  .quote-footer {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    text-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
  }

  .quote-icon-close {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(3rem, 6vh, 5rem);
    color: #c3e4be;
    line-height: 1;
    font-weight: 700;
    margin-top: 0.15rem;
  }

  .quote-credit {
    font-size: clamp(1rem, 2.2vh, 1.35rem);
    font-weight: 600;
    color: #c3e4be;
    line-height: 1.4;
  }



  .bottom-left-panel {
    position: absolute;
    bottom: 2rem;
    left: 3rem;
    right: 15rem; /* leave space for right nav buttons at bottom right */
    z-index: 100;
    display: flex;
    align-items: center;
    gap: 2.5rem;
    pointer-events: none;
  }

  .bottom-left-panel * {
    pointer-events: auto;
  }

  /* QR Code Widget & Map Widget */
  .qr-widget, .map-widget {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    flex-shrink: 0;
    opacity: 1;
    transition: opacity 0.35s ease;
  }

  .qr-widget.fading {
    opacity: 0;
  }

  .qr-widget canvas {
    border-radius: 8px;
    display: block;
  }

  .qr-label, .map-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.55);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* Case Metadata Widget */
  .case-meta-widget {
    flex: 1;
    display: flex;
    align-items: center;
    max-width: 800px;
    opacity: 1;
    transition: opacity 0.35s ease;
  }

  .case-meta-widget.fading {
    opacity: 0;
  }

  .case-stats-text {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(1.4rem, 2.8vh, 2.2rem); /* Large stats text, matching case study title size */
    font-weight: 700;
    line-height: 1.25;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.01em;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
  }

  .case-stats-text .stats-light {
    font-weight: 300;
    opacity: 0.85;
  }

  .mini-map-container {
    width: 240px;
    height: 128px; /* Same height as QR code */
    border-radius: 8px; /* Match QR code border radius */
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    background: #142011;
  }

  #mini-map {
    width: 100%;
    height: 100%;
    background: transparent;
  }

  /* Tooltip customization */
  .leaflet-tooltip.mini-map-tooltip {
    background-color: rgba(20, 32, 17, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #ffffff;
    font-family: 'Outfit', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    padding: 0.25rem 0.5rem;
  }

  .leaflet-tooltip-top.mini-map-tooltip::before {
    border-top-color: rgba(20, 32, 17, 0.95);
  }

  /* Responsive Styling */
  @media (max-width: 1200px) {
    .bottom-left-panel {
      right: 12rem;
      gap: 1.5rem;
    }
  }

  @media (max-width: 1100px) {
    .header-banner {
      grid-template-columns: 1fr;
      grid-template-rows: auto auto;
      gap: 0.75rem;
      height: auto;
      min-height: 10vh;
      padding: 1rem 1.5rem;
    }
    .header-banner-text {
      grid-row: 1;
      font-size: clamp(1.1rem, 3.2vh, 1.6rem);
      margin-bottom: 0.25rem;
    }
    .header-left {
      grid-row: 2;
      justify-self: flex-start;
    }
    .header-right {
      grid-row: 2;
      justify-self: flex-end;
    }
  }

  @media (max-width: 992px) {
    .slide-item {
      padding: calc(9rem + var(--banner-height)) 3rem 4rem 3rem;
    }
    .fixed-top-header {
      top: calc(3rem + var(--banner-height));
      left: 3rem;
      right: 3rem;
    }
    .slide-case-title {
      font-size: 1.8rem;
    }
    .quote-body {
      font-size: 2.1rem;
    }
    .bottom-left-panel {
      right: 10rem;
      gap: 1rem;
    }
    .case-stats-text {
      font-size: 1.5rem;
    }
  }

  @media (max-width: 850px) {
    .map-widget {
      display: none;
    }
    .bottom-left-panel {
      right: 8rem;
      left: 2rem;
      bottom: 2rem;
    }
    .case-stats-text {
      font-size: 1.25rem;
    }
  }

  @media (max-width: 768px) {
    /* Slim down top header banner */
    .header-banner {
      grid-template-columns: auto 1fr;
      grid-template-rows: auto;
      gap: 0.5rem;
      padding: 0.5rem 1rem;
      height: 60px !important;
      min-height: 60px !important;
    }
    .header-banner-text {
      grid-row: 1;
      font-size: 0.85rem !important;
      text-align: right;
      justify-self: end;
      margin: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
    }
    .header-left {
      grid-row: 1;
      justify-self: start;
    }
    
    /* Relocate controls to bottom fixed panel */
    .header-right {
      position: fixed !important;
      bottom: 0 !important;
      left: 0 !important;
      right: 0 !important;
      background: rgba(10, 16, 8, 0.95) !important;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 0.75rem 1rem !important;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      z-index: 1002 !important;
      width: 100%;
      box-sizing: border-box;
      justify-self: stretch;
    }
    .right-controls {
      display: flex !important;
      flex-direction: row !important;
      flex-wrap: wrap !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 0.5rem !important;
      width: 100% !important;
    }
    .autoplay-capsule {
      display: inline-flex !important;
      align-items: center !important;
      padding: 0.25rem 0.5rem !important;
      background: rgba(255, 255, 255, 0.06) !important;
      border: 1px solid rgba(255, 255, 255, 0.1) !important;
      border-radius: 20px !important;
      gap: 0.35rem !important;
      max-width: 100% !important;
    }
    .progress-bar-container {
      width: 50px !important;
    }
    .shuffle-btn {
      padding: 0.35rem !important;
      height: 30px !important;
      width: 30px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .case-select-capsule {
      flex: 1 1 100% !important; /* Wrap to its own full width row */
      margin-top: 0.25rem !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      padding: 0 !important;
    }
    .case-select {
      width: 100% !important;
      max-width: 100% !important;
      font-size: 0.8rem !important;
      padding: 0.35rem 0.75rem !important;
    }
    .back-to-cases {
      align-self: center;
      padding: 0.4rem 0.85rem;
      font-size: 0.75rem;
      white-space: nowrap;
    }
    
    /* Position case info/titles closer to top */
    .fixed-top-header {
      top: 75px !important;
      left: 1.5rem !important;
      right: 1.5rem !important;
    }
    .slide-case-title {
      font-size: 1.2rem !important;
    }
    .slide-case-subtitle {
      font-size: 0.75rem !important;
    }
    .slide-pave-logo {
      width: 2.2rem !important;
      height: 2.2rem !important;
    }
    
    /* Quote styling and container spacing */
    .slide-item {
      padding: 170px 1.5rem 120px 1.5rem !important;
    }
    .quote-body {
      font-size: 1.5rem !important;
      line-height: 1.45 !important;
    }
    .quote-type {
      font-size: 0.7rem !important;
    }
    .quote-credit {
      font-size: 0.75rem !important;
    }

    /* Position stats text as a pill above the bottom bar */
    .bottom-left-panel {
      left: 1rem !important;
      right: 1rem !important;
      bottom: 75px !important; /* place just above bottom control bar */
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      text-align: center !important;
      background: none !important;
      box-shadow: none !important;
      pointer-events: none !important;
    }
    .qr-widget, .map-widget {
      display: none !important; /* hide qr code and map on mobile */
    }
    .case-meta-widget {
      background: rgba(10, 16, 8, 0.85) !important;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 0.4rem 0.85rem !important;
      border-radius: 8px !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      pointer-events: auto !important;
    }
    .case-stats-text {
      font-size: 0.8rem !important;
      line-height: 1.35 !important;
      margin: 0 !important;
      text-shadow: none !important;
    }
  }
</style>

<div class="slideshow-container" id="slideshow-container">
  <!-- Top Header Banner & Navigation Controls -->
  <div class="header-banner">
    <!-- Left: Back Button -->
    <div class="header-left">
      <a href="{{ '/' | relative_url }}" class="back-to-cases" title="Back to site">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        <span>Back to site</span>
      </a>
    </div>

    <!-- Center: Title -->
    <h1 class="header-banner-text">What are people around the world saying about AI?</h1>

    <!-- Right: Controls & Drop-down -->
    <div class="header-right">
      <div class="right-controls">
        <!-- Autoplay capsule -->
        <div class="autoplay-capsule">
          <button class="play-pause-btn" id="play-pause-btn" aria-label="Pause Autoplay">
            <svg class="pause-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
            <svg class="play-icon" viewBox="0 0 24 24" fill="currentColor" style="display: none;">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </button>

          <select id="speed-select" class="speed-select" aria-label="Autoplay Speed">
            <option value="14000">Slow (14s)</option>
            <option value="10000" selected>Medium (10s)</option>
            <option value="7000">Fast (7s)</option>
          </select>

          <button class="shuffle-btn active" id="shuffle-btn" aria-label="Toggle Random Order" title="Toggle Random Order">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="16 3 21 3 21 8"></polyline>
              <line x1="4" y1="20" x2="21" y2="3"></line>
              <polyline points="21 16 21 21 16 21"></polyline>
              <line x1="15" y1="15" x2="21" y2="21"></line>
              <line x1="4" y1="4" x2="9" y2="9"></line>
            </svg>
          </button>

          <div class="progress-bar-container">
            <div class="progress-bar-fill" id="progress-bar-fill"></div>
          </div>

          <div class="slide-counter" id="slide-counter">1 / 1</div>
        </div>

        <!-- Case Selection Capsule -->
        <div class="case-select-capsule">
          <select id="case-select" class="case-select" aria-label="Select Case Study">
            <option value="featured" selected>Featured messages</option>
            <option value="all">All messages</option>
            <option value="disabled" disabled>-- Specific case (Selecte below) --</option>
            {% assign opt_case_index = 0 %}
            {% for case in site.cases %}
              {% if case.messages %}
                <option value="{{ opt_case_index }}">{{ case.title | escape }}</option>
                {% assign opt_case_index = opt_case_index | plus: 1 %}
              {% endif %}
            {% endfor %}
          </select>
        </div>
      </div>
    </div>
  </div>

  <!-- Fixed Top Header (Static Case Title/Subtitle & PAVE Logo) -->
  <div class="fixed-top-header">
    <div class="slide-case-info" id="fixed-case-info">
      <h2 class="slide-case-title" id="fixed-case-title"></h2>
      <p class="slide-case-subtitle" id="fixed-case-subtitle"></p>
    </div>
    <div class="slide-pave-logo">
      <img src="{{ '/assets/images/adobe_component_6.png' | relative_url }}" alt="PAVE Logo">
    </div>
  </div>

  <!-- Fixed Background Layers (A/B for cross-fade, never move with slides) -->
  <div class="bg-layer" id="bg-layer-a" style="opacity: 0.28;">
    <div class="bg-layer-halftone"></div>
  </div>
  <div class="bg-layer" id="bg-layer-b" style="opacity: 0;">
    <div class="bg-layer-halftone"></div>
  </div>

  <!-- Slides Track -->
  <div class="slides-track" id="slides-track">
    {% assign slide_index = 0 %}
    {% assign case_index = 0 %}
    
    {% for case in site.cases %}
      {% if case.messages %}
        {% for message_slug in case.messages %}
          {% assign message = site.messages | where: "slug", message_slug | first %}
          {% if message %}

            {% assign bg_url = nil %}
            {% if case.photos-and-images and case.photos-and-images.size > 0 %}
              {% if case.photos-and-images[0].thumbnails.large %}
                {% assign bg_url = case.photos-and-images[0].thumbnails.large.url %}
              {% else %}
                {% assign bg_url = case.photos-and-images[0].url %}
              {% endif %}
            {% endif %}

            {% assign deliberating_people = 0 %}
            {% assign total_deliberating_person_hours = 0 %}
            {% assign deliberating_people_with_hours = 0 %}

            {% assign participating_people = 0 %}
            {% assign total_participating_person_hours = 0 %}
            {% assign participating_people_with_hours = 0 %}

            {% assign contributing_people = 0 %}
            {% assign other_people = 0 %}

            {% assign has_collective_intelligence = false %}
            {% assign has_non_delib_participated = false %}
            {% assign has_non_delib_contributed = false %}

            {% for part_slug in case.participants %}
              {% assign part = site.participants | where: "slug", part_slug | first %}
              {% if part %}
                {% assign is_deliberative_group = false %}
                {% assign is_participated_group = false %}
                {% assign is_contributed_group = false %}
                
                {% for method in part.which-of-the-following-methods-were-used-to %}
                  {% if method == "Collective Intelligence Process" %}
                    {% assign has_collective_intelligence = true %}
                  {% endif %}
                  {% if site.data.methods_map.deliberated contains method %}
                    {% assign is_deliberative_group = true %}
                  {% endif %}
                  {% if site.data.methods_map.participated contains method %}
                    {% assign is_participated_group = true %}
                  {% endif %}
                  {% if site.data.methods_map.contributed contains method %}
                    {% assign is_contributed_group = true %}
                  {% endif %}
                {% endfor %}

                {% if is_deliberative_group %}
                  {% if part.how-many-people-took-part %}
                    {% assign p_count = part.how-many-people-took-part | plus: 0 %}
                    {% assign deliberating_people = deliberating_people | plus: p_count %}
                    
                    {% if part.on-average-how-many-hours-did-each-participant %}
                      {% assign p_hours = part.on-average-how-many-hours-did-each-participant | plus: 0 %}
                      {% assign group_hours = p_count | times: p_hours %}
                      {% assign total_deliberating_person_hours = total_deliberating_person_hours | plus: group_hours %}
                      {% assign deliberating_people_with_hours = deliberating_people_with_hours | plus: p_count %}
                    {% endif %}
                  {% endif %}
                {% elsif is_participated_group %}
                  {% assign has_non_delib_participated = true %}
                  {% if part.how-many-people-took-part %}
                    {% assign p_count = part.how-many-people-took-part | plus: 0 %}
                    {% assign participating_people = participating_people | plus: p_count %}
                    
                    {% if part.on-average-how-many-hours-did-each-participant %}
                      {% assign p_hours = part.on-average-how-many-hours-did-each-participant | plus: 0 %}
                      {% assign group_hours = p_count | times: p_hours %}
                      {% assign total_participating_person_hours = total_participating_person_hours | plus: group_hours %}
                      {% assign participating_people_with_hours = participating_people_with_hours | plus: p_count %}
                    {% endif %}
                  {% endif %}
                {% elsif is_contributed_group %}
                  {% assign has_non_delib_contributed = true %}
                  {% if part.how-many-people-took-part %}
                    {% assign p_count = part.how-many-people-took-part | plus: 0 %}
                    {% assign contributing_people = contributing_people | plus: p_count %}
                  {% endif %}
                {% else %}
                  {% if part.how-many-people-took-part %}
                    {% assign p_count = part.how-many-people-took-part | plus: 0 %}
                    {% assign other_people = other_people | plus: p_count %}
                  {% endif %}
                {% endif %}
              {% endif %}
            {% endfor %}

            {% assign avg_delib_hours = 0 %}
            {% assign avg_delib_hours_display = "" %}
            {% if deliberating_people_with_hours > 0 %}
              {% assign raw_avg_delib_hours = total_deliberating_person_hours | times: 1.0 | divided_by: deliberating_people_with_hours %}
              {% assign rounded_delib = raw_avg_delib_hours | round: 1 | append: "" %}
              {% if rounded_delib contains ".0" %}
                {% assign delib_parts = rounded_delib | split: "." %}
                {% assign avg_delib_hours_display = delib_parts[0] %}
              {% else %}
                {% assign avg_delib_hours_display = rounded_delib %}
              {% endif %}
              {% assign avg_delib_hours = raw_avg_delib_hours %}
            {% endif %}

            {% assign avg_part_hours = 0 %}
            {% assign avg_part_hours_display = "" %}
            {% if participating_people_with_hours > 0 %}
              {% assign raw_avg_part_hours = total_participating_person_hours | times: 1.0 | divided_by: participating_people_with_hours %}
              {% assign rounded_part = raw_avg_part_hours | round: 1 | append: "" %}
              {% if rounded_part contains ".0" %}
                {% assign part_parts = rounded_part | split: "." %}
                {% assign avg_part_hours_display = part_parts[0] %}
              {% else %}
                {% assign avg_part_hours_display = rounded_part %}
              {% endif %}
              {% assign avg_part_hours = raw_avg_part_hours %}
            {% endif %}

            {% assign non_delib_people = participating_people | plus: contributing_people | plus: other_people %}
            {% assign non_delib_verb = "participated" %}
            {% if has_non_delib_participated %}
              {% assign non_delib_verb = "participated" %}
            {% elsif has_non_delib_contributed %}
              {% if has_collective_intelligence %}
                {% assign non_delib_verb = "contributed to a collective intelligence process" %}
              {% else %}
                {% assign non_delib_verb = "contributed" %}
              {% endif %}
            {% endif %}

            {% assign start_year = case.what-year-did-the-project-start %}
            {% assign end_year = case.what-year-did-the-project-conclude %}
            {% assign year_text = "" %}

            {% if start_year and end_year %}
              {% if start_year == end_year %}
                {% assign year_text = "In " | append: start_year %}
              {% else %}
                {% assign year_text = "Between " | append: start_year | append: " and " | append: end_year %}
              {% endif %}
            {% elsif start_year %}
              {% assign year_text = "In " | append: start_year %}
            {% elsif end_year %}
              {% assign year_text = "In " | append: end_year %}
            {% endif %}

            {% capture stats_text %}{% if year_text != "" %}<span class="stats-light">{{ year_text }}</span> {% endif %}{% if deliberating_people > 0 and non_delib_people > 0 %}{% if non_delib_people > 0 %}{{ non_delib_people }} participants{% else %}participants{% endif %} {{ non_delib_verb }}{% if non_delib_verb == "participated" and avg_part_hours > 0 %} over the course of {{ avg_part_hours_display }} hours{% endif %} and {% if deliberating_people > 0 %}{{ deliberating_people }}{% else %}others{% endif %} deliberated{% if avg_delib_hours > 0 %} over the course of {{ avg_delib_hours_display }} hours{% endif %} <span class="stats-light">to explore issues related to AI.</span>{% elsif deliberating_people > 0 %}{% if deliberating_people > 0 %}{{ deliberating_people }} participants{% else %}participants{% endif %} deliberated{% if avg_delib_hours > 0 %} over the course of {{ avg_delib_hours_display }} hours{% endif %} <span class="stats-light">to explore issues related to AI.</span>{% else %}{% if non_delib_people > 0 %}{{ non_delib_people }} participants{% else %}participants{% endif %} {{ non_delib_verb }}{% if non_delib_verb == "participated" and avg_part_hours > 0 %} over the course of {{ avg_part_hours_display }} hours{% endif %} <span class="stats-light">to explore issues related to AI.</span>{% endif %}{% endcapture %}

            {% assign loc_array = "" | split: "" %}
            {% for part_slug in case.participants %}
              {% assign part = site.participants | where: "slug", part_slug | first %}
              {% if part %}
                {% for loc_slug in part.locations %}
                  {% assign loc = site.locations | where: "slug", loc_slug | first %}
                  {% if loc.latitude and loc.longitude %}
                    {% capture loc_json %}{"lat":{{ loc.latitude }},"lng":{{ loc.longitude }},"name":"{{ loc.title | escape }}"}{% endcapture %}
                    {% assign loc_array = loc_array | push: loc_json %}
                  {% endif %}
                {% endfor %}
              {% endif %}
            {% endfor %}
            {% assign unique_locs = loc_array | uniq %}

            <div class="slide-item" 
                 data-slide-index="{{ slide_index }}"
                 data-case-index="{{ case_index }}"
                 data-featured="{% if message.featured and message.featured.size > 0 %}true{% else %}false{% endif %}"
                 data-case-title="{{ case.title | escape }} ({{case.what-year-did-the-project-start}} - {{case.what-year-did-the-project-conclude}})"
                 data-case-subtitle="{{ case.describe-the-subject-matter-in-your-own-words-one | escape }}"
                 data-case-url="{{ '/c/' | append: case.airtable_id | append: '/' | absolute_url }}"
                 data-case-stats="{{ stats_text | escape }}"
                 data-case-locations='[{{ unique_locs | join: "," }}]'
                 {% if bg_url %}data-bg-image="{{ bg_url | relative_url }}"{% endif %}>

              <!-- Center: Quote / Recommendation Body -->
              <div class="slide-quote-content">
                <div class="quote-header">
                  <span class="quote-icon-open">“</span>
                  <span class="quote-type">{{ message.type }}</span>
                </div>
                <div class="quote-body">
                  {{ message.title }}
                </div>
                {% if message.additional-credit-line %}
                  <div class="quote-footer">
                     <span class="quote-icon-close">”</span>
                     <span class="quote-credit">{{ message.additional-credit-line }}</span>
                  </div>
                {% endif %}
              </div>
            </div>

            {% assign slide_index = slide_index | plus: 1 %}
          {% endif %}
        {% endfor %}
        {% assign case_index = case_index | plus: 1 %}
      {% endif %}
    {% endfor %}
  </div>

  <!-- Bottom Left Panel -->
  <div class="bottom-left-panel">
    <!-- QR Code Widget -->
    <div class="qr-widget" id="qr-widget">
      <div id="qr-code"></div>
      <span class="qr-label">Scan to view case</span>
    </div>

    <!-- Mini-Map Widget (Stays floating, does not fade out) -->
    <div class="map-widget" id="map-widget">
      <div class="mini-map-container">
        <div id="mini-map"></div>
      </div>
      <span class="map-label">Participant Locations</span>
    </div>

    <!-- Case Stats Widget (Fades out/in) -->
    <div class="case-meta-widget" id="case-meta-widget">
      <p class="case-stats-text" id="case-stats-text"></p>
    </div>
  </div>

  <!-- Edge Navigation Zones (Hover & Click to change slides) -->
  <div class="edge-nav-zone nav-zone-left" id="prev-btn" aria-label="Previous slide" title="Previous Slide">
    <div class="edge-nav-btn">
      <svg viewBox="0 0 24 24">
        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
      </svg>
    </div>
  </div>

  <div class="edge-nav-zone nav-zone-right" id="next-btn" aria-label="Next slide" title="Next Slide">
    <div class="edge-nav-btn">
      <svg viewBox="0 0 24 24">
        <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
      </svg>
    </div>
  </div>
</div>


<!-- Slideshow Logic Engine -->
<script>
document.addEventListener('DOMContentLoaded', () => {
  // Spacing calculation helper for dynamic header banner height
  function adjustHeaderSpacing() {
    const banner = document.querySelector('.header-banner');
    if (banner) {
      const height = banner.offsetHeight;
      document.documentElement.style.setProperty('--banner-height', `${height}px`);
    }
  }
  adjustHeaderSpacing();
  window.addEventListener('resize', adjustHeaderSpacing);

  const container = document.getElementById('slideshow-container');
  const track = document.getElementById('slides-track');
  const slides = document.querySelectorAll('.slide-item');
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const playPauseBtn = document.getElementById('play-pause-btn');
  const playIcon = playPauseBtn.querySelector('.play-icon');
  const pauseIcon = playPauseBtn.querySelector('.pause-icon');
  const progressBarFill = document.getElementById('progress-bar-fill');
  const slideCounter = document.getElementById('slide-counter');
  const speedSelect = document.getElementById('speed-select');
  const caseSelect = document.getElementById('case-select');

  const totalSlides = slides.length;
  if (totalSlides === 0) return;

  const shuffleBtn = document.getElementById('shuffle-btn');

  let currentIndex = 0;
  let slideDuration = parseInt(speedSelect.value);
  let lastTime = 0;
  let progress = 0;
  let animationFrameId = null;
  let isPlaying = true;
  let currentCaseIndex = -1;

  let isRandom = true;
  let orderArray = Array.from({ length: totalSlides }, (_, i) => i);
  let orderPosition = 0;

  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }

  function applyDOMOrder() {
    track.style.transition = 'none';
    orderArray.forEach(slideIndex => {
      track.appendChild(slides[slideIndex]);
    });
    track.style.transform = `translateX(-${orderPosition * 100}vw)`;
    // Force reflow
    track.offsetHeight;
    track.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
  }

  function applyFilter() {
    const filterValue = caseSelect ? caseSelect.value : 'featured';
    
    // 1. Determine active indexes
    let activeIndexes = [];
    if (filterValue === 'featured') {
      for (let i = 0; i < totalSlides; i++) {
        if (slides[i].dataset.featured === 'true') {
          activeIndexes.push(i);
        }
      }
    } else if (filterValue === 'all') {
      activeIndexes = Array.from({ length: totalSlides }, (_, i) => i);
    } else {
      // Specific case index
      const selectedCaseIndex = parseInt(filterValue);
      for (let i = 0; i < totalSlides; i++) {
        if (parseInt(slides[i].dataset.caseIndex) === selectedCaseIndex) {
          activeIndexes.push(i);
        }
      }
    }

    // Handle edge case: if no slides match
    if (activeIndexes.length === 0) {
      activeIndexes = Array.from({ length: totalSlides }, (_, i) => i);
    }

    // Hide all slides first, then show only active slides
    slides.forEach((slide, idx) => {
      if (activeIndexes.includes(idx)) {
        slide.style.display = '';
      } else {
        slide.style.display = 'none';
      }
    });

    // 2. Set orderArray based on isRandom and activeIndexes
    if (isRandom) {
      const currentSlideIdx = orderArray[orderPosition];
      let pool = [...activeIndexes];
      let firstVal = null;
      if (currentSlideIdx !== undefined && pool.includes(currentSlideIdx)) {
        firstVal = currentSlideIdx;
        pool = pool.filter(v => v !== currentSlideIdx);
      }
      shuffleArray(pool);
      if (firstVal !== null) {
        orderArray = [firstVal, ...pool];
      } else {
        orderArray = pool;
      }
      orderPosition = 0;
    } else {
      const currentSlideIdx = orderArray[orderPosition];
      orderArray = [...activeIndexes];
      if (currentSlideIdx !== undefined && orderArray.includes(currentSlideIdx)) {
        orderPosition = orderArray.indexOf(currentSlideIdx);
      } else {
        orderPosition = 0;
      }
    }

    applyDOMOrder();
    
    if (orderArray.length > 0) {
      goToSlide(orderArray[orderPosition]);
    }
  }

  function setRandomOrder(randomize) {
    isRandom = randomize;
    if (isRandom) {
      shuffleBtn.classList.add('active');
      const currentVal = orderArray[orderPosition];
      const activeIndexes = [...orderArray];
      const remaining = activeIndexes.filter(v => v !== currentVal);
      shuffleArray(remaining);
      orderArray = [currentVal, ...remaining];
      orderPosition = 0;
    } else {
      shuffleBtn.classList.remove('active');
      const currentVal = orderArray[orderPosition];
      const activeIndexesSorted = [...orderArray].sort((a, b) => a - b);
      orderArray = activeIndexesSorted;
      orderPosition = orderArray.indexOf(currentVal);
    }
    applyDOMOrder();

    if (orderArray.length > 0) {
      slideCounter.innerText = `${orderPosition + 1} / ${orderArray.length}`;
    }
  }

  // Background cross-fade layer references
  const bgLayerA = document.getElementById('bg-layer-a');
  const bgLayerB = document.getElementById('bg-layer-b');
  let activeBgLayer = 'a'; // 'a' starts visible

  // Cross-fade between fixed background layers on case change
  function crossFadeBackground(imageUrl) {
    const incoming = activeBgLayer === 'a' ? bgLayerB : bgLayerA;
    const outgoing = activeBgLayer === 'a' ? bgLayerA : bgLayerB;

    if (imageUrl) {
      incoming.classList.add('has-image');
      incoming.style.backgroundImage = 'linear-gradient(rgba(20, 32, 17, 0.45), rgba(20, 32, 17, 0.65)), url(' + imageUrl + ')';
      incoming.style.backgroundSize = 'cover';
      incoming.style.backgroundPosition = 'center';
      incoming.style.opacity = '0.6';
    } else {
      incoming.classList.remove('has-image');
      incoming.style.backgroundImage = 'none';
      incoming.style.opacity = '0.28';
    }

    outgoing.style.opacity = '0';
    activeBgLayer = activeBgLayer === 'a' ? 'b' : 'a';
  }

  // Initialize Counter display
  slideCounter.innerText = `1 / ${totalSlides}`;

  // QR Code & Mini-Map widget
  const qrWidget = document.getElementById('qr-widget');
  const qrCodeEl = document.getElementById('qr-code');
  const caseMetaWidget = document.getElementById('case-meta-widget');
  const caseStatsTextEl = document.getElementById('case-stats-text');
  
  let qrInstance = null;
  let qrCurrentUrl = null;
  let miniMap = null;
  let markerGroup = null;

  function initMiniMap() {
    const miniMapEl = document.getElementById('mini-map');
    if (!miniMapEl) return;
    
    miniMap = L.map('mini-map', {
      zoomControl: false,
      attributionControl: false,
      dragging: false,
      scrollWheelZoom: false,
      doubleClickZoom: false,
      boxZoom: false
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=cb1_4qtr_1_72e49fe987375b3637f246b7', {
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 20
    }).addTo(miniMap);

    markerGroup = L.layerGroup().addTo(miniMap);
  }

  function updateQRCodeAndStats(url, statsText, locations) {
    if (!url) return;

    // 1. Update Mini Map immediately with smooth pan/zoom transition
    if (miniMap && markerGroup) {
      markerGroup.clearLayers();
      miniMap.invalidateSize();
      
      if (locations && locations.length > 0) {
        let bounds = [];
        locations.forEach(loc => {
          if (loc.lat && loc.lng) {
            const marker = L.circleMarker([loc.lat, loc.lng], {
              color: '#ffffff',
              fillColor: '#ffd700',
              fillOpacity: 0.8,
              radius: 6,
              weight: 1.5
            });
            marker.bindTooltip(loc.name, {
              direction: 'top',
              className: 'mini-map-tooltip'
            });
            marker.addTo(markerGroup);
            bounds.push([loc.lat, loc.lng]);
          }
        });

        if (bounds.length > 0) {
          if (bounds.length === 1) {
            miniMap.setView(bounds[0], 5, { animate: true, duration: 0.8 });
          } else {
            miniMap.fitBounds(bounds, { padding: [15, 15], animate: true, duration: 0.8 });
          }
        }
      } else {
        // World view fallback if no locations
        miniMap.setView([20, 0], 1, { animate: true, duration: 0.8 });
      }
    }

    // 2. Fade out QR and Stats text
    qrWidget.classList.add('fading');
    if (caseMetaWidget) caseMetaWidget.classList.add('fading');

    setTimeout(() => {
      // 3. Update QR
      if (url !== qrCurrentUrl) {
        qrCurrentUrl = url;
        qrCodeEl.innerHTML = '';
        qrInstance = new QRCode(qrCodeEl, {
          text: url,
          width: 128,
          height: 128,
          colorDark: '#ffffff',
          colorLight: 'rgba(0,0,0,0)',
          correctLevel: QRCode.CorrectLevel.L
        });
      }

      // 4. Update Stats Text
      if (caseStatsTextEl) {
        caseStatsTextEl.innerHTML = statsText;
      }

      // Fade back in QR and Stats
      qrWidget.classList.remove('fading');
      if (caseMetaWidget) caseMetaWidget.classList.remove('fading');
    }, 300);
  }

  function updateCaseSelect(caseIndex) {
    if (caseSelect) {
      if (caseSelect.value !== 'featured' && caseSelect.value !== 'all') {
        caseSelect.value = caseIndex;
      }
    }
  }

  function goToSlide(index) {
    currentIndex = index;
    if (currentIndex >= totalSlides) currentIndex = 0;
    if (currentIndex < 0) currentIndex = totalSlides - 1;

    orderPosition = orderArray.indexOf(currentIndex);
    if (orderPosition === -1) {
      orderPosition = 0;
      currentIndex = orderArray[0];
    }
    
    // Transition slides track horizontally using orderPosition for a single slide transition
    track.style.transform = `translateX(-${orderPosition * 100}vw)`;
    slideCounter.innerText = `${orderPosition + 1} / ${orderArray.length}`;

    // Adjust font size dynamically for long quotes to prevent overflow/overlap
    const activeSlide = slides[currentIndex];
    const quoteBody = activeSlide.querySelector('.quote-body');
    if (quoteBody) {
      const textLength = quoteBody.textContent.trim().length;
      let fontSize = '2.5rem'; // Default desktop size
      
      if (window.innerWidth <= 768) {
        // Mobile sizes
        if (textLength > 300) {
          fontSize = '1.05rem';
        } else if (textLength > 200) {
          fontSize = '1.2rem';
        } else if (textLength > 100) {
          fontSize = '1.4rem';
        } else {
          fontSize = '1.65rem';
        }
      } else {
        // Desktop sizes
        if (textLength > 300) {
          fontSize = '1.5rem';
        } else if (textLength > 200) {
          fontSize = '1.85rem';
        } else if (textLength > 100) {
          fontSize = '2.15rem';
        }
      }
      quoteBody.style.fontSize = fontSize;
    }
    
    // Update case info elements with transitions when case changes
    const caseIndex = parseInt(activeSlide.dataset.caseIndex);
    const title = activeSlide.dataset.caseTitle;
    const subtitle = activeSlide.dataset.caseSubtitle;
    const imageUrl = activeSlide.dataset.bgImage;

    const titleEl = document.getElementById('fixed-case-title');
    const subtitleEl = document.getElementById('fixed-case-subtitle');
    const caseInfoEl = document.getElementById('fixed-case-info');

    if (caseIndex !== currentCaseIndex) {
      currentCaseIndex = caseIndex;

      // Cross-fade the fixed background layer
      crossFadeBackground(imageUrl);

      // Parse case locations
      let locations = [];
      try {
        locations = JSON.parse(activeSlide.dataset.caseLocations || '[]');
      } catch (e) {
        console.error("Error parsing case locations JSON:", e);
      }

      // Update QR code and stats next to it
      updateQRCodeAndStats(activeSlide.dataset.caseUrl, activeSlide.dataset.caseStats, locations);

      // Fade out/in the case title block
      if (caseInfoEl) {
        caseInfoEl.style.opacity = '0';
        setTimeout(() => {
          if (titleEl) titleEl.textContent = title;
          if (subtitleEl) subtitleEl.textContent = subtitle;
          caseInfoEl.style.opacity = '1';
        }, 150);
      } else {
        if (titleEl) titleEl.textContent = title;
        if (subtitleEl) subtitleEl.textContent = subtitle;
      }
    }

    updateCaseSelect(caseIndex);

    // Reset timer progress
    lastTime = performance.now();
    progress = 0;
    progressBarFill.style.width = '0%';
  }

  function goToNextSlide() {
    let nextPosition = orderPosition + 1;
    if (nextPosition >= orderArray.length) nextPosition = 0;
    goToSlide(orderArray[nextPosition]);
  }

  function goToPrevSlide() {
    let prevPosition = orderPosition - 1;
    if (prevPosition < 0) prevPosition = orderArray.length - 1;
    goToSlide(orderArray[prevPosition]);
  }

  // Animation cycle loop using requestAnimationFrame
  function tick(timestamp) {
    if (!lastTime) lastTime = timestamp;
    
    if (isPlaying) {
      const elapsed = timestamp - lastTime;
      progress = (elapsed / slideDuration) * 100;
      
      if (progress >= 100) {
        progress = 0;
        lastTime = timestamp;
        goToNextSlide();
      }
      progressBarFill.style.width = `${progress}%`;
    } else {
      // Preserve elapsed calculation relative to progress when paused
      lastTime = timestamp - (progress / 100) * slideDuration;
    }
    
    animationFrameId = requestAnimationFrame(tick);
  }

  // Start autoplay timer
  animationFrameId = requestAnimationFrame(tick);

  function pauseAutoplay() {
    isPlaying = false;
    playIcon.style.display = 'block';
    pauseIcon.style.display = 'none';
  }

  function playAutoplay() {
    isPlaying = true;
    playIcon.style.display = 'none';
    pauseIcon.style.display = 'block';
    lastTime = performance.now();
  }

  // Controls bindings
  prevBtn.addEventListener('click', goToPrevSlide);
  nextBtn.addEventListener('click', goToNextSlide);

  shuffleBtn.addEventListener('click', () => {
    setRandomOrder(!isRandom);
  });

  playPauseBtn.addEventListener('click', () => {
    if (isPlaying) {
      pauseAutoplay();
    } else {
      playAutoplay();
    }
  });

  // Handle Autoplay Speed changes
  speedSelect.addEventListener('change', () => {
    slideDuration = parseInt(speedSelect.value);
    // Restart current progress cycle
    lastTime = performance.now();
    progress = 0;
    progressBarFill.style.width = '0%';
  });

  // Handle Case Dropdown selection changes
  if (caseSelect) {
    caseSelect.addEventListener('change', () => {
      applyFilter();
    });
  }

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
      goToNextSlide();
    } else if (e.key === 'ArrowLeft') {
      goToPrevSlide();
    } else if (e.key === ' ') {
      e.preventDefault(); // prevent space from scrolling page
      if (isPlaying) {
        pauseAutoplay();
      } else {
        playAutoplay();
      }
    }
  });

  // Swipe gestures support for mobile devices
  let touchStartX = 0;
  let touchEndX = 0;

  container.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  container.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, { passive: true });

  function handleSwipe() {
    const swipeThreshold = 55;
    if (touchStartX - touchEndX > swipeThreshold) {
      goToNextSlide();
    } else if (touchEndX - touchStartX > swipeThreshold) {
      goToPrevSlide();
    }
  }

  // Initialize mini-map first
  initMiniMap();

  // Initialize with filter and random order by default
  if (totalSlides > 0) {
    applyFilter();
  }
});
</script>
