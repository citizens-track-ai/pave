---
layout: page
title: Welcome to the Public AI Voice and Engagement (PAVE) Case Book
description: "Explore the Public AI Voice and Engagement (PAVE) Case Book, cataloguing global participatory initiatives, citizen assemblies, and public voice projects shaping AI governance."
---

{% comment %}
  Dynamic Jekyll aggregation logic for Case Book statistics
{% endcomment %}
{% assign total_cases = 0 %}
{% assign total_participants = 0 %}
{% assign total_hours = 0 %}
{% assign unique_countries = "" | split: "" %}

{% for case in site.cases %}
  {% if case.curation-decision == "Do not include" %}{% continue %}{% endif %}
  {% assign total_cases = total_cases | plus: 1 %}
{% endfor %}

{% for part in site.participants %}
  {% assign linked_case_valid = false %}
  {% for case_slug in part.cases %}
    {% assign case_obj = site.cases | where: "slug", case_slug | first %}
    {% if case_obj and case_obj.curation-decision != "Do not include" %}
      {% assign linked_case_valid = true %}
    {% endif %}
  {% endfor %}
  {% if linked_case_valid == false %}{% continue %}{% endif %}

  {% if part.how-many-people-took-part %}
    {% assign p_count = part.how-many-people-took-part | plus: 0 %}
    {% assign total_participants = total_participants | plus: p_count %}
    
    {% if part.on-average-how-many-hours-did-each-participant %}
      {% assign p_hours = part.on-average-how-many-hours-did-each-participant | plus: 0 %}
      {% assign p_total_hours = p_count | times: p_hours %}
      {% assign total_hours = total_hours | plus: p_total_hours %}
    {% endif %}
  {% endif %}
  
  {% for loc_slug in part.locations %}
    {% assign loc = site.locations | where: "slug", loc_slug | first %}
    {% if loc.country-code %}
      {% assign c_code = loc.country-code | upcase %}
      {% unless unique_countries contains c_code %}
        {% assign unique_countries = unique_countries | push: c_code %}
      {% endunless %}
    {% endif %}
  {% endfor %}
{% endfor %}

{% assign total_countries_count = unique_countries | size %}

{% comment %}
  Map Coordinates Extraction - Filter to ONLY Featured and Full Case studies (Exclude Mapping Entries)
{% endcomment %}
{% assign coords = "" | split: "" %}
{% for case in site.cases %}
  {% if case.curation-decision == "Mapping Entry" or case.curation-decision == "Mapping Entries" or case.curation-decision == "Do not include" %}{% continue %}{% endif %}
  {% for part_slug in case.participants %}
    {% assign part = site.participants | where: "slug", part_slug | first %}
    {% if part %}
      {% for loc_slug in part.locations %}
        {% assign loc = site.locations | where: "slug", loc_slug | first %}
        {% if loc.latitude and loc.longitude %}
          {% capture loc_json %}{"lat":{{ loc.latitude }},"lng":{{ loc.longitude }},"name":"{{ loc.title | escape }}","case":"{{ case.title | escape }}"}{% endcapture %}
          {% assign coords = coords | push: loc_json %}
        {% endif %}
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endfor %}
{% assign unique_coords = coords | uniq %}

