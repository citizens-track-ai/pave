---
layout: default
title: Map
description: "Interactive global map of public AI voice and participatory engagement initiatives, visualising projects and democratic deliberations worldwide."
permalink: /map/
menus: [header]
menu_order: 2
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css" />
<script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>

<style>
/* Page content wrapper override for map */
.page-content .wrapper {
  max-width: 100% !important;
  width: 100% !important;
  padding-inline: 1rem !important;
  box-sizing: border-box !important;
}

/* Page Layout */
.map-alt-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2rem;
  margin-top: 1.5rem;
  margin-bottom: 3rem;
}

@media (max-width: 992px) {
  .map-alt-layout {
    grid-template-columns: 1fr;
  }
}

/* Sidebar Styling */
.map-sidebar {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
  align-self: start;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(73, 106, 64, 0.1);
  padding-bottom: 0.75rem;
}

.sidebar-header h2 {
  font-size: 1.25rem;
  margin: 0;
  font-weight: 700;
  color: #1a2f16;
}

.reset-btn {
  background: none;
  border: none;
  color: #496a40;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  transition: color 0.15s ease;
  text-decoration: underline;
}

.reset-btn:hover {
  color: #1a2f16;
}

/* Filter Sections */
.filter-section {
  margin-bottom: 1.5rem;
}

.filter-section:last-child {
  margin-bottom: 0;
}

.filter-section h3 {
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #556c50;
  margin-top: 0;
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Scrollbar for touchscreen and overflow scrollable facets */
.scrollable-facet {
  max-height: 210px; /* 5 items * 42px height */
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding-right: 6px;
  background: #fafbfa;
  border: 1px solid rgba(73, 106, 64, 0.05);
  border-radius: 10px;
  padding: 6px;
}

.scrollable-facet::-webkit-scrollbar {
  width: 6px;
}
.scrollable-facet::-webkit-scrollbar-track {
  background: rgba(73, 106, 64, 0.03);
  border-radius: 3px;
}
.scrollable-facet::-webkit-scrollbar-thumb {
  background: rgba(73, 106, 64, 0.25);
  border-radius: 3px;
}

.curation-filter-section {
  border-bottom: 1px solid rgba(73, 106, 64, 0.08);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.toggle-filter-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(73, 106, 64, 0.03);
  border: 1px solid rgba(73, 106, 64, 0.08);
  min-height: 44px;
}

.filter-label-toggle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  font-weight: 700;
  color: #243f1f;
  cursor: pointer;
  user-select: none;
  width: 100%;
}

.filter-label-toggle input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #496a40;
  cursor: pointer;
  margin: 0;
}

.tag-badge.curation-featured {
  background-color: rgba(36, 63, 31, 0.08);
  color: #243f1f;
}

.tag-badge.curation-full {
  background-color: rgba(73, 106, 64, 0.08);
  color: #496a40;
}

.tag-badge.curation-mapping {
  background-color: rgba(141, 163, 138, 0.12);
  color: #627760;
}

