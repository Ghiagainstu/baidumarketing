const pptxgen = require("pptxgenjs");

// Website color scheme
const C = {
  brandBlue: "2563EB",      // Primary brand blue
  darkBlue: "1D4ED8",       // Hover/darker blue
  navy: "0F172A",           // Dark backgrounds
  white: "FFFFFF",
  lightGray: "F8FAFC",      // Light background
  midGray: "F1F5F9",        // Card backgrounds
  border: "E2E8F0",        // Borders
  text: "1E293B",           // Primary text
  textMuted: "64748B",      // Secondary text
  green: "10B981",          // Positive accents
  greenDark: "059669",
  gold: "F59E0B",           // Highlight accents
  red: "EF4444",            // Warning
};

const FONT = "Arial";
const FONT_BOLD = "Arial";

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Baidu PPC Pro";
pres.title = "Baidu PPC Pro — Your Bridge to China's Digital Ad Market";

// Helper: shadow factory
const makeShadow = () => ({
  type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08
});

// Helper: card shape
function addCard(slide, x, y, w, h, opts = {}) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: opts.fill || C.white },
    shadow: makeShadow(),
    line: { color: C.border, width: 0.5 }
  });
}

// Helper: stat callout
function addStat(slide, x, y, value, label, color) {
  slide.addText(value, {
    x, y, w: 2.2, h: 0.6,
    fontSize: 36, fontFace: FONT_BOLD, bold: true,
    color: color || C.brandBlue, align: "center", margin: 0
  });
  slide.addText(label, {
    x, y: y + 0.6, w: 2.2, h: 0.4,
    fontSize: 12, fontFace: FONT, color: C.textMuted, align: "center", margin: 0
  });
}

// ============================================================
// SLIDE 1: Title
// ============================================================
let s1 = pres.addSlide();
s1.background = { color: C.navy };

// Large title
s1.addText("Baidu PPC Pro", {
  x: 0.8, y: 1.2, w: 8.4, h: 1.2,
  fontSize: 44, fontFace: FONT_BOLD, bold: true,
  color: C.white, align: "left", margin: 0
});

// Subtitle
s1.addText("Your Bridge to China's 100 Billion Dollar Digital Ad Market", {
  x: 0.8, y: 2.4, w: 8.4, h: 0.7,
  fontSize: 20, fontFace: FONT, color: "CBD5E1", align: "left", margin: 0
});

// Accent line
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 3.3, w: 1.2, h: 0.06,
  fill: { color: C.brandBlue }
});

// Tagline
s1.addText("Compliance. Clarity. Zero Guesswork.", {
  x: 0.8, y: 3.6, w: 8.4, h: 0.5,
  fontSize: 16, fontFace: FONT, italic: true,
  color: C.textMuted, align: "left", margin: 0
});

// Bottom bar
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 5.1, w: 10, h: 0.525,
  fill: { color: C.brandBlue }
});
s1.addText("baidumarketing.com", {
  x: 0.8, y: 5.1, w: 8.4, h: 0.525,
  fontSize: 14, fontFace: FONT, color: C.white, align: "left", valign: "middle", margin: 0
});

// ============================================================
// SLIDE 2: Why BPP — The Problem & Our Solution
// ============================================================
let s2 = pres.addSlide();
s2.background = { color: C.white };

s2.addText("Why Baidu PPC Pro?", {
  x: 0.8, y: 0.4, w: 8.4, h: 0.7,
  fontSize: 32, fontFace: FONT_BOLD, bold: true,
  color: C.text, align: "left", margin: 0
});

// Problem section
s2.addText("The Challenge", {
  x: 0.8, y: 1.3, w: 4, h: 0.5,
  fontSize: 18, fontFace: FONT_BOLD, bold: true,
  color: C.red, align: "left", margin: 0
});

const problems = [
  "Foreign companies can't open Baidu ad accounts without a Chinese entity",
  "Complex compliance, document translation, and verification processes",
  "Cross-border payment and currency conversion barriers",
  "Language and cultural gaps in campaign management"
];