<style>
  /* 1. Style theme wrapper to span wider dashboard layout on home */
  .page-content {
    background: transparent !important;
  }
  
  .site-header .wrapper,
  .site-footer .wrapper,
  .page-content .wrapper {
    max-width: 1200px !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }
  
  .page-content .wrapper {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
  }

  /* Hide default Jekyll title for layout: page on homepage */
  .post-header {
    display: none !important;
  }

  /* 2. Dashboard Elements in light theme matching main.scss */
  .dashboard-container {
    display: flex;
    flex-direction: column;
    gap: 3.5rem;
    padding-top: 1rem;
  }

  /* Hero Section split: dynamic stats on left, globe on right */
  .hero-panel {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 2.5rem;
    align-items: center;
  }

  .hero-left {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .hero-wip-badge {
    align-self: flex-start;
    background: rgba(73, 106, 64, 0.06);
    border: 1px solid rgba(73, 106, 64, 0.25);
    color: #496a40;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
  }

  .hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin: 0;
    color: #1a2f16;
  }

  .hero-subtitle {
    font-size: clamp(1rem, 2vw, 1.15rem);
    line-height: 1.55;
    color: #243f1f;
    margin: 0;
  }

  /* Dynamic count-up stats layout */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
    margin-top: 1rem;
  }

  .stat-card {
    background: #ffffff;
    border: 1px solid rgba(73, 106, 64, 0.12);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
  }

  .stat-number {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 700;
    color: #1a2f16;
    line-height: 1.1;
  }

  .stat-card:nth-child(2) .stat-number {
    color: #496a40;
  }

  .stat-card:nth-child(3) .stat-number {
    color: #2e4728;
  }

  .stat-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6a8c61;
  }

  /* Rotating Globe Styling */
  .hero-right {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
  }

  .globe-container {
    position: relative;
    width: 100%;
    max-width: 380px;
    aspect-ratio: 1 / 1;
    height: auto;
    border-radius: 50%;
    cursor: grab;
  }

  .globe-container:active {
    cursor: grabbing;
  }

  #globe-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  /* 4. Action Cards Grid Layout (2x2) */
  .action-cards-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .action-card {
    background: #ffffff;
    border: 1px solid rgba(73, 106, 64, 0.12);
    border-radius: 16px;
    padding: 2rem;
    display: flex;
    gap: 1.5rem;
    text-decoration: none !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .action-card:hover {
    transform: translateY(-6px);
    background: rgba(73, 106, 64, 0.04);
    border-color: #496a40;
    box-shadow: 0 12px 30px rgba(73, 106, 64, 0.1);
  }

  .action-icon-wrapper {
    flex-shrink: 0;
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 12px;
    background: rgba(73, 106, 64, 0.06);
    border: 1px solid rgba(73, 106, 64, 0.15);
    color: #496a40;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .action-card:hover .action-icon-wrapper {
    background: #496a40;
    color: #ffffff;
    border-color: #496a40;
    transform: scale(1.05);
  }

  .action-info {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .action-card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #1a2f16;
    margin: 0;
  }

  .action-card-description {
    font-size: 0.9rem;
    line-height: 1.5;
    color: #375030;
    margin: 0;
  }

  .action-cta {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.88rem;
    font-weight: 700;
    color: #496a40;
    margin-top: 0.5rem;
    transition: gap 0.2s ease;
  }

  .action-card:hover .action-cta {
    color: #1a2f16;
    gap: 0.6rem;
  }

  /* 5. Responsive Breakpoints */
  @media (max-width: 992px) {
    .hero-panel {
      grid-template-columns: 1fr;
      gap: 3rem;
      text-align: center;
    }
    .hero-wip-badge {
      align-self: center;
    }
    .hero-title {
      font-size: 2.75rem;
    }
    .stats-grid {
      max-width: 600px;
      margin: 1.5rem auto 0 auto;
      width: 100%;
    }
    .action-cards-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 768px) {
    .hero-title {
      font-size: 2.2rem;
    }
    .stats-grid {
      grid-template-columns: 1fr;
    }
    .action-card {
      flex-direction: column;
      padding: 1.75rem;
    }
    .globe-container {
      max-width: 300px;
    }
  }
</style>

<div class="dashboard-container">
  <!-- Hero Section -->
  <div class="hero-panel">
    <!-- Left Hero: Headers and Counters -->
    <div class="hero-left">
      <h1 class="hero-title">
        Exploring Public Voice on AI
      </h1>
      <p class="hero-subtitle">
        How are people across the world engaged in dialogue about data and artificial intelligence? 
      </p>
      
      <!-- Stats Count-up Grid -->
      <div class="stats-grid">
        <div class="stat-card" data-target="{{ total_cases }}">
          <div class="stat-number">0</div>
          <div class="stat-label">Case Studies</div>
        </div>
        <div class="stat-card" data-target="{{ total_participants }}">
          <div class="stat-number">0</div>
          <div class="stat-label">Total Participants</div>
        </div>
        <div class="stat-card" data-target="{{ total_hours }}">
          <div class="stat-number">0</div>
          <div class="stat-label">Hours of input</div>
        </div>
        <div class="stat-card" data-target="{{ total_countries_count }}">
          <div class="stat-number">0</div>
          <div class="stat-label">Countries</div>
        </div>
      </div>
    </div>

    <!-- Right Hero: Spinning Globe -->
    <div class="hero-right">
      <div class="globe-container" id="globe-container">
        <canvas id="globe-canvas" width="380" height="380"></canvas>
      </div>
    </div>
  </div>

  <!-- Action Matrix (2x2 Grid) -->
  <div class="action-cards-grid">
    <!-- Discover Card -->
    <a href="{{ '/cases/' | relative_url }}" class="action-card">
      <div class="action-icon-wrapper">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
        </svg>
      </div>
      <div class="action-info">
        <h2 class="action-card-title">Browse cases</h2>
        <p class="action-card-description">
          Browse case studies of participatory AI projects, and find out about efforts to run informed and inclusive processes.
        </p>
        <span class="action-cta">
          View cases
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </span>
      </div>
    </a>

    <!-- Explore Map Card -->
    <a href="{{ '/map/' | relative_url }}" class="action-card">
      <div class="action-icon-wrapper">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
          <line x1="8" y1="2" x2="8" y2="18"></line>
          <line x1="16" y1="6" x2="16" y2="22"></line>
        </svg>
      </div>
      <div class="action-info">
        <h2 class="action-card-title">Explore map</h2>
        <p class="action-card-description">
          Open the interactive map to see the voices seeking to inform AI development, deployment and governance.
        </p>
        <span class="action-cta">
          Launch map
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </span>
      </div>
    </a>

    <!-- Watch Card -->
    <a href="{{ '/tools/' | relative_url }}" class="action-card">
      <div class="action-icon-wrapper">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="23 7 16 12 23 17 23 7"></polygon>
          <rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect>
        </svg>
      </div>
      <div class="action-info">
        <h2 class="action-card-title">Hear voices</h2>
        <p class="action-card-description">
          Look at the recommendations and issues raised in different processes, or watch videos sharing project processes and outcomes. 
        </p>
        <span class="action-cta">
          Expore
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </span>
      </div>
    </a>

    <!-- Contribute Card -->
    <a href="{{ '/get-involved/' | relative_url }}" class="action-card">
      <div class="action-icon-wrapper">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </div>
      <div class="action-info">
        <h2 class="action-card-title">Get involved</h2>
        <p class="action-card-description">
          Contribute your projects, find out about the Participatory AI Research & Practice Symposium, or learn how you can run your own process and support the citizens' track on AI.
        </p>
        <span class="action-cta">
          Get involved
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </span>
      </div>
    </a>
  </div>
</div>

<!-- 3D Canvas Rotating Globe script & Count-up Animation -->
<script>
document.addEventListener('DOMContentLoaded', () => {
  // 1. Live Stats Count-up logic
  const statCards = document.querySelectorAll('.stat-card');
  statCards.forEach(card => {
    const target = Math.round(parseFloat(card.getAttribute('data-target') || '0'));
    const numEl = card.querySelector('.stat-number');
    if (!numEl) return;

    let current = 0;
    const duration = 1500; // milliseconds
    const startTime = performance.now();

    function updateStats(timestamp) {
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease out cubic
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      current = Math.floor(easeProgress * target);
      
      numEl.textContent = current.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(updateStats);
      } else {
        numEl.textContent = target.toLocaleString();
      }
    }
    requestAnimationFrame(updateStats);
  });

  // 2. Rotating 3D Dot-matrix Globe
  const canvas = document.getElementById('globe-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  // Locations extracted dynamically via Jekyll
  const locations = [{{ unique_coords | join: "," }}] || [];

  let width = canvas.width;
  let height = canvas.height;
  let cx = width / 2;
  let cy = height / 2;
  let radius = Math.min(width, height) * 0.42;

  // Generate Fibonacci Sphere points (uniformly spaced)
  const points = [];
  const numPoints = 400;
  const phi = Math.PI * (3 - Math.sqrt(5)); // golden angle in radians

  for (let i = 0; i < numPoints; i++) {
    const y = 1 - (i / (numPoints - 1)) * 2; // y goes from 1 to -1
    const r = Math.sqrt(1 - y * y); // radius at y
    const theta = phi * i;
    const x = Math.cos(theta) * r;
    const z = Math.sin(theta) * r;
    points.push({ x, y, z });
  }

  // Map latitude/longitude to 3D sphere coordinate space
  const plottedPoints = locations.map(loc => {
    const radLat = (loc.lat * Math.PI) / 180;
    const radLng = (loc.lng * Math.PI) / 180;
    return {
      // Coordinate Math projection
      x: Math.cos(radLat) * Math.sin(radLng),
      y: -Math.sin(radLat),
      z: Math.cos(radLat) * Math.cos(radLng),
      name: loc.name,
      case: loc.case
    };
  });

  // Dual axis rotation: Y-axis (alpha) and X-axis (beta)
  let alpha = 0; // horizontal spin
  let beta = 0.2; // vertical tilt

  // Drag interaction states
  let isDragging = false;
  let previousMousePosition = { x: 0, y: 0 };
  
  let mouseX = -1000;
  let mouseY = -1000;
  let activeTooltip = null;

  // Projection math converting 3D sphere (x,y,z) to rotated coordinate space
  function project(p) {
    // 1. Rotate around Y-axis (alpha)
    const cosA = Math.cos(alpha);
    const sinA = Math.sin(alpha);
    const x1 = p.x * cosA - p.z * sinA;
    const z1 = p.x * sinA + p.z * cosA;
    const y1 = p.y;

    // 2. Rotate around X-axis (beta)
    const cosB = Math.cos(beta);
    const sinB = Math.sin(beta);
    const rx = x1;
    const ry = y1 * cosB - z1 * sinB;
    const rz = y1 * sinB + z1 * cosB;

    return {
      x: cx + rx * radius,
      y: cy + ry * radius,
      z: rz,
      name: p.name,
      case: p.case
    };
  }

  function drawGlobe() {
    ctx.clearRect(0, 0, width, height);

    // Auto rotate Y-axis slowly when NOT dragging
    if (!isDragging) {
      alpha += 0.0015;
    }

    // A. Draw subtle background atmosphere glow
    const radialGlow = ctx.createRadialGradient(cx, cy, radius * 0.5, cx, cy, radius * 1.15);
    radialGlow.addColorStop(0, 'rgba(73, 106, 64, 0.05)');
    radialGlow.addColorStop(1, 'rgba(246, 248, 245, 0)');
    ctx.fillStyle = radialGlow;
    ctx.beginPath();
    ctx.arc(cx, cy, radius * 1.15, 0, Math.PI * 2);
    ctx.fill();

    // B. Draw outer ring path
    ctx.strokeStyle = 'rgba(73, 106, 64, 0.12)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.stroke();

    const projectedGrid = points.map(project);
    const projectedCases = plottedPoints.map(project);

    // C. Draw rear hemisphere grid points (z < 0)
    ctx.fillStyle = 'rgba(73, 106, 64, 0.12)';
    projectedGrid.forEach(p => {
      if (p.z < 0) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 0.9, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // D. Draw rear hemisphere case coordinates (z < 0)
    ctx.fillStyle = 'rgba(73, 106, 64, 0.08)';
    projectedCases.forEach(p => {
      if (p.z < 0) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // E. Draw front hemisphere grid points (z >= 0)
    ctx.fillStyle = 'rgba(73, 106, 64, 0.35)';
    projectedGrid.forEach(p => {
      if (p.z >= 0) {
        ctx.beginPath();
        const size = 1 + p.z * 0.8;
        ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // F. Draw front hemisphere case coordinates (z >= 0)
    let closestCase = null;
    let minDistance = 12; // pixels limit for hover detection

    projectedCases.forEach(p => {
      if (p.z >= 0) {
        // Disable hover highlights when the user is actively dragging the globe
        const dist = isDragging ? 1000 : Math.hypot(p.x - mouseX, p.y - mouseY);

        // Highlight marker
        ctx.save();
        ctx.shadowColor = '#496a40';
        ctx.shadowBlur = 6;
        ctx.fillStyle = '#496a40';
        ctx.beginPath();
        const dotSize = 4 + p.z * 2.2;
        ctx.arc(p.x, p.y, dotSize, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Pulsing radar ring
        ctx.strokeStyle = 'rgba(73, 106, 64, 0.3)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        const pulseRadius = dotSize + 3.5 + Math.sin(Date.now() / 240) * 3;
        ctx.arc(p.x, p.y, pulseRadius, 0, Math.PI * 2);
        ctx.stroke();

        if (dist < minDistance) {
          minDistance = dist;
          closestCase = p;
        }
      }
    });

    // Tooltip handling state
    if (closestCase) {
      activeTooltip = closestCase;
    } else {
      activeTooltip = null;
    }

    // Render Tooltip box
    if (activeTooltip) {
      ctx.save();
      
      ctx.font = 'bold 11px "Outfit", sans-serif';
      const nameText = activeTooltip.name;
      const caseText = activeTooltip.case;
      
      const textWidth = Math.max(ctx.measureText(nameText).width, ctx.measureText(caseText).width) + 16;
      const textHeight = 34;

      // Safe Tooltip Positions: Prevent clipping outside canvas viewport
      let tx = activeTooltip.x + 12;
      let ty = activeTooltip.y - 12;
      
      // If tooltip clips on the right, render to the left of the marker
      if (tx + textWidth > width - 10) {
        tx = activeTooltip.x - textWidth - 12;
      }
      // If tooltip clips on the top, render below the marker
      if (ty - textHeight < 10) {
        ty = activeTooltip.y + textHeight + 12;
      }

      // Tooltip Card style
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = 'rgba(73, 106, 64, 0.25)';
      ctx.lineWidth = 1;
      
      // Shadow for light theme card
      ctx.shadowColor = 'rgba(0, 0, 0, 0.08)';
      ctx.shadowBlur = 10;
      ctx.shadowOffsetY = 4;

      ctx.beginPath();
      ctx.roundRect(tx, ty - textHeight, textWidth, textHeight + 6, 6);
      ctx.fill();
      ctx.stroke();

      ctx.shadowBlur = 0;
      ctx.shadowOffsetY = 0;

      // Draw text content
      ctx.fillStyle = '#1a2f16';
      ctx.fillText(nameText, tx + 8, ty - 21);
      ctx.font = '10px "Plus Jakarta Sans", sans-serif';
      ctx.fillStyle = '#496a40';
      ctx.fillText(caseText, tx + 8, ty - 8);

      ctx.restore();
    }

    requestAnimationFrame(drawGlobe);
  }

  // Mouse coordinate mapping for hover highlights
  canvas.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;
  });

  canvas.addEventListener('mouseleave', () => {
    mouseX = -1000;
    mouseY = -1000;
  });

  // Drag Interaction Handlers (Mouse)
  canvas.addEventListener('mousedown', e => {
    isDragging = true;
    previousMousePosition = { x: e.clientX, y: e.clientY };
  });

  window.addEventListener('mousemove', e => {
    if (!isDragging) return;
    const deltaX = e.clientX - previousMousePosition.x;
    const deltaY = e.clientY - previousMousePosition.y;

    alpha += deltaX * 0.005; // horizontal Y-spin
    beta += deltaY * 0.005;  // vertical X-tilt
    
    // Clamp vertical tilt to prevent flipping the poles upside down
    beta = Math.max(-Math.PI / 2.2, Math.min(Math.PI / 2.2, beta));

    previousMousePosition = { x: e.clientX, y: e.clientY };
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  // Drag Interaction Handlers (Touch for Mobile)
  canvas.addEventListener('touchstart', e => {
    if (e.touches.length === 1) {
      isDragging = true;
      previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }
  }, { passive: true });

  window.addEventListener('touchmove', e => {
    if (!isDragging || e.touches.length !== 1) return;
    const deltaX = e.touches[0].clientX - previousMousePosition.x;
    const deltaY = e.touches[0].clientY - previousMousePosition.y;

    alpha += deltaX * 0.005;
    beta += deltaY * 0.005;
    beta = Math.max(-Math.PI / 2.2, Math.min(Math.PI / 2.2, beta));

    previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  }, { passive: true });

  window.addEventListener('touchend', () => {
    isDragging = false;
  });

  // Start Animation
  requestAnimationFrame(drawGlobe);
});
</script>