/* Custom DivIcon Marker Styling */
.custom-map-marker {
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-marker-pin {
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  border: 2.5px solid #ffffff;
  width: 100%;
  height: 100%;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

/* Accents per curation level (three shades of green aligned with site theme) */
.custom-marker-pin.marker-featured {
  background-color: #243f1f; /* Deep Forest Green */
  color: #ffffff;
  box-shadow: 0 4px 10px rgba(36, 63, 31, 0.4);
}

.custom-marker-pin.marker-featured:hover {
  transform: scale(1.15);
}

.custom-marker-pin.marker-full {
  background-color: #496a40; /* Brand Green */
  color: #ffffff;
  border-color: #ffffff;
  box-shadow: 0 2px 6px rgba(73, 106, 64, 0.3);
}

.custom-marker-pin.marker-mapping {
  background-color: #8da38a; /* Light Sage Green */
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.85);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
  opacity: 0.85;
}

.marker-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.marker-icon-wrapper svg {
  width: 55%;
  height: 55%;
  fill: currentColor;
  display: block;
}

.custom-marker-pin.marker-mapping .marker-icon-wrapper svg {
  width: 65%;
  height: 65%;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #243f1f;
  cursor: pointer;
  line-height: 1.4;
  user-select: none;
  padding: 8px 10px;
  border-radius: 8px;
  min-height: 40px; /* Touch target optimized */
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.filter-label:hover {
  background-color: rgba(73, 106, 64, 0.04);
}

.filter-label:active {
  background-color: rgba(73, 106, 64, 0.12); /* Touch response feedback */
}

.filter-label.active-checked {
  background-color: rgba(73, 106, 64, 0.08);
  border-color: rgba(73, 106, 64, 0.15);
  font-weight: 600;
}

.filter-label.zero-count {
  opacity: 0.45;
}

.filter-label.zero-count input {
  cursor: not-allowed;
}

.filter-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  accent-color: #496a40;
  cursor: pointer;
  flex-shrink: 0;
  margin: 0;
}

.filter-count {
  color: #7a9476;
  font-size: 0.75rem;
  margin-left: auto;
  font-weight: 500;
}

/* Dual Range Slider Styling */
.slider-wrapper {
  position: relative;
  width: 100%;
  height: 20px;
  margin-top: 15px;
  margin-bottom: 25px;
}

.slider-track {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 5px;
  background-color: rgba(73, 106, 64, 0.1);
  border-radius: 5px;
  transform: translateY(-50%);
  z-index: 1;
}

.slider-highlight {
  position: absolute;
  top: 50%;
  height: 5px;
  background-color: #496a40;
  border-radius: 5px;
  transform: translateY(-50%);
  z-index: 2;
}

.slider-wrapper input[type="range"] {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  background: none;
  pointer-events: none;
  -webkit-appearance: none;
  appearance: none;
  transform: translateY(-50%);
  z-index: 3;
  margin: 0;
}

.slider-wrapper input[type="range"]::-webkit-slider-thumb {
  height: 18px;
  width: 18px;
  border-radius: 50%;
  background-color: #496a40;
  border: 2px solid #ffffff;
  cursor: pointer;
  pointer-events: auto;
  -webkit-appearance: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
  transition: transform 0.1s ease;
}

.slider-wrapper input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.slider-wrapper input[type="range"]::-moz-range-thumb {
  height: 14px;
  width: 14px;
  border-radius: 50%;
  background-color: #496a40;
  border: 2px solid #ffffff;
  cursor: pointer;
  pointer-events: auto;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
  transition: transform 0.1s ease;
}

.slider-wrapper input[type="range"]::-moz-range-thumb:hover {
  transform: scale(1.15);
}

.slider-values {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  font-weight: 600;
  color: #496a40;
}

/* Statistics Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.08);
  border-top: 3px solid #496a40;
  border-radius: 12px;
  padding: 1rem 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.01);
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(73, 106, 64, 0.08);
}

/* Distinct card tops to look beautiful and premium */
.stat-card:nth-child(1) { border-top-color: #243f1f; } /* Deep Forest Green */
.stat-card:nth-child(2) { border-top-color: #496a40; } /* Brand Green */
.stat-card:nth-child(3) { border-top-color: #7a9476; } /* Muted Sage Green */
.stat-card:nth-child(4) { border-top-color: #8da38a; } /* Light Sage Green */
.stat-card:nth-child(5) { border-top-color: #243f1f; } /* Deep Forest Green */

.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card:nth-child(1) .stat-icon { background: rgba(36, 63, 31, 0.08); color: #243f1f; }
.stat-card:nth-child(2) .stat-icon { background: rgba(73, 106, 64, 0.08); color: #496a40; }
.stat-card:nth-child(3) .stat-icon { background: rgba(122, 148, 118, 0.08); color: #7a9476; }
.stat-card:nth-child(4) .stat-icon { background: rgba(141, 163, 138, 0.08); color: #8da38a; }
.stat-card:nth-child(5) .stat-icon { background: rgba(36, 63, 31, 0.08); color: #243f1f; }

.stat-icon svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-family: 'Outfit', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #1a2f16;
  line-height: 1.2;
}

.stat-label-text {
  font-size: 0.725rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #556c50;
  letter-spacing: 0.02em;
}

/* Map Styling */
.map-alt-container {
  height: 550px;
  width: 100%;
  border: 1px solid rgba(73, 106, 64, 0.12);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.02);
  overflow: hidden;
  margin-bottom: 2rem;
  z-index: 10;
}

/* Map Loader Spinner Overlay */
.map-loader-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 550px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(2.5px);
  -webkit-backdrop-filter: blur(2.5px);
  z-index: 1001;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 16px;
  border: 1px solid rgba(73, 106, 64, 0.12);
  transition: opacity 0.4s ease, visibility 0.4s ease;
}

@media (max-width: 768px) {
  .map-alt-container, .map-loader-overlay {
    height: 350px !important;
  }
}

.map-loader-overlay.fade-out {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.map-loader-spinner {
  width: 45px;
  height: 45px;
  border: 3.5px solid rgba(73, 106, 64, 0.15);
  border-left-color: #496a40;
  border-radius: 50%;
  animation: map-loader-spin 0.85s linear infinite;
}

@keyframes map-loader-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Dynamic Case Listing Section */
.cases-list-section {
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.01);
}

.cases-list-section h2 {
  font-size: 1.25rem;
  margin-top: 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(73, 106, 64, 0.08);
  padding-bottom: 0.5rem;
}

.cases-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.case-item-card {
  border: 1px solid rgba(73, 106, 64, 0.06);
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.15s ease;
  background: #fbfcfb;
}

.case-item-card:hover {
  border-color: rgba(73, 106, 64, 0.2);
  background: #ffffff;
  transform: translateX(3px);
}

.case-item-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex-grow: 1;
}

.case-item-title {
  font-weight: 700;
  font-size: 1rem;
  color: #1a2f16;
}

.case-item-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.775rem;
  color: #7a9476;
  flex-wrap: wrap;
}

.case-item-meta span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.tag-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.45rem;
  border-radius: 9999px;
  background-color: rgba(73, 106, 64, 0.08);
  color: #496a40;
}

.case-item-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
  min-width: 120px;
}

.case-stat-num {
  font-family: 'Outfit', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #496a40;
}

.case-stat-lbl {
  font-size: 0.675rem;
  text-transform: uppercase;
  color: #7a9476;
}

/* Map Controls Bar (Segmented control button group + cluster checkbox) */
.map-controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -1rem; /* push it close under the map container */
  margin-bottom: 2rem;
  padding: 0.75rem 1rem;
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.1);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.01);
  flex-wrap: wrap;
  gap: 1rem;
}

.location-view-toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.location-toggle-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #496a40;
  user-select: none;
  transition: color 0.2s ease;
}

/* Premium CSS Toggle Switch */
.switch-container {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
  margin: 0;
}

.switch-container input {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #496a40; /* Participant theme: Brand Green */
  transition: .3s;
  border-radius: 24px;
}

.switch-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

.switch-container input:checked + .switch-slider {
  background-color: #7a9476; /* Organisation theme: Muted Sage Green */
}

.switch-container input:checked + .switch-slider:before {
  transform: translateX(24px);
}

.cluster-toggle-wrapper label,
.shading-toggle-wrapper label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #496a40;
  cursor: pointer;
  user-select: none;
  min-height: 36px;
}

.cluster-toggle-wrapper input[type="checkbox"],
.shading-toggle-wrapper input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #496a40;
  cursor: pointer;
  margin: 0;
}

/* Custom Marker Cluster Styling (three shades of brand green) */
.marker-cluster-small {
  background-color: rgba(141, 163, 138, 0.4) !important;
}
.marker-cluster-small div {
  background-color: rgba(114, 140, 110, 0.85) !important;
  color: #ffffff !important;
  font-weight: 700;
}

.marker-cluster-medium {
  background-color: rgba(73, 106, 64, 0.4) !important;
}
.marker-cluster-medium div {
  background-color: rgba(73, 106, 64, 0.9) !important;
  color: #ffffff !important;
  font-weight: 700;
}

.marker-cluster-large {
  background-color: rgba(36, 63, 31, 0.4) !important;
}
.marker-cluster-large div {
  background-color: rgba(36, 63, 31, 0.95) !important;
  color: #ffffff !important;
  font-weight: 700;
}

.marker-cluster div {
  width: 30px;
  height: 30px;
  margin-left: 5px;
  margin-top: 5px;
  text-align: center;
  border-radius: 15px;
  font: 12px "Helvetica Neue", Arial, Helvetica, sans-serif;
}
.marker-cluster span {
  line-height: 30px;
}

.geojson-tooltip {
  background-color: #1a2f16 !important;
  color: #ffffff !important;
  border: 1px solid #496a40 !important;
  border-radius: 6px !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 0.85rem !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
  padding: 6px 10px !important;
  opacity: 0.95 !important;
}

/* Horizontal scale buttons */
.scale-horizontal-row {
  display: flex;
  justify-content: space-between;
  gap: 0.4rem;
  width: 100%;
  margin-top: 0.25rem;
}

.scale-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px 4px;
  background: #ffffff;
  border: 1.5px solid rgba(73, 106, 64, 0.12);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  text-align: center;
  min-height: 90px;
}

.scale-btn input[type="checkbox"] {
  display: none;
}