problems.forEach((p, i) => {
  s2.addText([
    { text: "✕  ", options: { color: C.red, bold: true, fontSize: 14 } },
    { text: p, options: { color: C.text, fontSize: 13 } }
  ], {
    x: 0.8, y: 1.9 + i * 0.45, w: 4.2, h: 0.42,
    fontFace: FONT, valign: "middle", margin: 0
  });
});

// Solution section
s2.addText("Our Solution", {
  x: 5.2, y: 1.3, w: 4, h: 0.5,
  fontSize: 18, fontFace: FONT_BOLD, bold: true,
  color: C.greenDark, align: "left", margin: 0
});

const solutions = [
  "Full account setup without a local Chinese entity",
  "We handle documents, translation, and compliance",
  "Accept international wire, SWIFT, 8 major currencies",
  "Bilingual team + AI-powered optimization"
];

solutions.forEach((s, i) => {
  s2.addText([
    { text: "✓  ", options: { color: C.green, bold: true, fontSize: 14 } },
    { text: s, options: { color: C.text, fontSize: 13 } }
  ], {
    x: 5.2, y: 1.9 + i * 0.45, w: 4.2, h: 0.42,
    fontFace: FONT, valign: "middle", margin: 0
  });
});

// Divider line
s2.addShape(pres.shapes.LINE, {
  x: 5.0, y: 1.5, w: 0, h: 2.5,
  line: { color: C.border, width: 1 }
});

// Stats at bottom
addCard(s2, 0.8, 3.9, 8.4, 1.2, { fill: C.lightGray });
addStat(s2, 1.0, 4.0, "500+", "Accounts Opened", C.brandBlue);
addStat(s2, 3.3, 4.0, "72h", "Avg. Activation", C.greenDark);
addStat(s2, 5.6, 4.0, "5.4x", "Avg. ROAS", C.gold);
addStat(s2, 7.9, 4.0, "25+", "Years Experience", C.brandBlue);

// ============================================================
// SLIDE 3: Account Opening
// ============================================================
let s3 = pres.addSlide();
s3.background = { color: C.white };

s3.addText("Baidu Account Opening", {
  x: 0.8, y: 0.4, w: 6, h: 0.7,
  fontSize: 32, fontFace: FONT_BOLD, bold: true,
  color: C.text, align: "left", margin: 0
});

s3.addText("Get your Baidu advertising account in 72 hours — no local entity required.", {
  x: 0.8, y: 1.1, w: 8.4, h: 0.5,
  fontSize: 15, fontFace: FONT, color: C.textMuted, align: "left", margin: 0
});

// Steps
const steps = [
  { num: "01", title: "Submit Request", desc: "Fill in your company info and requirements via our contact form." },
  { num: "02", title: "Document & Setup", desc: "Provide business documents. We handle translation, submission, and compliance review." },
  { num: "03", title: "Account Activated", desc: "Your Baidu account is verified and live within 72 hours." },
  { num: "04", title: "Campaign Live", desc: "Fund your account and start running ads on China's #1 search engine." }
];

steps.forEach((step, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = 0.8 + col * 4.4;
  const y = 1.9 + row * 1.5;

  addCard(s3, x, y, 4.0, 1.2);

  // Number badge
  s3.addShape(pres.shapes.RECTANGLE, {
    x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5,
    fill: { color: C.brandBlue }
  });
  s3.addText(step.num, {
    x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5,
    fontSize: 16, fontFace: FONT_BOLD, bold: true, color: C.white,
    align: "center", valign: "middle", margin: 0
  });

  s3.addText(step.title, {
    x: x + 0.85, y: y + 0.15, w: 3.0, h: 0.35,
    fontSize: 15, fontFace: FONT_BOLD, bold: true, color: C.text, margin: 0
  });
  s3.addText(step.desc, {
    x: x + 0.85, y: y + 0.5, w: 3.0, h: 0.6,
    fontSize: 12, fontFace: FONT, color: C.textMuted, margin: 0
  });
});

