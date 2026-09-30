const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

async function createVinamilkDeck() {
  const pres = new pptxgen();
  
  // Explicitly set 16:9 widescreen layout (13.333 x 7.5 inches)
  pres.defineLayout({ name: 'LAYOUT_16x9_WIDE', width: 13.333, height: 7.5 });
  pres.layout = 'LAYOUT_16x9_WIDE';
  pres.author = 'Pham Minh Hoang';
  pres.company = 'Vinamilk Internship Applicant';
  pres.title = 'Vinamilk Supply Chain Operations Internship 2026 - Pham Minh Hoang';

  // Color constants
  const C_VM_BLUE = '0047BA';
  const C_VM_DARK = '002D72';
  const C_VM_LIGHT = 'EBF3FE';
  const C_VM_SOFT = 'D6E6FE';
  const C_ACCENT = '00A3FF';
  const C_GREEN = '10B981';
  const C_TEXT_DARK = '0F172A';
  const C_TEXT_MUTED = '475569';
  const C_WHITE = 'FFFFFF';
  const FONT_HEAD = 'Arial';
  const FONT_BODY = 'Arial';

  // Helper: Slide Header
  function addSlideHeader(slide, category, section) {
    slide.addText(
      [
        { text: 'VINAMILK SUPPLY CHAIN OPERATIONS 2026', options: { bold: true, color: C_VM_BLUE, fontSize: 10 } },
        { text: `   |   ${category} • ${section}`, options: { color: C_VM_DARK, fontSize: 9.5, bold: false } }
      ],
      { x: 0.8, y: 0.35, w: 11.73, h: 0.3, margin: 0 }
    );
    // Divider line
    slide.addShape(pres.ShapeType.line, {
      x: 0.8, y: 0.72, w: 11.73, h: 0,
      line: { color: C_VM_SOFT, width: 1.5 }
    });
  }

  // ==========================================
  // SLIDE 1: COVER
  // ==========================================
  const s1 = pres.addSlide();
  s1.background = { color: C_VM_BLUE };

  // Top sub-bar
  s1.addText('VINAMILK SUPPLY CHAIN OPERATIONS 2026   |   SELF-INTRODUCTION CANDIDATE DOSSIER', {
    x: 0.8, y: 0.4, w: 11.73, h: 0.3,
    color: 'BFDBFE', fontSize: 10, bold: true, margin: 0
  });

  // Left Content: Hero
  s1.addShape(pres.ShapeType.roundRect, {
    x: 0.8, y: 1.1, w: 4.5, h: 0.36,
    fill: { color: '003B99' },
    line: { color: '60A5FA', width: 1 },
    rectRadius: 0.18
  });
  s1.addText('SUPPLY CHAIN OPERATIONS INTERN CANDIDATE', {
    x: 0.8, y: 1.1, w: 4.5, h: 0.36,
    color: C_WHITE, fontSize: 10, bold: true, align: 'center', valign: 'middle', margin: 0
  });

  s1.addText('PRECISION &\nOPERATIONAL AGILITY', {
    x: 0.8, y: 1.6, w: 6.2, h: 1.6,
    color: C_WHITE, fontFace: FONT_HEAD, fontSize: 36, bold: true, lineSpacing: 40, margin: 0
  });

  s1.addText('Leveraging dual-degree academic rigor, real-world 3F agribusiness logistics experience, and AI-driven workflow optimization to empower Vinamilk\'s farm-to-table excellence.', {
    x: 0.8, y: 3.4, w: 6.0, h: 1.1,
    color: 'E0E7FF', fontSize: 12.5, lineSpacing: 18, margin: 0
  });

  // Candidate Badge Box
  s1.addShape(pres.ShapeType.roundRect, {
    x: 0.8, y: 4.85, w: 6.0, h: 1.5,
    fill: { color: C_WHITE },
    line: { color: C_WHITE },
    rectRadius: 0.15,
    shadow: { type: 'outer', color: '000000', blur: 6, offset: 3, opacity: 0.2 }
  });
  s1.addText([
    { text: 'Pham Minh Hoang\n', options: { fontSize: 20, bold: true, color: C_VM_DARK } },
    { text: 'Final-Year Senior • National Economics University (NEU)\n', options: { fontSize: 11, bold: true, color: C_VM_BLUE } },
    { text: 'Dual Degrees: Logistics & SCM  |  International Business Management', options: { fontSize: 10.5, color: C_TEXT_MUTED } }
  ], {
    x: 1.05, y: 4.95, w: 5.5, h: 1.3, valign: 'middle', margin: 0
  });

  // Right Side: Card with Metrics & Highlights
  s1.addShape(pres.ShapeType.roundRect, {
    x: 7.2, y: 1.1, w: 5.33, h: 5.4,
    fill: { color: C_WHITE },
    rectRadius: 0.2,
    shadow: { type: 'outer', color: '000000', blur: 10, offset: 4, opacity: 0.25 }
  });

  s1.addText('KEY PROFILE METRICS', {
    x: 7.4, y: 1.35, w: 4.93, h: 0.3,
    color: C_VM_BLUE, fontSize: 11, bold: true, align: 'center', margin: 0
  });

  // 3 Metric Pills
  const metrics = [
    { val: '3.52', lbl: 'NEU GPA / 4.0', x: 7.5 },
    { val: '6.5', lbl: 'IELTS Band', x: 9.15 },
    { val: '0', lbl: 'Demurrage Days', x: 10.8 }
  ];
  metrics.forEach(m => {
    s1.addShape(pres.ShapeType.roundRect, {
      x: m.x, y: 1.75, w: 1.45, h: 1.15,
      fill: { color: C_VM_LIGHT },
      line: { color: C_VM_SOFT, width: 1 },
      rectRadius: 0.1
    });
    s1.addText([
      { text: `${m.val}\n`, options: { fontSize: 22, bold: true, color: C_VM_BLUE } },
      { text: m.lbl, options: { fontSize: 8.5, bold: true, color: C_TEXT_MUTED } }
    ], {
      x: m.x, y: 1.85, w: 1.45, h: 0.95, align: 'center', valign: 'middle', margin: 0
    });
  });

  // Operational Grit Banner
  s1.addShape(pres.ShapeType.roundRect, {
    x: 7.5, y: 3.1, w: 4.75, h: 3.15,
    fill: { color: C_VM_LIGHT },
    line: { color: 'BFDBFE', width: 1 },
    rectRadius: 0.15
  });
  s1.addText([
    { text: '✓ 100% OPERATIONAL GRIT\n\n', options: { fontSize: 12, bold: true, color: C_VM_DARK } },
    { text: '• Practical Agribusiness Logistics: ', options: { fontSize: 10.5, bold: true, color: C_VM_BLUE } },
    { text: 'Hands-on operations at C.P. Vietnam Corporation (3F model: Feed-Farm-Food).\n\n', options: { fontSize: 10, color: C_TEXT_DARK } },
    { text: '• Zero Cost Penalties: ', options: { fontSize: 10.5, bold: true, color: C_VM_BLUE } },
    { text: 'Successfully cleared 10 raw material import shipments with 0 demurrage or detention.\n\n', options: { fontSize: 10, color: C_TEXT_DARK } },
    { text: '• AI Operational Automation: ', options: { fontSize: 10.5, bold: true, color: C_VM_BLUE } },
    { text: 'Pioneered custom AI agents to streamline tracking & reporting workflows.', options: { fontSize: 10, color: C_TEXT_DARK } }
  ], {
    x: 7.7, y: 3.25, w: 4.35, h: 2.85, valign: 'top', margin: 0
  });

  // ==========================================
  // SLIDE 2: ABOUT ME & ACADEMIC RIGOR
  // ==========================================
  const s2 = pres.addSlide();
  s2.background = { color: C_WHITE };
  addSlideHeader(s2, '01', 'ABOUT ME & ACADEMIC RIGOR');

  // Left Column: Candidate Essence
  s2.addShape(pres.ShapeType.roundRect, {
    x: 0.8, y: 0.95, w: 4.8, h: 6.0,
    fill: { color: C_VM_BLUE },
    rectRadius: 0.18,
    shadow: { type: 'outer', color: '000000', blur: 8, offset: 3, opacity: 0.15 }
  });

  s2.addText('CANDIDATE PROFILE', {
    x: 1.15, y: 1.25, w: 4.1, h: 0.3,
    color: 'BFDBFE', fontSize: 10, bold: true, margin: 0
  });

  s2.addText('Analytical Mind,\nHands-On Instinct', {
    x: 1.15, y: 1.6, w: 4.1, h: 0.9,
    color: C_WHITE, fontFace: FONT_HEAD, fontSize: 24, bold: true, margin: 0
  });

  s2.addText('Final-year student at National Economics University (NEU) simultaneously completing two competitive bachelor degrees in Logistics & Supply Chain Management and International Business Management.', {
    x: 1.15, y: 2.65, w: 4.1, h: 1.1,
    color: 'E0E7FF', fontSize: 11.5, lineSpacing: 16, margin: 0
  });

  // Quote Box
  s2.addShape(pres.ShapeType.roundRect, {
    x: 1.15, y: 3.9, w: 4.1, h: 1.45,
    fill: { color: '003B99' },
    line: { color: '60A5FA', width: 1 },
    rectRadius: 0.1
  });
  s2.addText('"Supply chain operations is the art of synchronizing physical velocity, data integrity, and strict quality compliance. I don\'t just observe—I execute."', {
    x: 1.35, y: 4.0, w: 3.7, h: 1.25,
    color: C_WHITE, fontSize: 11, italic: true, lineSpacing: 15, valign: 'middle', margin: 0
  });

  // Tag badges
  s2.addText('TAGS: Dual-Degree NEU  •  IELTS 6.5  •  ICDL Certified  •  AI Agent Developer', {
    x: 1.15, y: 5.6, w: 4.1, h: 0.8,
    color: 'BFDBFE', fontSize: 10, bold: true, margin: 0
  });

  // Right Column 1: Academic Grounding
  s2.addShape(pres.ShapeType.roundRect, {
    x: 5.85, y: 0.95, w: 6.68, h: 2.85,
    fill: { color: C_VM_LIGHT },
    line: { color: C_VM_SOFT, width: 1 },
    rectRadius: 0.15
  });
  s2.addText([
    { text: 'THEORETICAL GROUNDING • NATIONAL ECONOMICS UNIVERSITY\n', options: { fontSize: 9.5, bold: true, color: C_VM_BLUE } },
    { text: 'Rigorous Supply Chain & Operations Foundation\n\n', options: { fontSize: 16, bold: true, color: C_VM_DARK } },
    { text: '• Deep understanding of queueing theory, capacity bottleneck identification, aggregate planning, and Lean waste reduction to compress order-to-delivery lead times.\n', options: { fontSize: 11, color: C_TEXT_DARK } },
    { text: '• Mastery of international commercial terms (Incoterms 2020), import-export documentation, and payment verification methods (L/C, T/T).\n\n', options: { fontSize: 11, color: C_TEXT_DARK } },
    { text: 'Key Coursework: Global Logistics (8.9/10) | Logistics Ops Management (8.8/10) | Foreign Trade (8.4/10)', options: { fontSize: 10, bold: true, color: C_VM_BLUE } }
  ], {
    x: 6.1, y: 1.1, w: 6.2, h: 2.55, valign: 'top', margin: 0
  });

  // Right Column 2: C.P. Vietnam Experience
  s2.addShape(pres.ShapeType.roundRect, {
    x: 5.85, y: 4.05, w: 6.68, h: 2.9,
    fill: { color: C_VM_LIGHT },
    line: { color: C_VM_SOFT, width: 1 },
    rectRadius: 0.15
  });
  s2.addText([
    { text: 'OPERATIONAL EXPOSURE • C.P. VIETNAM CORPORATION\n', options: { fontSize: 9.5, bold: true, color: C_VM_BLUE } },
    { text: '3F Model (Feed-Farm-Food) Logistics Immersion\n\n', options: { fontSize: 16, bold: true, color: C_VM_DARK } },
    { text: '• Customs Declarations: ', options: { fontSize: 11, bold: true, color: C_VM_BLUE } },
    { text: 'Successfully cleared 10 import shipments of core agricultural feed ingredients via ECUS5-VNACCS with 100% compliance.\n', options: { fontSize: 11, color: C_TEXT_DARK } },
    { text: '• Specialized Regulatory Compliance: ', options: { fontSize: 11, bold: true, color: C_VM_BLUE } },
    { text: 'Researched HS codes and coordinated with veterinary quarantine authorities to satisfy food safety & phytosanitary standards.\n', options: { fontSize: 11, color: C_TEXT_DARK } },
    { text: '• Airport Ground Handling: ', options: { fontSize: 11, bold: true, color: C_VM_BLUE } },
    { text: 'Directly executed live chicks air cargo clearance at Noi Bai Airport, minimizing transit stress.', options: { fontSize: 11, color: C_TEXT_DARK } }
  ], {
    x: 6.1, y: 4.2, w: 6.2, h: 2.6, valign: 'top', margin: 0
  });

  // ==========================================
  // SLIDE 3: 3 PILLARS OF OPERATIONAL EXCELLENCE
  // (PERFECTLY SCALED TO FIT 13.333 x 7.5 WITH 0 OVERFLOW)
  // ==========================================
  const s3 = pres.addSlide();
  s3.background = { color: C_WHITE };
  addSlideHeader(s3, '02', 'KEY STRENGTHS & DIFFERENTIATORS');

  s3.addText('3 Pillars of Operational Excellence', {
    x: 0.8, y: 0.88, w: 11.73, h: 0.42,
    fontFace: FONT_HEAD, fontSize: 23, bold: true, color: C_VM_BLUE, margin: 0
  });
  s3.addText('Combining field-tested execution, rigorous financial auditing, and modern AI automation', {
    x: 0.8, y: 1.3, w: 11.73, h: 0.25,
    fontSize: 11.5, color: C_TEXT_MUTED, margin: 0
  });

  const cardW = 3.67;
  const cardGap = 0.36;
  const pillars = [
    {
      num: '01', tag: 'EXECUTION',
      x: 0.8,
      title: 'End-to-End Operational Execution & Compliance',
      b1: 'Reconciled commercial docs (B/L, Inv, PL, C/O) with 100% data integrity before declarations.',
      b2: 'Successfully declared & cleared 10 raw material feed shipments via ECUS5-VNACCS.',
      b3: 'Directly executed ground ops and air cargo clearance for live chicks at Noi Bai Airport.',
      highlight: '🎯 0 demurrage or detention incurred'
    },
    {
      num: '02', tag: 'ANALYTICS',
      x: 0.8 + cardW + cardGap,
      title: 'Cost Auditing & Analytical Problem Solving',
      b1: 'Formulated and maintained detailed Shipment Cost Sheets for trucking, ocean freight & port fees.',
      b2: 'Rigorously audited carrier invoices to eliminate billing discrepancies and maintain cost accuracy.',
      b3: 'Applied queueing models & safety stock calculations to resolve flow bottlenecks.',
      highlight: '📊 100% cost auditing accuracy on billing'
    },
    {
      num: '03', tag: 'INNOVATION',
      x: 0.8 + (cardW + cardGap) * 2,
      title: 'AI Automation & Digital Agility',
      b1: 'Pioneered building custom AI agents on Google Antigravity to automate logistics tracking & synthesis.',
      b2: 'Replaced manual Excel reconciliation with automated scripts, boosting daily reporting speed.',
      b3: 'ICDL International Computer Certificate; advanced Excel modeling (VLOOKUP, Pivot, Models).',
      highlight: '🚀 Ready for smart digital supply chain'
    }
  ];

  pillars.forEach(p => {
    // Card border
    s3.addShape(pres.ShapeType.roundRect, {
      x: p.x, y: 1.7, w: cardW, h: 5.25,
      fill: { color: C_WHITE },
      line: { color: C_VM_SOFT, width: 1.5 },
      rectRadius: 0.15,
      shadow: { type: 'outer', color: '000000', blur: 6, offset: 2, opacity: 0.08 }
    });

    // Num box
    s3.addShape(pres.ShapeType.roundRect, {
      x: p.x + 0.25, y: 1.95, w: 0.75, h: 0.55,
      fill: { color: C_VM_BLUE },
      rectRadius: 0.1
    });
    s3.addText(p.num, {
      x: p.x + 0.25, y: 1.95, w: 0.75, h: 0.55,
      color: C_WHITE, fontSize: 15, bold: true, align: 'center', valign: 'middle', margin: 0
    });

    // Tag Pill
    s3.addShape(pres.ShapeType.roundRect, {
      x: p.x + 2.3, y: 2.05, w: 1.12, h: 0.35,
      fill: { color: C_VM_LIGHT },
      rectRadius: 0.17
    });
    s3.addText(p.tag, {
      x: p.x + 2.3, y: 2.05, w: 1.12, h: 0.35,
      color: C_VM_BLUE, fontSize: 9.5, bold: true, align: 'center', valign: 'middle', margin: 0
    });

    // Title
    s3.addText(p.title, {
      x: p.x + 0.25, y: 2.65, w: 3.17, h: 0.7,
      fontFace: FONT_HEAD, fontSize: 13, bold: true, color: C_VM_DARK, lineSpacing: 16, margin: 0
    });

    // Bullets
    s3.addText([
      { text: `• ${p.b1}\n\n`, options: { fontSize: 10, color: C_TEXT_DARK } },
      { text: `• ${p.b2}\n\n`, options: { fontSize: 10, color: C_TEXT_DARK } },
      { text: `• ${p.b3}`, options: { fontSize: 10, color: C_TEXT_DARK } }
    ], {
      x: p.x + 0.25, y: 3.45, w: 3.17, h: 2.6, valign: 'top', margin: 0
    });

    // Highlight bottom pill
    s3.addShape(pres.ShapeType.roundRect, {
      x: p.x + 0.2, y: 6.25, w: 3.27, h: 0.55,
      fill: { color: C_VM_LIGHT },
      line: { color: 'BFDBFE', width: 0.8 },
      rectRadius: 0.1
    });
    s3.addText(p.highlight, {
      x: p.x + 0.2, y: 6.25, w: 3.27, h: 0.55,
      fontSize: 9.5, bold: true, color: C_VM_DARK, align: 'center', valign: 'middle', margin: 0
    });
  });

  // ==========================================
  // SLIDE 4: WHY SUPPLY CHAIN & WHY VINAMILK
  // ==========================================
  const s4 = pres.addSlide();
  s4.background = { color: C_WHITE };
  addSlideHeader(s4, '03', 'MOTIVATION & TARGET DESTINATION');

  s4.addText('Passion Meets Benchmark Scale', {
    x: 0.8, y: 0.88, w: 11.73, h: 0.42,
    fontFace: FONT_HEAD, fontSize: 23, bold: true, color: C_VM_BLUE, margin: 0
  });
  s4.addText('Connecting personal operational drive with Vinamilk\'s world-class dairy ecosystem', {
    x: 0.8, y: 1.3, w: 11.73, h: 0.25,
    fontSize: 11.5, color: C_TEXT_MUTED, margin: 0
  });

  const colW = 5.64;
  const colGap = 0.45;

  // Left Box: Why Supply Chain
  s4.addShape(pres.ShapeType.roundRect, {
    x: 0.8, y: 1.75, w: colW, h: 5.2,
    fill: { color: C_VM_LIGHT },
    line: { color: 'BFDBFE', width: 1.5 },
    rectRadius: 0.18
  });
  s4.addText('FIELD PASSION', {
    x: 1.1, y: 2.0, w: 5.0, h: 0.28,
    color: C_VM_BLUE, fontSize: 10, bold: true, margin: 0
  });
  s4.addText('Why Supply Chain Operations?', {
    x: 1.1, y: 2.3, w: 5.0, h: 0.4,
    fontFace: FONT_HEAD, fontSize: 19, bold: true, color: C_VM_DARK, margin: 0
  });

  s4.addText([
    { text: '• The Backbone of Daily Nutrition:\n', options: { fontSize: 11.5, bold: true, color: C_VM_BLUE } },
    { text: 'Captivated by the synchronized orchestration of raw materials, cold storage, and express distribution where every hour saved directly protects nutritional freshness.\n\n', options: { fontSize: 10, color: C_TEXT_DARK } },
    { text: '• Where Analysis Meets Floor Reality:\n', options: { fontSize: 11.5, bold: true, color: C_VM_BLUE } },
    { text: 'Supply chain operations is the ultimate arena where analytical models are tested against dynamic lead times, sudden volume surges, and tight transport schedules.\n\n', options: { fontSize: 10, color: C_TEXT_DARK } },
    { text: '• Scalable Societal Impact:\n', options: { fontSize: 11.5, bold: true, color: C_VM_BLUE } },
    { text: 'Optimizing distribution networks directly ensures essential dairy products reach millions of Vietnamese children and families reliably every morning.', options: { fontSize: 10, color: C_TEXT_DARK } }
  ], {
    x: 1.1, y: 2.85, w: 5.04, h: 3.8, valign: 'top', margin: 0
  });

  // Right Box: Why Vinamilk
  s4.addShape(pres.ShapeType.roundRect, {
    x: 0.8 + colW + colGap, y: 1.75, w: colW, h: 5.2,
    fill: { color: C_VM_BLUE },
    rectRadius: 0.18,
    shadow: { type: 'outer', color: '000000', blur: 8, offset: 3, opacity: 0.18 }
  });
  s4.addText('TARGET DESTINATION', {
    x: 0.8 + colW + colGap + 0.3, y: 2.0, w: 5.0, h: 0.28,
    color: 'BFDBFE', fontSize: 10, bold: true, margin: 0
  });
  s4.addText('Why Vinamilk 2026?', {
    x: 0.8 + colW + colGap + 0.3, y: 2.3, w: 5.0, h: 0.4,
    fontFace: FONT_HEAD, fontSize: 19, bold: true, color: C_WHITE, margin: 0
  });

  s4.addText([
    { text: '• Vietnam’s Apex FMCG Supply Chain:\n', options: { fontSize: 11.5, bold: true, color: '93C5FD' } },
    { text: 'Vinamilk sets the gold standard with automated Mega Factories, high-bay AS/RS smart warehousing, and high-standard dairy farms nationwide.\n\n', options: { fontSize: 10, color: 'F1F5F9' } },
    { text: '• Bridge from 3F Agri to FMCG Dairy:\n', options: { fontSize: 11.5, bold: true, color: '93C5FD' } },
    { text: 'Having managed feed import operations at C.P. Vietnam, I am hungry to elevate my expertise into Vinamilk’s integrated "Farm-to-Table" cold chain.\n\n', options: { fontSize: 10, color: 'F1F5F9' } },
    { text: '• An Action-Oriented Culture:\n', options: { fontSize: 11.5, bold: true, color: '93C5FD' } },
    { text: 'Vinamilk’s promise—"direct participation in operational activities rather than observing from the sidelines"—matches my proactive, high-ownership mindset.', options: { fontSize: 10, color: 'F1F5F9' } }
  ], {
    x: 0.8 + colW + colGap + 0.3, y: 2.85, w: 5.04, h: 3.8, valign: 'top', margin: 0
  });

  // ==========================================
  // SLIDE 5: LEARNING OBJECTIVES & VALUE DELIVERY
  // ==========================================
  const s5 = pres.addSlide();
  s5.background = { color: C_WHITE };
  addSlideHeader(s5, '04', 'GOALS & VALUE CONTRIBUTION');

  s5.addText('Learning Objectives & Value Delivery', {
    x: 0.8, y: 0.88, w: 11.73, h: 0.42,
    fontFace: FONT_HEAD, fontSize: 23, bold: true, color: C_VM_BLUE, margin: 0
  });
  s5.addText('A dual commitment: rapid personal mastery and measurable operational contribution', {
    x: 0.8, y: 1.3, w: 11.73, h: 0.25,
    fontSize: 11.5, color: C_TEXT_MUTED, margin: 0
  });

  // Left Column: Learning Objectives
  s5.addShape(pres.ShapeType.roundRect, {
    x: 0.8, y: 1.7, w: colW, h: 4.45,
    fill: { color: C_VM_LIGHT },
    line: { color: C_VM_SOFT, width: 1 },
    rectRadius: 0.15
  });
  s5.addText('🎯 LEARNING OBJECTIVES (GROWTH ROADMAP)', {
    x: 1.05, y: 1.9, w: 5.1, h: 0.3,
    color: C_VM_DARK, fontSize: 11, bold: true, margin: 0
  });

  const learnItems = [
    {
      title: 'Smart Warehousing & DC Operations',
      desc: 'Gain hands-on exposure to automated AS/RS storage, inventory turnover control, and cold-chain distribution center flows.'
    },
    {
      title: 'End-to-End Systemic Thinking',
      desc: 'Observe how dairy farming, mega-factory processing, and nationwide primary/secondary transport synchronize under peak loads.'
    },
    {
      title: 'Continuous Improvement (Kaizen/PDCA)',
      desc: 'Learn structured root-cause problem solving to pinpoint bottleneck delays and compress order-to-delivery lead times.'
    }
  ];
  learnItems.forEach((it, idx) => {
    const yPos = 2.3 + idx * 1.15;
    s5.addShape(pres.ShapeType.roundRect, {
      x: 1.05, y: yPos, w: 5.14, h: 1.0,
      fill: { color: C_WHITE },
      line: { color: 'E2E8F0', width: 0.8 },
      rectRadius: 0.1
    });
    s5.addText([
      { text: `${it.title}\n`, options: { fontSize: 10.5, bold: true, color: C_VM_BLUE } },
      { text: it.desc, options: { fontSize: 9.5, color: C_TEXT_DARK } }
    ], {
      x: 1.2, y: yPos + 0.1, w: 4.84, h: 0.8, valign: 'middle', margin: 0
    });
  });

  // Right Column: Value Delivery
  s5.addShape(pres.ShapeType.roundRect, {
    x: 0.8 + colW + colGap, y: 1.7, w: colW, h: 4.45,
    fill: { color: 'D1FAE5' },
    line: { color: 'A7F3D0', width: 1 },
    rectRadius: 0.15
  });
  s5.addText('⚡ VALUE DELIVERY (DAY 1 IMPACT)', {
    x: 0.8 + colW + colGap + 0.25, y: 1.9, w: 5.1, h: 0.3,
    color: '065F46', fontSize: 11, bold: true, margin: 0
  });

  const valItems = [
    {
      title: 'Day-One Document & Cost Precision',
      desc: 'Bring proven customs clearance and cost-auditing vigilance from C.P. Vietnam to maintain 100% compliance in operational paperwork.'
    },
    {
      title: 'Workflow Automation & Productivity',
      desc: 'Leverage AI agent scripting and advanced Excel data modeling to eliminate repetitive tracking tasks and build daily operational summaries.'
    },
    {
      title: 'High Grit & Long-Term Commitment',
      desc: 'Eager to tackle challenging floor assignments, with the explicit goal of advancing into a full-time Supply Chain Specialist role at Vinamilk.'
    }
  ];
  valItems.forEach((it, idx) => {
    const yPos = 2.3 + idx * 1.15;
    s5.addShape(pres.ShapeType.roundRect, {
      x: 0.8 + colW + colGap + 0.25, y: yPos, w: 5.14, h: 1.0,
      fill: { color: C_WHITE },
      line: { color: 'E2E8F0', width: 0.8 },
      rectRadius: 0.1
    });
    s5.addText([
      { text: `${it.title}\n`, options: { fontSize: 10.5, bold: true, color: '047857' } },
      { text: it.desc, options: { fontSize: 9.5, color: C_TEXT_DARK } }
    ], {
      x: 0.8 + colW + colGap + 0.4, y: yPos + 0.1, w: 4.84, h: 0.8, valign: 'middle', margin: 0
    });
  });

  // Bottom Contact Strip
  s5.addShape(pres.ShapeType.roundRect, {
    x: 0.8, y: 6.35, w: 11.73, h: 0.75,
    fill: { color: C_VM_DARK },
    rectRadius: 0.12
  });
  s5.addText([
    { text: 'Pham Minh Hoang   ', options: { fontSize: 12, bold: true, color: C_WHITE } },
    { text: '•  Ready for Day 1 Impact   |   ', options: { fontSize: 11, bold: true, color: '93C5FD' } },
    { text: '📞 0349451048   •   ✉️ hoang050205@gmail.com   •   🔗 linkedin.com/in/phạm-minh-hoàng-517b66342   •   📍 Hanoi, Vietnam', options: { fontSize: 10, color: 'E2E8F0' } }
  ], {
    x: 1.1, y: 6.42, w: 11.13, h: 0.6, valign: 'middle', align: 'center', margin: 0
  });

  const outDir = path.join(__dirname, 'outputs', 'reports');
  fs.mkdirSync(outDir, { recursive: true });

  const pptxPath = path.join(outDir, 'Vinamilk_Supply_Chain_Operations_PhamMinhHoang.pptx');
  await pres.writeFile({ fileName: pptxPath });
  console.log('SUCCESS: PowerPoint created at ' + pptxPath);
}

createVinamilkDeck().catch(err => {
  console.error('ERROR creating deck:', err);
  process.exit(1);
});