.scale-btn:hover {
  border-color: rgba(73, 106, 64, 0.35);
  background-color: rgba(73, 106, 64, 0.02);
}

.scale-btn.active-checked {
  background-color: rgba(73, 106, 64, 0.08);
  border-color: #496a40;
  box-shadow: 0 2px 8px rgba(73, 106, 64, 0.08);
}

.scale-btn.zero-count {
  opacity: 0.45;
}

.scale-icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(73, 106, 64, 0.05);
  color: #496a40;
  margin-bottom: 6px;
  transition: all 0.2s ease;
}

.scale-btn.active-checked .scale-icon-box {
  background: #496a40;
  color: #ffffff;
}

.scale-icon-box svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
}

.scale-label-text {
  font-size: 0.725rem;
  font-weight: 700;
  color: #243f1f;
  margin-bottom: 2px;
}

.scale-percentage {
  font-size: 0.675rem;
  font-weight: 600;
  color: #7a9476;
}

.scale-btn.active-checked .scale-percentage {
  color: #496a40;
}

/* Bottom filters section */
.bottom-filters-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
  margin-top: 0.75rem;
  margin-bottom: 1.25rem;
  background: #ffffff;
  border: 1px solid rgba(73, 106, 64, 0.08);
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.01);
}

.bottom-filter-box h3 {
  font-size: 0.8rem;
  font-weight: 700;
  color: #243f1f;
  margin-top: 0;
  margin-bottom: 0.35rem;
  border-bottom: 1px solid rgba(73, 106, 64, 0.08);
  padding-bottom: 0.15rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.checkbox-table-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.2rem 0.5rem;
}

.checkbox-table-grid .filter-label {
  font-size: 0.75rem;
  padding: 3px 5px;
  min-height: 24px;
  border-radius: 6px;
}

.checkbox-table-grid.scrollable-facet {
  height: 220px;
  overflow-y: auto;
  padding-right: 0.25rem;
  -webkit-overflow-scrolling: touch;
}

.checkbox-table-grid.theme-grid {
  grid-template-columns: 1fr;
  gap: 0.2rem;
  height: 220px;
  overflow-y: auto;
  padding-right: 0.25rem;
}

/* Map Wrapper & Floating Controls */
.map-wrapper {
  position: relative;
  width: 100%;
}

.map-floating-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(73, 106, 64, 0.15);
  border-radius: 8px;
  padding: 8px 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 190px;
}

.location-links-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #7a9476;
  border-bottom: 1.5px solid rgba(73, 106, 64, 0.08);
  padding-bottom: 6px;
  margin-bottom: 2px;
}

.location-link {
  background: none;
  border: none;
  padding: 0;
  font-family: inherit;
  font-size: inherit;
  font-weight: inherit;
  color: #7a9476;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.15s ease;
}

.location-link:hover {
  color: #496a40;
}

.location-link.active {
  color: #496a40;
  font-weight: 700;
  text-decoration: none;
}

.location-link-separator {
  color: rgba(73, 106, 64, 0.25);
  font-weight: normal;
  user-select: none;
}

.map-floating-controls .cluster-toggle-wrapper label,
.map-floating-controls .shading-toggle-wrapper label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #496a40;
  cursor: pointer;
  margin: 0;
  min-height: auto;
}

.map-floating-controls .cluster-toggle-wrapper input[type="checkbox"],
.map-floating-controls .shading-toggle-wrapper input[type="checkbox"] {
  width: 14px;
  height: 14px;
  margin: 0;
  accent-color: #496a40;
  cursor: pointer;
}


/* Sidebar Explanation Box */
.sidebar-explanation-box {
  background: rgba(73, 106, 64, 0.06);
  border: 1px solid rgba(73, 106, 64, 0.15);
  border-radius: 12px;
  padding: 1rem;
  font-size: 0.8rem;
  line-height: 1.45;
  color: #243f1f;
  margin-top: 1.5rem;
}
.sidebar-explanation-box p {
  margin: 0;
}
.sidebar-explanation-highlight {
  font-weight: 700;
  color: #496a40;
}

/* Sidebar Header Collapse Support */
.toggle-trigger {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  user-select: none;
}

.toggle-arrow-icon {
  display: none;
  width: 16px;
  height: 16px;
  fill: currentColor;
  transition: transform 0.25s ease;
}

@media (max-width: 992px) {
  .toggle-trigger {
    cursor: pointer;
    width: auto;
  }
  
  .toggle-arrow-icon {
    display: inline-block;
  }
  
  /* Collapsed state */
  .map-sidebar.collapsed-filters .filter-section,
  .map-sidebar.collapsed-filters .sidebar-explanation-box {
    display: none !important;
  }
  
  .map-sidebar.collapsed-filters .toggle-arrow-icon {
    transform: rotate(-90deg);
  }
}
</style>