// Key stats
s3.addText("Key Metrics", {
  x: 0.8, y: 4.8, w: 2, h: 0.3,
  fontSize: 12, fontFace: FONT, bold: true, color: C.textMuted, margin: 0
});

const metrics = ["98% First-time pass rate", "500+ Accounts opened", "72h Average activation"];
metrics.forEach((m, i) => {
  s3.addText([
    { text: "▸ ", options: { color: C.brandBlue, bold: true } },
    { text: m, options: { color: C.text, fontSize: 12 } }
  ], {
    x: 0.8 + i * 3.1, y: 5.1, w: 2.9, h: 0.3,
    fontFace: FONT, margin: 0
  });
});

// ============================================================
// SLIDE 4: Budget Top-Up & Funding
// ============================================================
let s4 = pres.addSlide();
s4.background = { color: C.white };

s4.addText("Budget Top-Up & Funding", {
  x: 0.8, y: 0.4, w: 8, h: 0.7,
  fontSize: 32, fontFace: FONT_BOLD, bold: true,
  color: C.text, align: "left", margin: 0
});

s4.addText("Seamless international payments, credited within 1 business day.", {
  x: 0.8, y: 1.1, w: 8.4, h: 0.5,
  fontSize: 15, fontFace: FONT, color: C.textMuted, align: "left", margin: 0
});

// Left: Process
s4.addText("How It Works", {
  x: 0.8, y: 1.8, w: 4, h: 0.4,
  fontSize: 16, fontFace: FONT_BOLD, bold: true, color: C.text, margin: 0
});

const fundingSteps = [
  "Wire funds via international SWIFT transfer",
  "We convert at competitive FX rates",
  "Funds credited to your Baidu account (T+1)",
  "Full transaction receipt for your records"
];

fundingSteps.forEach((f, i) => {
  s4.addText([
    { text: `${i + 1}. `, options: { color: C.brandBlue, bold: true, fontSize: 14 } },
    { text: f, options: { color: C.text, fontSize: 13 } }
  ], {
    x: 0.8, y: 2.3 + i * 0.45, w: 4.2, h: 0.42,
    fontFace: FONT, valign: "middle", margin: 0
  });
});

// Right: Pricing card
addCard(s4, 5.4, 1.8, 4.0, 2.6, { fill: C.lightGray });

s4.addText("Pricing", {
  x: 5.6, y: 1.95, w: 3.6, h: 0.4,
  fontSize: 18, fontFace: FONT_BOLD, bold: true, color: C.text, align: "center", margin: 0
});

// Price rows
const priceData = [
  ["Standard", "2.5%", "From 2.5% on FX conversion"],
  ["Volume", "1.5%", "Discounts for larger budgets"],
  ["Minimum", "$0", "No minimum top-up required"]
];

priceData.forEach((p, i) => {
  const rowY = 2.5 + i * 0.6;
  s4.addText(p[0], {
    x: 5.6, y: rowY, w: 1.6, h: 0.3,
    fontSize: 12, fontFace: FONT, color: C.textMuted, margin: 0
  });
  s4.addText(p[1], {
    x: 7.2, y: rowY, w: 0.8, h: 0.3,
    fontSize: 16, fontFace: FONT_BOLD, bold: true, color: C.brandBlue, align: "right", margin: 0
  });
  s4.addText(p[2], {
    x: 5.6, y: rowY + 0.25, w: 3.6, h: 0.25,
    fontSize: 10, fontFace: FONT, color: C.textMuted, margin: 0
  });
});

// Supported currencies
s4.addText("Supported Currencies", {
  x: 0.8, y: 4.5, w: 3, h: 0.3,
  fontSize: 12, fontFace: FONT, bold: true, color: C.textMuted, margin: 0
});

const currencies = ["USD", "EUR", "GBP", "CNY", "JPY", "HKD", "SGD", "AUD"];
s4.addText(currencies.join("   "), {
  x: 0.8, y: 4.8, w: 8.4, h: 0.35,
  fontSize: 13, fontFace: FONT, color: C.brandBlue, bold: true, margin: 0
});

// ============================================================
// SLIDE 5: Campaign Management
// ============================================================
let s5 = pres.addSlide();
s5.background = { color: C.white };

s5.addText("Campaign Management", {
  x: 0.8, y: 0.4, w: 8, h: 0.7,
  fontSize: 32, fontFace: FONT_BOLD, bold: true,
  color: C.text, align: "left", margin: 0
});

s5.addText("Bilingual team + AI optimization to maximize your ROI.", {
  x: 0.8, y: 1.1, w: 8.4, h: 0.5,
  fontSize: 15, fontFace: FONT, color: C.textMuted, align: "left", margin: 0
});

// Service cards
const mgmtServices = [
  { title: "Keyword Research", desc: "Baidu-specific keyword tools to find high-intent, low-cost opportunities" },
  { title: "Ad Copy Creation", desc: "Native-level Chinese ad copywriting with cultural sensitivity" },
  { title: "Bidding & Optimization", desc: "oCPC smart bidding — pay for conversions, not clicks. CPC from ¥0.30" },
  { title: "A/B Testing", desc: "Weekly optimizations and creative testing to improve performance" },
  { title: "Performance Reports", desc: "Detailed monthly KPI breakdowns with actionable recommendations" },
  { title: "White-Label Support", desc: "Resell Baidu PPC under your own brand with our back-end support" }
];

mgmtServices.forEach((svc, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.8 + col * 3.0;
  const y = 1.8 + row * 1.6;

  addCard(s5, x, y, 2.7, 1.3);

  // Blue top accent
  s5.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 2.7, h: 0.06,
    fill: { color: C.brandBlue }
  });

  s5.addText(svc.title, {
    x: x + 0.2, y: y + 0.2, w: 2.3, h: 0.35,
    fontSize: 14, fontFace: FONT_BOLD, bold: true, color: C.text, margin: 0
  });
  s5.addText(svc.desc, {
    x: x + 0.2, y: y + 0.55, w: 2.3, h: 0.65,
    fontSize: 11, fontFace: FONT, color: C.textMuted, margin: 0
  });
});

// Performance stats
addCard(s5, 0.8, 4.8, 8.4, 0.7, { fill: C.lightGray });
s5.addText([
  { text: "Avg. ROAS  ", options: { color: C.textMuted, fontSize: 12 } },
  { text: "5.4x  ", options: { color: C.greenDark, fontSize: 16, bold: true } },
  { text: "    |    ", options: { color: C.border, fontSize: 12 } },
  { text: "Conversion +42%  ", options: { color: C.greenDark, fontSize: 12, bold: true } },
  { text: "    |    ", options: { color: C.border, fontSize: 12 } },
  { text: "CPC -18%  ", options: { color: C.brandBlue, fontSize: 12, bold: true } },
  { text: "    |    ", options: { color: C.border, fontSize: 12 } },
  { text: "Service from 6% of ad spend", options: { color: C.textMuted, fontSize: 12 } }
], {
  x: 1.0, y: 4.8, w: 8.0, h: 0.7,
  fontFace: FONT, valign: "middle", align: "center", margin: 0
});

// ============================================================
// SLIDE 6: Pricing Overview
// ============================================================
let s6 = pres.addSlide();
s6.background = { color: C.navy };

s6.addText("Transparent Pricing", {
  x: 0.8, y: 0.4, w: 8.4, h: 0.7,
  fontSize: 32, fontFace: FONT_BOLD, bold: true,
  color: C.white, align: "left", margin: 0
});

s6.addText("No hidden fees. Everything clearly listed.", {
  x: 0.8, y: 1.1, w: 8.4, h: 0.4,
  fontSize: 15, fontFace: FONT, color: "CBD5E1", align: "left", margin: 0
});