<div class="map-alt-layout">
  <!-- Left Side Filters -->
  <aside class="map-sidebar">
    <!-- Print Brand Logo (hidden by default) -->
    <div class="sidebar-print-logo" style="display: none; padding: 0.5rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(73, 106, 64, 0.15);">
      <img src="{{ '/assets/images/pave-case-book-logo.png' | relative_url }}" alt="PAVE Case Book Logo" style="height: 42px; display: block; max-width: 100%;">
    </div>

    <div class="sidebar-header">
      <h2 id="sidebar-toggle-btn" class="toggle-trigger">
        Filters
        <svg class="toggle-arrow-icon" viewBox="0 0 24 24"><path d="M7 10l5 5 5-5z"/></svg>
      </h2>
      <button class="reset-btn" id="reset-all-btn">Reset All</button>
    </div>

    <!-- Case Type Curation Filter -->
    <div class="filter-section curation-filter-section">
      <div class="toggle-filter-wrapper">
        <label class="filter-label-toggle">
          <input type="checkbox" id="full-cases-only-toggle">
          Full cases only
        </label>
        <span class="filter-count" id="curation-facet-count">(0)</span>
      </div>
    </div>

    <!-- Participation by scale Filter -->
    <div class="filter-section scale-filter-section">
      <h3>Participation by scale</h3>
      <div class="scale-horizontal-row" id="level-filters">
        <!-- Community -->
        <label class="scale-btn" data-value="Community">
          <input type="checkbox" value="Community">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
          </span>
          <span class="scale-label-text">Community</span>
          <span class="scale-percentage">(0%)</span>
        </label>
        
        <!-- National -->
        <label class="scale-btn" data-value="National">
          <input type="checkbox" value="National">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.53c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.4z"/></svg>
          </span>
          <span class="scale-label-text">National</span>
          <span class="scale-percentage">(0%)</span>
        </label>

        <!-- Global -->
        <label class="scale-btn" data-value="Global">
          <input type="checkbox" value="Global">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95c-.32-1.25-.78-2.45-1.38-3.56 1.84.42 3.39 1.63 4.33 3.56zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.33-.14 2 0 .67.06 1.34.14 2H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56-1.84-.42-3.39-1.63-4.33-3.56zm2.95-8H5.08c.94-1.93 2.49-3.14 4.33-3.56-.6 1.11-1.06 2.31-1.38 3.56zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96zM14.26 14h-4.52c-.1-.66-.14-1.33-.14-2 0-.67.04-1.34.14-2h4.52c.1.66.14 1.33.14 2 0 .67-.04 1.34-.14 2zm.82 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95c-.94 1.93-2.49 3.14-4.33 3.56zm1.54-5.56c.08-.66.14-1.33.14-2 0-.67-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2h-3.38z"/></svg>
          </span>
          <span class="scale-label-text">Global</span>
          <span class="scale-percentage">(0%)</span>
        </label>
      </div>
    </div>

    <!-- Type of methods Filter -->
    <div class="filter-section scale-filter-section">
      <h3>Participation by method</h3>
      <div class="scale-horizontal-row" id="methodology-filters">
        <!-- Deliberation -->
        <label class="scale-btn" data-value="deliberation">
          <input type="checkbox" value="deliberation">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/></svg>
          </span>
          <span class="scale-label-text">Deliberation</span>
          <span class="scale-percentage">(0%)</span>
        </label>
        
        <!-- Participation -->
        <label class="scale-btn" data-value="participation">
          <input type="checkbox" value="participation">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 8 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
          </span>
          <span class="scale-label-text">Participation</span>
          <span class="scale-percentage">(0%)</span>
        </label>

        <!-- Research -->
        <label class="scale-btn" data-value="research">
          <input type="checkbox" value="research">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          </span>
          <span class="scale-label-text">Research</span>
          <span class="scale-percentage">(0%)</span>
        </label>
      </div>
    </div>

    <!-- Modality Filter -->
    <div class="filter-section scale-filter-section">
      <h3>Participation by location</h3>
      <div class="scale-horizontal-row" id="modality-filters">
        <!-- Offline -->
        <label class="scale-btn" data-value="Offline">
          <input type="checkbox" value="Offline">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
          </span>
          <span class="scale-label-text">Offline</span>
          <span class="scale-percentage">(0%)</span>
        </label>
        
        <!-- Online -->
        <label class="scale-btn" data-value="Online">
          <input type="checkbox" value="Online">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M20 18c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2H0v2h24v-2h-4zM4 6h16v10H4V6z"/></svg>
          </span>
          <span class="scale-label-text">Online</span>
          <span class="scale-percentage">(0%)</span>
        </label>

        <!-- Hybrid -->
        <label class="scale-btn" data-value="Hybrid">
          <input type="checkbox" value="Hybrid">
          <span class="scale-icon-box">
            <svg viewBox="0 0 24 24"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H8V4h12v12z"/></svg>
          </span>
          <span class="scale-label-text">Hybrid</span>
          <span class="scale-percentage">(0%)</span>
        </label>
      </div>
    </div>

    <!-- Explanation Box -->
    <div class="sidebar-explanation-box">
      <p>This map shows participants involved in <span class="sidebar-explanation-highlight" id="explanation-processes-count">82</span> processes that have taken place bringing participatory public inputs into aspects of AI-related research, development, deployment or governance. Processes might involve participants in more than one location, and many involve multiple methods. The data draws on submissions and desk research.</p>
    </div>
  </aside>

  <!-- Right Side Map & Stats -->
  <main class="map-main">
    <!-- Top Statistics Bar -->
    <div class="stats-grid">
      <!-- Mapped Cases Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-cases">0</span>
          <span class="stat-label-text">Participatory Processes</span>
        </div>
      </div>

      <!-- Total Engaged Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 8 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-participants">0</span>
          <span class="stat-label-text">Participants Engaged</span>
        </div>
      </div>
      
      <!-- Countries Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.53c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.4z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-countries">0</span>
          <span class="stat-label-text">Countries</span>
        </div>
      </div>

      <!-- Continents Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.53c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.4z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-continents">0</span>
          <span class="stat-label-text">Continents</span>
        </div>
      </div>

      <!-- Messages Card -->
      <div class="stat-card">
        <div class="stat-icon">
          <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/></svg>
        </div>
        <div class="stat-info">
          <span class="stat-number" id="stats-messages">0</span>
          <span class="stat-label-text">Recommendations & Issues</span>
        </div>
      </div>
    </div>

    <!-- Map Area Wrapper -->
    <div class="map-wrapper">
      <div id="map" class="map-alt-container"></div>

      <!-- Map Loading Spinner -->
      <div id="map-loader" class="map-loader-overlay">
        <div class="map-loader-spinner"></div>
      </div>

      <!-- Floating Map Controls Overlay (top-right of map) -->
      <div class="map-floating-controls">
        <div class="location-links-selector">
          <button type="button" class="location-link active" id="btn-show-participants">Participants</button>
          <span class="location-link-separator">|</span>
          <button type="button" class="location-link" id="btn-show-organisations">Organisations</button>
        </div>
        <div class="cluster-toggle-wrapper">
          <label>
            <input type="checkbox" id="map-cluster-toggle"> Cluster markers
          </label>
        </div>
        <div class="shading-toggle-wrapper">
          <label>
            <input type="checkbox" id="map-shading-toggle" checked> Country shading
          </label>
        </div>
      </div>
    </div>

    <!-- Methods & Theme Bottom Filters -->
    <div class="bottom-filters-section">
      <div class="bottom-filter-box">
        <h3>Methods</h3>
        <div class="checkbox-table-grid scrollable-facet" id="methods-filters">
          <!-- Dynamically populated and sorted -->
        </div>
      </div>

      <div class="bottom-filter-box">
        <h3>Theme</h3>
        <div class="checkbox-table-grid theme-grid" id="theme-filters">
          <label class="filter-label"><input type="checkbox" value="Artificial Intelligence"> Artificial Intelligence <span class="filter-count">(0)</span></label>
          <label class="filter-label"><input type="checkbox" value="Education"> Education <span class="filter-count">(0)</span></label>
          <label class="filter-label"><input type="checkbox" value="Environment"> Environment <span class="filter-count">(0)</span></label>
          <label class="filter-label"><input type="checkbox" value="Healthcare"> Healthcare <span class="filter-count">(0)</span></label>
          <label class="filter-label"><input type="checkbox" value="Infrastructure"> Infrastructure <span class="filter-count">(0)</span></label>
          <label class="filter-label"><input type="checkbox" value="Safety"> Safety <span class="filter-count">(0)</span></label>
          <label class="filter-label"><input type="checkbox" value="Work"> Work <span class="filter-count">(0)</span></label>
          <label class="filter-label"><input type="checkbox" value="Youth"> Youth <span class="filter-count">(0)</span></label>
        </div>
      </div>
    </div>

    <!-- Filtered Cases List Section -->
    <div class="cases-list-section">
      <h2 id="cases-count-header">Cases Mapped</h2>
      <div class="cases-grid" id="cases-grid-list">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </main>
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {


  // Collapsible Filters for Narrow Screens
  const sidebarToggleBtn = document.getElementById('sidebar-toggle-btn');
  const mapSidebar = document.querySelector('.map-sidebar');
  if (sidebarToggleBtn && mapSidebar) {
    // If narrow, default to collapsed on load
    if (window.innerWidth <= 992) {
      mapSidebar.classList.add('collapsed-filters');
    }
    
    sidebarToggleBtn.addEventListener('click', () => {
      if (window.innerWidth <= 992) {
        mapSidebar.classList.toggle('collapsed-filters');
      }
    });
  }

  // Print Mode URL parameter verification
  if (window.location.search.includes('print')) {
    const sidebarHeader = document.querySelector('.sidebar-header');
    const curationSection = document.querySelector('.curation-filter-section');
    const printLogo = document.querySelector('.sidebar-print-logo');
    if (sidebarHeader) sidebarHeader.style.display = 'none';
    if (curationSection) curationSection.style.display = 'none';
    if (printLogo) printLogo.style.display = 'block';
  }

  // 1. Initialise the Map

  const isMobile = window.innerWidth <= 768;
  const map = L.map('map', {
    minZoom: 1,
    maxZoom: 15
  }).setView([20, 0], isMobile ? 1 : 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  const markerClusterGroup = L.markerClusterGroup({
    showCoverageOnHover: false,
    maxClusterRadius: 40
  });

  const pointLayer = L.layerGroup();
  let geojsonData = null;
  let geojsonLayer = null;

  // 1b. Fetch GeoJSON for country heatmap
  fetch('https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson')
    .then(res => res.json())
    .then(data => {
      geojsonData = data;
      if (allCases.length > 0) {
        updateFiltersAndUI();
      }
    })
    .catch(err => console.error("Error loading GeoJSON for heatmap:", err));

  // Global variables to store loaded data
  let allCases = [];
  let methodCounts = {};
  let activeMapLayer = 'participants';
  
  // DOM References
  const methodsFiltersContainer = document.getElementById('methods-filters');
  const statsCases = document.getElementById('stats-cases');
  const statsCountries = document.getElementById('stats-countries');
  const statsContinents = document.getElementById('stats-continents');
  const statsParticipants = document.getElementById('stats-participants');
  const statsMessages = document.getElementById('stats-messages');
  const casesGridList = document.getElementById('cases-grid-list');
  const casesCountHeader = document.getElementById('cases-count-header');
  const resetBtn = document.getElementById('reset-all-btn');



  // 2. Fetch Aggregated Cases Data
  fetch('/assets/data/cases_aggregated.json')
    .then(response => response.json())
    .then(data => {
      allCases = data;
      
      // Compute methods occurrence frequency for sorting and counting
      computeMethodsFreq();

      // Listen for checkbox changes (including 'Full cases only' toggle)
      document.querySelectorAll('.filter-section input[type="checkbox"], .bottom-filters-section input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateFiltersAndUI);
      });

      // Listen for location link selectors
      const btnShowParticipants = document.getElementById('btn-show-participants');
      const btnShowOrganisations = document.getElementById('btn-show-organisations');
      
      btnShowParticipants.addEventListener('click', () => {
        activeMapLayer = 'participants';
        btnShowParticipants.classList.add('active');
        btnShowOrganisations.classList.remove('active');
        updateFiltersAndUI();
      });
      
      btnShowOrganisations.addEventListener('click', () => {
        activeMapLayer = 'organisations';
        btnShowOrganisations.classList.add('active');
        btnShowParticipants.classList.remove('active');
        updateFiltersAndUI();
      });

      // Listen for cluster and shading checkboxes
      document.getElementById('map-cluster-toggle').addEventListener('change', updateFiltersAndUI);
      document.getElementById('map-shading-toggle').addEventListener('change', updateFiltersAndUI);

      // Initial filter run (draws everything)
      updateFiltersAndUI();
    })
    .catch(error => {
      console.error("Error loading aggregated cases:", error);
    });

  // Reset Button logic
  resetBtn.addEventListener('click', () => {
    // Uncheck all sidebar and bottom checkboxes
    document.querySelectorAll('.map-sidebar input[type="checkbox"], .bottom-filters-section input[type="checkbox"]').forEach(cb => cb.checked = false);
    
    // Reset map controls
    document.getElementById('map-cluster-toggle').checked = false;
    document.getElementById('map-shading-toggle').checked = true;
    
    activeMapLayer = 'participants';
    document.getElementById('btn-show-participants').classList.add('active');
    document.getElementById('btn-show-organisations').classList.remove('active');

    updateFiltersAndUI();
  });

  // 3. Methods aggregation
  function computeMethodsFreq() {
    methodCounts = {};
    allCases.forEach(c => {
      if (c.methods && Array.isArray(c.methods)) {
        c.methods.forEach(m => {
          methodCounts[m] = (methodCounts[m] || 0) + 1;
        });
      }
    });
  }

  // 3a. Update Fixed Facet Labels (Modality, Level, Theme)
  function updateFixedFacetLabels(containerId, countMap) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const labels = container.querySelectorAll('.filter-label');
    labels.forEach(label => {
      const input = label.querySelector('input');
      const value = input.value;
      const count = countMap[value] || 0;
      
      const countSpan = label.querySelector('.filter-count');
      if (countSpan) {
        countSpan.innerText = '(' + count + ')';
      }
      
      if (input.checked) {
        label.classList.add('active-checked');
      } else {
        label.classList.remove('active-checked');
      }
      
      if (count === 0) {
        label.classList.add('zero-count');
      } else {
        label.classList.remove('zero-count');
      }
    });
  }

  // 3b. Render Methods checkboxes dynamically (sorted, count-filtered, touchscreen-optimized)
  function updateMethodsCheckboxes(activeCounts, selectedMethods) {
    const methodsToRender = [];
    const allMethodNames = new Set([...Object.keys(methodCounts), ...selectedMethods]);
    
    allMethodNames.forEach(m => {
      const count = activeCounts[m] || 0;
      const isChecked = selectedMethods.includes(m);
      // Hide methods with count 0 unless they are checked
      if (count > 0 || isChecked) {
        methodsToRender.push({ name: m, count: count, checked: isChecked });
      }
    });

    // Sort: checked ones first, then by count descending, then alphabetical
    methodsToRender.sort((a, b) => {
      if (a.checked !== b.checked) {
        return a.checked ? -1 : 1;
      }
      if (b.count !== a.count) {
        return b.count - a.count;
      }
      return a.name.localeCompare(b.name);
    });

    methodsFiltersContainer.innerHTML = '';
    methodsToRender.forEach(method => {
      const label = document.createElement('label');
      label.className = 'filter-label' + (method.checked ? ' active-checked' : '') + (method.count === 0 ? ' zero-count' : '');
      
      const input = document.createElement('input');
      input.type = 'checkbox';
      input.value = method.name;
      input.checked = method.checked;
      input.addEventListener('change', updateFiltersAndUI);

      const spanText = document.createTextNode(' ' + method.name);
      
      const countSpan = document.createElement('span');
      countSpan.className = 'filter-count';
      countSpan.innerText = '(' + method.count + ')';

      label.appendChild(input);
      label.appendChild(spanText);
      label.appendChild(countSpan);
      
      methodsFiltersContainer.appendChild(label);
    });

    // Adjust scrollable class dynamically
    if (methodsToRender.length > 5) {
      methodsFiltersContainer.classList.add('scrollable-facet');
    } else {
      methodsFiltersContainer.classList.remove('scrollable-facet');
    }
  }

  // 3d. Update Scale Facet Labels as percentages
  function updateScalePercentageLabels(containerId, countMap, totalCount) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const buttons = container.querySelectorAll('.scale-btn');
    buttons.forEach(btn => {
      const input = btn.querySelector('input');
      const value = input.value;
      const count = countMap[value] || 0;
      
      const pct = totalCount > 0 ? Math.round((count / totalCount) * 100) : 0;
      const pctSpan = btn.querySelector('.scale-percentage');
      if (pctSpan) {
        pctSpan.innerText = '(' + pct + '%)';
      }
      
      if (input.checked) {
        btn.classList.add('active-checked');
      } else {
        btn.classList.remove('active-checked');
      }
      
      if (count === 0) {
        btn.classList.add('zero-count');
      } else {
        btn.classList.remove('zero-count');
      }
    });
  }



  // 5. Filter application
  function updateFiltersAndUI() {
    // Collect active filter choices
    const fullCasesOnly = document.getElementById('full-cases-only-toggle').checked;
    const selectedMods = Array.from(document.querySelectorAll('#modality-filters input:checked')).map(cb => cb.value);
    const selectedLevels = Array.from(document.querySelectorAll('#level-filters input:checked')).map(cb => cb.value);
    const selectedMethodsCats = Array.from(document.querySelectorAll('#methodology-filters input:checked')).map(cb => cb.value);
    const selectedThemes = Array.from(document.querySelectorAll('#theme-filters input:checked')).map(cb => cb.value);
    const selectedMethods = Array.from(document.querySelectorAll('#methods-filters input:checked')).map(cb => cb.value);
 
    // Helpers to check match
    const matchesCuration = (c) => !fullCasesOnly || (c.curation_decision === 'Featured Full Case' || c.curation_decision === 'Full Case');
    const matchesModality = (c, mods) => mods.length === 0 || (c.modalities && c.modalities.some(m => mods.includes(m)));
    const matchesLevel = (c, levels) => levels.length === 0 || levels.includes(c.level_of_engagement);
    const matchesMethodCategory = (c, cats) => cats.length === 0 || (c.method_categories && c.method_categories.some(cat => cats.includes(cat)));
    const matchesTheme = (c, themes) => themes.length === 0 || (c.themes && c.themes.some(t => themes.includes(t)));
    const matchesMethod = (c, meths) => meths.length === 0 || (c.methods && c.methods.some(m => meths.includes(m)));
 
    // Filter Cases Array (Matches all filters)
    const filteredCases = allCases.filter(c => 
      matchesCuration(c) &&
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesMethodCategory(c, selectedMethodsCats) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods)
    );

    // --- ORTHOGONAL FACET COUNTS ---

    // 0. Curation Toggle count (shows count of Featured/Full cases matching other active filters)
    const casesForCuration = allCases.filter(c =>
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesMethodCategory(c, selectedMethodsCats) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods)
    );
    const fullCasesCount = casesForCuration.filter(c => c.curation_decision === 'Featured Full Case' || c.curation_decision === 'Full Case').length;
    document.getElementById('curation-facet-count').innerText = '(' + fullCasesCount + ')';

    // 1. Modality counts (ignore Modality filter)
    const casesForModality = allCases.filter(c =>
      matchesCuration(c) &&
      matchesLevel(c, selectedLevels) &&
      matchesMethodCategory(c, selectedMethodsCats) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods)
    );
    const modalityCounts = { "Offline": 0, "Online": 0, "Hybrid": 0 };
    casesForModality.forEach(c => {
      if (c.modalities) {
        c.modalities.forEach(m => {
          if (m in modalityCounts) modalityCounts[m]++;
        });
      }
    });

    // 2. Level counts (ignore Level filter)
    const casesForLevel = allCases.filter(c =>
      matchesCuration(c) &&
      matchesModality(c, selectedMods) &&
      matchesMethodCategory(c, selectedMethodsCats) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods)
    );
    const levelCounts = { "Community": 0, "National": 0, "Professional": 0, "Global": 0 };
    casesForLevel.forEach(c => {
      if (c.level_of_engagement in levelCounts) {
        levelCounts[c.level_of_engagement]++;
      }
    });

    // 2b. Methodology counts (ignore Methodology filter)
    const casesForMethodology = allCases.filter(c =>
      matchesCuration(c) &&
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesTheme(c, selectedThemes) &&
      matchesMethod(c, selectedMethods)
    );
    const methodologyCounts = { "deliberation": 0, "participation": 0, "research": 0 };
    casesForMethodology.forEach(c => {
      if (c.method_categories) {
        c.method_categories.forEach(cat => {
          if (cat in methodologyCounts) {
            methodologyCounts[cat]++;
          }
        });
      }
    });

    // 3. Theme counts (ignore Theme filter)
    const casesForTheme = allCases.filter(c =>
      matchesCuration(c) &&
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesMethodCategory(c, selectedMethodsCats) &&
      matchesMethod(c, selectedMethods)
    );
    const themeCounts = {
      "Artificial Intelligence": 0, "Education": 0, "Environment": 0,
      "Healthcare": 0, "Infrastructure": 0, "Safety": 0, "Work": 0, "Youth": 0
    };
    casesForTheme.forEach(c => {
      if (c.themes) {
        c.themes.forEach(t => {
          if (t in themeCounts) themeCounts[t]++;
        });
      }
    });

    // 4. Method counts (ignore Method filter)
    const casesForMethod = allCases.filter(c =>
      matchesCuration(c) &&
      matchesModality(c, selectedMods) &&
      matchesLevel(c, selectedLevels) &&
      matchesMethodCategory(c, selectedMethodsCats) &&
      matchesTheme(c, selectedThemes)
    );
    const activeMethodCounts = {};
    casesForMethod.forEach(c => {
      if (c.methods) {
        c.methods.forEach(m => {
          activeMethodCounts[m] = (activeMethodCounts[m] || 0) + 1;
        });
      }
    });

    // Update checkbox labels & dynamic lists
    updateScalePercentageLabels('modality-filters', modalityCounts, casesForModality.length);
    updateScalePercentageLabels('level-filters', levelCounts, casesForLevel.length);
    updateScalePercentageLabels('methodology-filters', methodologyCounts, casesForMethodology.length);
    updateFixedFacetLabels('theme-filters', themeCounts);
    updateMethodsCheckboxes(activeMethodCounts, selectedMethods);

    // Update Stats, Map, and Case list
    updateStatistics(filteredCases);
    updateMapPoints(filteredCases);
    updateCaseListUI(filteredCases);

    // Hide loader overlay
    const mapLoader = document.getElementById('map-loader');
    if (mapLoader) {
      mapLoader.classList.add('fade-out');
    }
  }

  function updateStatistics(filteredCases) {
    const countriesSet = new Set();
    const continentsSet = new Set();
    let totalParticipantsCount = 0;
    let totalMessagesCount = 0;

    filteredCases.forEach(c => {
      if (c.countries) c.countries.forEach(co => countriesSet.add(co));
      if (c.continents) c.continents.forEach(con => continentsSet.add(con));
      totalParticipantsCount += c.total_participants || 0;
      totalMessagesCount += c.message_count || 0;
    });

    // Animate stats counter transitions for a premium look
    animateCounter(statsCases, filteredCases.length);
    animateCounter(statsParticipants, totalParticipantsCount, '> ');
    animateCounter(statsCountries, countriesSet.size);
    animateCounter(statsContinents, continentsSet.size);
    animateCounter(statsMessages, totalMessagesCount, '> ');

    // Update explanation box dynamic process count
    const explanationCountSpan = document.getElementById('explanation-processes-count');
    if (explanationCountSpan) {
      explanationCountSpan.innerText = filteredCases.length;
    }
  }

  function animateCounter(element, targetValue, prefix = '') {
    const startVal = parseInt(element.innerText.replace(/[^0-9]/g, '')) || 0;
    if (startVal === targetValue) {
      element.innerText = prefix + targetValue.toLocaleString();
      return;
    }
    
    const duration = 400; // ms
    const startTime = performance.now();

    function step(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease out cubic
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const currentVal = Math.floor(startVal + easeProgress * (targetValue - startVal));
      
      element.innerText = prefix + currentVal.toLocaleString();

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        element.innerText = prefix + targetValue.toLocaleString();
      }
    }
    requestAnimationFrame(step);
  }

  function updateMapPoints(filteredCases) {
    // Clear both layers
    markerClusterGroup.clearLayers();
    pointLayer.clearLayers();

    // Get current map settings
    const mapLayerView = activeMapLayer;
    const clusterMarkers = document.getElementById('map-cluster-toggle').checked;

    const bounds = L.latLngBounds();
    let pointCount = 0;

    // SVG icon helper by curation type
    function getCurationIconSvg(decision) {
      if (decision === 'Featured Full Case') {
        // Star
        return `<svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
      } else if (decision === 'Full Case') {
        // Magnifying Glass
        return `<svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>`;
      } else {
        // Map Pin
        return `<svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>`;
      }
    }

    filteredCases.forEach(c => {
      const decision = c.curation_decision || 'Mapping Entry';
      let badgeClass = 'mapping';
      let size = 18;
      if (decision === 'Featured Full Case') {
        badgeClass = 'featured';
        size = 36;
      } else if (decision === 'Full Case') {
        badgeClass = 'full';
        size = 26;
      }

      const svgIcon = getCurationIconSvg(decision);

      // Render Participant points
      if (mapLayerView === 'participants' && c.participants) {
        c.participants.forEach(part => {
          if (!part.locations) return;
          part.locations.forEach(loc => {
            const iconHtml = `
              <div class="custom-marker-pin marker-${badgeClass} marker-type-participants">
                <span class="marker-icon-wrapper">${svgIcon}</span>
              </div>
            `;
            const customIcon = L.divIcon({
              className: 'custom-map-marker',
              html: iconHtml,
              iconSize: [size, size],
              iconAnchor: [size / 2, size / 2]
            });
            const marker = L.marker([loc.lat, loc.lng], { icon: customIcon });

            const countVal = part.count ? String(part.count).trim() : '';
            const parsedCount = parseInt(countVal.replace(/,/g, ''));
            const countText = (!isNaN(parsedCount)) ? `<strong>${parsedCount.toLocaleString()}</strong> people` : 'Participants';
            
            const locations = part.locations_list ? part.locations_list.split(',').map(s => s.trim()).filter(Boolean) : [];
            let popupText = '';
            
            if (locations.length > 5) {
              const markerCountry = loc.location_name || '';
              const otherCountries = locations.filter(name => name !== markerCountry);
              const firstFourOthers = otherCountries.slice(0, 4);
              const remainingCount = otherCountries.length - firstFourOthers.length;
              const pluralSuffix = remainingCount === 1 ? 'country' : 'countries';
              
              const countriesText = `${markerCountry ? `<strong>${markerCountry}</strong>` : ''}${firstFourOthers.length > 0 ? `, ${firstFourOthers.map(cc => `<strong>${cc}</strong>`).join(', ')}` : ''}, and <strong>${remainingCount}</strong> more ${pluralSuffix}`;
              
              popupText = `${countText} took part in this process on AI in ${countriesText} through <a href="${c.url}"><strong>${c.title}</strong></a>.`;
            } else {
              popupText = `${countText} took part in a participatory process on AI in <strong>${part.locations_list}</strong> through <a href="${c.url}"><strong>${c.title}</strong></a>.`;
            }

            marker.bindPopup(popupText);
            
            if (clusterMarkers) {
              markerClusterGroup.addLayer(marker);
            } else {
              pointLayer.addLayer(marker);
            }
            
            bounds.extend([loc.lat, loc.lng]);
            pointCount++;
          });
        });
      }

      // Render Organisation points
      if (mapLayerView === 'organisations' && c.organisations) {
        c.organisations.forEach(org => {
          if (!org.locations) return;
          org.locations.forEach(loc => {
            const iconHtml = `
              <div class="custom-marker-pin marker-${badgeClass} marker-type-organisation">
                <span class="marker-icon-wrapper">${svgIcon}</span>
              </div>
            `;
            const customIcon = L.divIcon({
              className: 'custom-map-marker',
              html: iconHtml,
              iconSize: [size, size],
              iconAnchor: [size / 2, size / 2]
            });
            const marker = L.marker([loc.lat, loc.lng], { icon: customIcon });

            const popupText = `<strong>Lead Organisation:</strong> <a href="${org.url}"><strong>${org.title}</strong></a><br>Lead organiser for <a href="${c.url}">${c.title}</a>.`;

            marker.bindPopup(popupText);
            
            if (clusterMarkers) {
              markerClusterGroup.addLayer(marker);
            } else {
              pointLayer.addLayer(marker);
            }
            
            bounds.extend([loc.lat, loc.lng]);
            pointCount++;
          });
        });
      }
    });

    // Ensure only the active layer group is attached to the map
    map.removeLayer(markerClusterGroup);
    map.removeLayer(pointLayer);

    if (clusterMarkers) {
      map.addLayer(markerClusterGroup);
    } else {
      map.addLayer(pointLayer);
    }

    // Auto-fit bounds if we have points
    if (pointCount > 0) {
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 12 });
    }

    // Render the heatmap layer behind markers
    updateHeatmap(filteredCases);
  }

  function updateHeatmap(filteredCases) {
    const showShading = document.getElementById('map-shading-toggle').checked;

    // If layer already exists, remove it from map
    if (geojsonLayer) {
      map.removeLayer(geojsonLayer);
    }

    if (!showShading || !geojsonData) return;

    // Calculate country counts from filteredCases
    const countryCounts = {};
    filteredCases.forEach(c => {
      if (c.countries) {
        c.countries.forEach(code => {
          const upperCode = code.toUpperCase();
          countryCounts[upperCode] = (countryCounts[upperCode] || 0) + 1;
        });
      }
    });

    // Helper to get green scale colors
    function getCountryColor(count) {
      if (!count || count === 0) return 'transparent';
      if (count === 1) return '#8da38a'; // Sage Green
      if (count === 2) return '#496a40'; // Brand Green
      return '#243f1f'; // Deep Forest Green
    }

    // Recreate geojson layer with active styles
    geojsonLayer = L.geoJson(geojsonData, {
      style: function(feature) {
        const code = (feature.properties.ISO_A2 || feature.properties.iso_a2 || '').toUpperCase();
        const count = countryCounts[code] || 0;
        return {
          fillColor: getCountryColor(count),
          weight: count > 0 ? 1 : 0.5,
          opacity: count > 0 ? 0.7 : 0.15,
          color: '#ffffff',
          fillOpacity: count > 0 ? 0.45 + Math.min(count * 0.08, 0.35) : 0
        };
      },
      onEachFeature: function(feature, layer) {
        const code = (feature.properties.ISO_A2 || feature.properties.iso_a2 || '').toUpperCase();
        const count = countryCounts[code] || 0;
        const countryName = feature.properties.NAME || feature.properties.name || code;
        if (count > 0) {
          layer.bindTooltip(`<strong>${countryName}</strong>: ${count} case${count === 1 ? '' : 's'}`, {
            sticky: true,
            className: 'geojson-tooltip'
          });
        }
      }
    });

    geojsonLayer.addTo(map);
    geojsonLayer.bringToBack();
  }

  function updateCaseListUI(filteredCases) {
    casesCountHeader.innerText = filteredCases.length + ' Participatory Processes Mapped';
    casesGridList.innerHTML = '';

    if (filteredCases.length === 0) {
      casesGridList.innerHTML = '<div style="color: #7a9476; text-align: center; padding: 2rem; font-style: italic;">No cases match the selected filters. Click "Reset All" to clear filters.</div>';
      return;
    }

    filteredCases.forEach(c => {
      const card = document.createElement('div');
      card.className = 'case-item-card';

      const details = document.createElement('div');
      details.className = 'case-item-details';

      const titleLink = document.createElement('a');
      titleLink.href = c.url;
      titleLink.className = 'case-item-title';
      titleLink.innerText = c.title;
      details.appendChild(titleLink);

      const meta = document.createElement('div');
      meta.className = 'case-item-meta';

      // Case Type badge
      const curationVal = c.curation_decision || 'Mapping Entry';
      let badgeClass = 'mapping';
      let badgeLabel = 'Mapping';
      if (curationVal === 'Featured Full Case') {
        badgeClass = 'featured';
        badgeLabel = 'Featured';
      } else if (curationVal === 'Full Case') {
        badgeClass = 'full';
        badgeLabel = 'Full Case';
      }

      const curationSpan = document.createElement('span');
      curationSpan.innerHTML = `<span class="tag-badge curation-${badgeClass}">${badgeLabel}</span>`;
      meta.appendChild(curationSpan);

      // Level badge
      if (c.level_of_engagement) {
        const levelSpan = document.createElement('span');
        levelSpan.innerHTML = `<span class="tag-badge">${c.level_of_engagement} Scope</span>`;
        meta.appendChild(levelSpan);
      }

      // Modalities list
      if (c.modalities && c.modalities.length > 0) {
        const modalitiesSpan = document.createElement('span');
        modalitiesSpan.innerText = 'Modality: ' + c.modalities.join(', ');
        meta.appendChild(modalitiesSpan);
      }

      // Themes tags
      if (c.themes && c.themes.length > 0) {
        const themesSpan = document.createElement('span');
        themesSpan.innerText = 'Theme: ' + c.themes.join(', ');
        meta.appendChild(themesSpan);
      }

      details.appendChild(meta);
      card.appendChild(details);

      const stats = document.createElement('div');
      stats.className = 'case-item-stats';

      if (c.total_participants > 0) {
        const pNum = document.createElement('div');
        pNum.className = 'case-stat-num';
        pNum.innerText = c.total_participants.toLocaleString();
        
        const pLbl = document.createElement('div');
        pLbl.className = 'case-stat-lbl';
        pLbl.innerText = 'Participants';
        
        stats.appendChild(pNum);
        stats.appendChild(pLbl);
      } else {
        const pNum = document.createElement('div');
        pNum.className = 'case-stat-num';
        pNum.style.color = '#7a9476';
        pNum.innerText = '-';
        
        const pLbl = document.createElement('div');
        pLbl.className = 'case-stat-lbl';
        pLbl.innerText = 'Participants';
        
        stats.appendChild(pNum);
        stats.appendChild(pLbl);
      }

      card.appendChild(stats);
      casesGridList.appendChild(card);
    });
  }
});
</script>