// Three pricing cards
const pricingCards = [
  {
    title: "Account Opening",
    price: "$100",
    unit: "one-time",
    features: [
      "Full account registration & verification",
      "Document translation & compliance",
      "72-hour activation (express available)",
      "English onboarding guide included"
    ],
    highlight: false
  },
  {
    title: "Budget Top-Up",
    price: "2.5%",
    unit: "from",
    features: [
      "International SWIFT wire transfers",
      "8 major currencies accepted",
      "T+1 crediting (same-day before 2PM CST)",
      "Volume discounts for larger budgets"
    ],
    highlight: true
  },
  {
    title: "Campaign Management",
    price: "6%",
    unit: "from ad spend",
    features: [
      "Bilingual team + AI optimization",
      "Keyword research & ad copywriting",
      "Weekly optimization & A/B testing",
      "Monthly performance reports"
    ],
    highlight: false
  }
];

pricingCards.forEach((card, i) => {
  const x = 0.8 + i * 3.05;
  const y = 1.8;
  const w = 2.8;
  const h = 3.5;

  const bgColor = card.highlight ? C.brandBlue : "1E293B";
  const borderColor = card.highlight ? C.brandBlue : "334155";

  // Card background
  s6.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: bgColor },
    line: { color: borderColor, width: 1 },
    shadow: makeShadow()
  });

  // Highlight badge
  if (card.highlight) {
    s6.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.3, y: y - 0.15, w: 1.6, h: 0.3,
      fill: { color: C.gold }
    });
    s6.addText("MOST POPULAR", {
      x: x + 0.3, y: y - 0.15, w: 1.6, h: 0.3,
      fontSize: 9, fontFace: FONT_BOLD, bold: true, color: C.navy,
      align: "center", valign: "middle", margin: 0
    });
  }

  // Title
  s6.addText(card.title, {
    x: x + 0.3, y: y + 0.35, w: w - 0.6, h: 0.4,
    fontSize: 16, fontFace: FONT_BOLD, bold: true,
    color: C.white, align: "center", margin: 0
  });

  // Price
  s6.addText(card.price, {
    x: x + 0.3, y: y + 0.85, w: w - 0.6, h: 0.7,
    fontSize: 36, fontFace: FONT_BOLD, bold: true,
    color: card.highlight ? C.gold : C.brandBlue, align: "center", margin: 0
  });
  s6.addText(card.unit, {
    x: x + 0.3, y: y + 1.5, w: w - 0.6, h: 0.3,
    fontSize: 12, fontFace: FONT,
    color: "94A3B8", align: "center", margin: 0
  });

  // Divider
  s6.addShape(pres.shapes.LINE, {
    x: x + 0.3, y: y + 2.0, w: w - 0.6, h: 0,
    line: { color: "334155", width: 0.5 }
  });

  // Features
  card.features.forEach((f, fi) => {
    s6.addText([
      { text: "✓  ", options: { color: C.green, bold: true, fontSize: 11 } },
      { text: f, options: { color: "CBD5E1", fontSize: 11 } }
    ], {
      x: x + 0.3, y: y + 2.15 + fi * 0.3, w: w - 0.6, h: 0.28,
      fontFace: FONT, margin: 0
    });
  });
});

// ============================================================
// SLIDE 7: Why Choose BPP — Differentiators
// ============================================================
let s7 = pres.addSlide();
s7.background = { color: C.white };

s7.addText("Why Choose Baidu PPC Pro?", {
  x: 0.8, y: 0.4, w: 8.4, h: 0.7,
  fontSize: 32, fontFace: FONT_BOLD, bold: true,
  color: C.text, align: "left", margin: 0
});

const differentiators = [
  { icon: "🏢", title: "No Local Entity Required", desc: "We handle compliance for foreign companies — WFOE, JV, RO, or any structure." },
  { icon: "⚡", title: "72-Hour Activation", desc: "Account verified and live in 3 business days. Express option available." },
  { icon: "🤖", title: "AI-Powered Optimization", desc: "Our AI reduces manual costs and passes the savings to you." },
  { icon: "💰", title: "Market-Lowest Fees", desc: "Top-up from 2.5%, management from 6%. No hidden charges." },
  { icon: "🌐", title: "Bilingual Support", desc: "Full English-Chinese support from Shanghai-based team with 25+ years experience." },
  { icon: "📊", title: "Transparent Reporting", desc: "Monthly KPI reports with clear breakdowns. You always know where your money goes." },
  { icon: "🔗", title: "oCPC Smart Bidding", desc: "Pay for conversions, not clicks. CPC from ¥0.30 with AI-optimized bids." },
  { icon: "🤝", title: "White-Label Ready", desc: "Resell Baidu PPC under your own brand. We handle the back-end." }
];

differentiators.forEach((d, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = 0.8 + col * 4.4;
  const y = 1.3 + row * 1.05;

  addCard(s7, x, y, 4.0, 0.9, { fill: C.lightGray });

  s7.addText(d.icon, {
    x: x + 0.15, y: y + 0.15, w: 0.6, h: 0.6,
    fontSize: 24, align: "center", valign: "middle", margin: 0
  });

  s7.addText(d.title, {
    x: x + 0.75, y: y + 0.1, w: 3.1, h: 0.35,
    fontSize: 14, fontFace: FONT_BOLD, bold: true, color: C.text, margin: 0
  });
  s7.addText(d.desc, {
    x: x + 0.75, y: y + 0.45, w: 3.1, h: 0.4,
    fontSize: 11, fontFace: FONT, color: C.textMuted, margin: 0
  });
});

// ============================================================
// SLIDE 8: Contact / CTA
// ============================================================
let s8 = pres.addSlide();
s8.background = { color: C.navy };

s8.addText("Ready to Enter China's", {
  x: 0.8, y: 1.0, w: 8.4, h: 0.7,
  fontSize: 36, fontFace: FONT_BOLD, bold: true,
  color: C.white, align: "center", margin: 0
});
s8.addText("Digital Ad Market?", {
  x: 0.8, y: 1.6, w: 8.4, h: 0.7,
  fontSize: 36, fontFace: FONT_BOLD, bold: true,
  color: C.brandBlue, align: "center", margin: 0
});

s8.addShape(pres.shapes.RECTANGLE, {
  x: 4.3, y: 2.5, w: 1.4, h: 0.06,
  fill: { color: C.brandBlue }
});

// CTA box
addCard(s8, 2.5, 2.8, 5.0, 2.0, { fill: "1E293B" });

s8.addText("Contact Us", {
  x: 2.5, y: 2.95, w: 5.0, h: 0.4,
  fontSize: 20, fontFace: FONT_BOLD, bold: true,
  color: C.white, align: "center", margin: 0
});

const contactInfo = [
  "✉  info@baidumarketing.com",
  "🌐  baidumarketing.com/contact",
  "💬  WhatsApp: +852 5237 0475"
];

contactInfo.forEach((c, i) => {
  s8.addText(c, {
    x: 2.5, y: 3.5 + i * 0.4, w: 5.0, h: 0.35,
    fontSize: 14, fontFace: FONT,
    color: "CBD5E1", align: "center", margin: 0
  });
});

// Button
s8.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 4.95, w: 3.0, h: 0.55,
  fill: { color: C.brandBlue }
});
s8.addText("Get Started →", {
  x: 3.5, y: 4.95, w: 3.0, h: 0.55,
  fontSize: 16, fontFace: FONT_BOLD, bold: true,
  color: C.white, align: "center", valign: "middle", margin: 0
});

// Footer
s8.addText("baidumarketing.com  |  Baidu PPC Pro", {
  x: 0.8, y: 5.2, w: 8.4, h: 0.3,
  fontSize: 10, fontFace: FONT, color: "64748B", align: "center", margin: 0
});

// ============================================================
// Write file
// ============================================================
pres.writeFile({ fileName: "BPP_Services_Introduction.pptx" })
  .then(() => console.log("PPT created: BPP_Services_Introduction.pptx"))
  .catch(err => console.error("Error:", err));
