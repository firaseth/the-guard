#!/usr/bin/env python3
"""
The Guard - Personal Safety AI: Technical Development Roadmap
Body PDF generation script (ReportLab)
"""

import os, sys, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, CondPageBreak, HRFlowable, ListFlowable, ListItem
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import SimpleDocTemplate

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FONT REGISTRATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
pdfmetrics.registerFont(TTFont('TimesNewRoman', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('TinosBold', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Calibri', '/usr/share/fonts/truetype/english/Carlito-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
registerFontFamily('TimesNewRoman', normal='TimesNewRoman', bold='TinosBold')
registerFontFamily('Calibri', normal='Calibri', bold='Calibri')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COLOR PALETTE (auto-generated)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACCENT       = colors.HexColor('#c72842')
TEXT_PRIMARY  = colors.HexColor('#191a1b')
TEXT_MUTED    = colors.HexColor('#848b90')
BG_SURFACE   = colors.HexColor('#d8dde0')
BG_PAGE      = colors.HexColor('#eff0f1')

TABLE_HEADER_COLOR = ACCENT
TABLE_HEADER_TEXT  = colors.white
TABLE_ROW_EVEN     = colors.white
TABLE_ROW_ODD      = BG_SURFACE

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STYLES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
styles = getSampleStyleSheet()

h1_style = ParagraphStyle(
    name='H1', fontName='TimesNewRoman', fontSize=22, leading=28,
    textColor=TEXT_PRIMARY, spaceBefore=18, spaceAfter=12, alignment=TA_LEFT
)
h2_style = ParagraphStyle(
    name='H2', fontName='TimesNewRoman', fontSize=16, leading=22,
    textColor=ACCENT, spaceBefore=14, spaceAfter=8, alignment=TA_LEFT
)
h3_style = ParagraphStyle(
    name='H3', fontName='TimesNewRoman', fontSize=13, leading=18,
    textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=6, alignment=TA_LEFT
)
body_style = ParagraphStyle(
    name='Body', fontName='TimesNewRoman', fontSize=11, leading=18,
    textColor=TEXT_PRIMARY, spaceBefore=0, spaceAfter=6, alignment=TA_JUSTIFY
)
bullet_style = ParagraphStyle(
    name='Bullet', fontName='TimesNewRoman', fontSize=11, leading=17,
    textColor=TEXT_PRIMARY, leftIndent=24, spaceBefore=2, spaceAfter=2,
    alignment=TA_LEFT, bulletIndent=12
)
code_style = ParagraphStyle(
    name='Code', fontName='DejaVuSans', fontSize=9, leading=14,
    textColor=TEXT_PRIMARY, leftIndent=18, rightIndent=18,
    spaceBefore=6, spaceAfter=6, alignment=TA_LEFT,
    backColor=colors.HexColor('#f5f5f5'), borderPadding=6
)
caption_style = ParagraphStyle(
    name='Caption', fontName='TimesNewRoman', fontSize=10, leading=14,
    textColor=TEXT_MUTED, spaceBefore=3, spaceAfter=6, alignment=TA_CENTER
)
callout_style = ParagraphStyle(
    name='Callout', fontName='TimesNewRoman', fontSize=11, leading=18,
    textColor=TEXT_PRIMARY, leftIndent=18, rightIndent=18,
    spaceBefore=8, spaceAfter=8, alignment=TA_LEFT,
    backColor=colors.HexColor('#fdf2f4'), borderPadding=10,
    borderColor=ACCENT, borderWidth=1, borderRadius=2
)

# TOC styles
toc_h1_style = ParagraphStyle(
    name='TOCHeading1', fontName='TimesNewRoman', fontSize=13,
    leftIndent=20, leading=20, spaceBefore=4, spaceAfter=4
)
toc_h2_style = ParagraphStyle(
    name='TOCHeading2', fontName='TimesNewRoman', fontSize=11,
    leftIndent=40, leading=16, spaceBefore=2, spaceAfter=2
)

# Table styles
header_cell_style = ParagraphStyle(
    name='HeaderCell', fontName='TimesNewRoman', fontSize=10.5,
    textColor=TABLE_HEADER_TEXT, alignment=TA_CENTER, leading=14
)
cell_style = ParagraphStyle(
    name='Cell', fontName='TimesNewRoman', fontSize=10,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=14
)
cell_center_style = ParagraphStyle(
    name='CellCenter', fontName='TimesNewRoman', fontSize=10,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER, leading=14
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DOCUMENT TEMPLATE WITH TOC SUPPORT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))


def add_heading(text, style, level=0):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), style)
    p.bookmark_name = text
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p


def safe_keep_together(elements):
    """Wrap elements in KeepTogether if total height is reasonable."""
    total_h = 0
    for el in elements:
        w, h = el.wrap(A4[0] - 2 * inch, A4[1])
        total_h += h
    if total_h <= A4[1] * 0.4:
        return [KeepTogether(elements)]
    elif len(elements) >= 2:
        return [KeepTogether(elements[:2])] + list(elements[2:])
    return list(elements)


def make_table(data, col_ratios, available_width):
    """Create a styled table with proportional column widths."""
    col_widths = [r * available_width for r in col_ratios]
    table = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), TABLE_HEADER_TEXT),
        ('GRID', (0, 0), (-1, -1), 0.5, TEXT_MUTED),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        bg = TABLE_ROW_EVEN if i % 2 == 1 else TABLE_ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    table.setStyle(TableStyle(style_cmds))
    return table


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BUILD DOCUMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'the_guard_body.pdf')
doc = TocDocTemplate(
    output_path,
    pagesize=A4,
    topMargin=1.0 * inch,
    bottomMargin=0.8 * inch,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
)

available_width = A4[0] - 2 * inch  # ~451pt

story = []

# ── TABLE OF CONTENTS ──
toc_title_style = ParagraphStyle(
    name='TOCTitle', fontName='TimesNewRoman', fontSize=22, leading=28,
    textColor=TEXT_PRIMARY, spaceBefore=12, spaceAfter=18, alignment=TA_LEFT
)
story.append(Paragraph('<b>Table of Contents</b>', toc_title_style))
toc = TableOfContents()
toc.levelStyles = [toc_h1_style, toc_h2_style]
story.append(toc)
story.append(PageBreak())

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1: INTRODUCTION & VISION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('1. Introduction and Vision', h1_style, 0),
    Paragraph(
        'The Guard is a personal safety AI application designed to serve as a constant, intelligent '
        'watchdog over the user or their loved ones. By combining cutting-edge computer vision, '
        'on-device language model reasoning, and seamless emergency connectivity, The Guard represents '
        'the frontier of AI engineering applied to personal security. The application runs entirely on '
        'the user\'s device or a local edge server, ensuring that no sensitive video or audio data '
        'is ever transmitted to the cloud. This privacy-first architecture is central to the design '
        'philosophy, making The Guard one of the most trustworthy safety companions available.',
        body_style
    ),
    Paragraph(
        'The name "The Guard" was chosen because it evokes a sense of strength, protection, and '
        'reliability. Much like a dedicated security professional, the application watches over the user '
        'in real time, analyzing visual and auditory inputs to detect potentially dangerous situations. '
        'Whether it is an elderly family member who may have suffered a fall, a solo traveler walking '
        'home at night, or anyone who wants an extra layer of personal safety, The Guard is designed '
        'to be their intelligent, ever-vigilant companion. The application does not merely react to '
        'predefined triggers; it uses a local large language model (LLM) to reason about situations '
        'contextually, distinguishing between genuine emergencies and benign events with nuance and accuracy.',
        body_style
    ),
    Paragraph(
        'Building an application that combines real-time computer vision with on-device LLM reasoning '
        'is a challenging but immensely rewarding engineering endeavor. This roadmap outlines the complete '
        'technical development journey, from initial setup through production deployment, covering every '
        'major system component, architectural decision, and implementation phase. The document is organized '
        'into five development phases, each building upon the previous one, along with dedicated sections '
        'on privacy, resource management, and the key open-source repositories that power the system.',
        body_style
    ),
    Spacer(1, 18),
])

# Callout: Vision Statement
story.append(Paragraph(
    '<b>Vision Statement:</b> Build an AI-powered personal safety application that runs entirely on-device, '
    'combining real-time object detection with intelligent reasoning to protect users and their loved ones '
    'in any situation, without ever compromising their privacy.',
    callout_style
))
story.append(Spacer(1, 18))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2: SYSTEM ARCHITECTURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('2. System Architecture', h1_style, 0),
    Paragraph(
        'The Guard employs a Hybrid Mobile Architecture that optimizes the balance between processing '
        'speed, battery efficiency, and user experience. The architecture is designed around three core '
        'principles: locality (all sensitive processing happens on-device or on a local edge server), '
        'modularity (each major subsystem operates independently and can be upgraded or replaced without '
        'affecting others), and responsiveness (the user interface remains smooth and responsive even '
        'during intensive AI processing). This hybrid approach ensures that the application performs '
        'reliably on a wide range of devices, from flagship smartphones to modest home servers.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('2.1 Architecture Overview', h2_style, 1),
    Paragraph(
        'The system is composed of four distinct layers, each responsible for a critical aspect of the '
        'application\'s functionality. These layers communicate through well-defined interfaces, ensuring '
        'that changes to one layer do not cascade into others. The following table summarizes each layer, '
        'its technology stack, and its role within the overall system.',
        body_style
    ),
    Spacer(1, 12),
])

# Architecture table
arch_data = [
    [
        Paragraph('<b>Layer</b>', header_cell_style),
        Paragraph('<b>Technology</b>', header_cell_style),
        Paragraph('<b>Role</b>', header_cell_style),
    ],
    [
        Paragraph('Frontend (Interface)', cell_style),
        Paragraph('Flutter (Dart)', cell_style),
        Paragraph('Cross-platform UI for iOS and Android with high-performance rendering and native-feel interactions', cell_style),
    ],
    [
        Paragraph('Computer Vision (Eyes)', cell_style),
        Paragraph('YOLOv8 (TFLite/ONNX)', cell_style),
        Paragraph('Real-time object detection running directly on the device for low-latency visual analysis', cell_style),
    ],
    [
        Paragraph('AI Brain (Agent)', cell_style),
        Paragraph('Llama.cpp (Phi-3 Mini)', cell_style),
        Paragraph('Local LLM reasoning engine for contextual decision-making and intelligent response generation', cell_style),
    ],
    [
        Paragraph('Backend (Orchestration)', cell_style),
        Paragraph('Python + LangChain', cell_style),
        Paragraph('Connects vision and language subsystems, manages data flow, and coordinates actions', cell_style),
    ],
]
story.append(make_table(arch_data, [0.20, 0.25, 0.55], available_width))
story.append(Spacer(1, 6))
story.append(Paragraph('<b>Table 1:</b> System Architecture Layers', caption_style))
story.append(Spacer(1, 18))

story.extend([
    Paragraph(
        'The frontend layer, built with Flutter, provides a unified codebase that compiles to native '
        'iOS and Android applications. Flutter was selected for its excellent cross-platform performance, '
        'rich widget library, and strong community support. The computer vision layer uses YOLOv8, '
        'specifically the Nano variant, converted to TensorFlow Lite or ONNX format for efficient '
        'on-device inference. The AI reasoning layer leverages llama.cpp to run quantized large language '
        'models such as Microsoft\'s Phi-3 Mini or Meta\'s Llama-3-8B, enabling sophisticated contextual '
        'reasoning without any cloud dependency. Finally, the orchestration layer, written in Python using '
        'LangChain-inspired logic, coordinates the flow of data between vision and language, triggering '
        'appropriate actions based on the AI agent\'s decisions.',
        body_style
    ),
    Spacer(1, 18),
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3: PHASE 1 - THE SETUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('3. Phase 1: The Setup (Foundations)', h1_style, 0),
    Paragraph(
        'Before any AI logic can be implemented, the development environment must be properly configured '
        'to handle real-time video processing and on-device inference. This foundational phase establishes '
        'the project structure, configures platform-specific permissions, and sets up the AI compute '
        'infrastructure. Getting this phase right is critical, as it determines the performance ceiling '
        'for every subsequent development stage. A poorly configured environment can introduce latency, '
        'memory leaks, and platform incompatibilities that become increasingly difficult to resolve as '
        'the application grows in complexity.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('3.1 Flutter Project Initialization', h2_style, 1),
    Paragraph(
        'The first step is to create a new Flutter project using the standard Flutter CLI tool. The '
        'project should be initialized with the latest stable version of Flutter to ensure compatibility '
        'with the most recent packages and APIs. After creating the project skeleton, the developer must '
        'configure platform-specific camera access permissions. On Android, this involves adding the '
        'appropriate uses-permission declarations to the AndroidManifest.xml file, including permissions '
        'for the camera, microphone, and foreground services (for background monitoring). On iOS, the '
        'Info.plist must include the NSCameraUsageDescription and NSMicrophoneUsageDescription keys with '
        'clear, user-facing descriptions of why the app needs these permissions.',
        body_style
    ),
    Paragraph(
        'The Flutter project structure should be organized with clear separation of concerns from the '
        'outset. Recommended directory structure includes separate folders for the vision module, the '
        'AI agent module, the communication module (voice and SMS), and shared utilities. This modular '
        'approach makes the codebase more maintainable and allows different team members to work on '
        'different subsystems simultaneously without creating merge conflicts.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('3.2 Choosing the AI Brain Host', h2_style, 1),
    Paragraph(
        'One of the most important architectural decisions is where the LLM runs. There are two viable '
        'options, each with distinct trade-offs that must be carefully evaluated based on the target '
        'hardware, battery constraints, and performance requirements.',
        body_style
    ),
    Spacer(1, 8),
    add_heading('Option A: On-Device LLM (High End)', h3_style),
    Paragraph(
        'For flagship smartphones equipped with a neural processing unit (NPU), the LLM can run directly '
        'on the phone using llama.dart, which is a Dart-native port of the popular llama.cpp C++ library. '
        'This approach eliminates all network latency and ensures the AI functions even without internet '
        'connectivity. However, it demands significant RAM (typically 4-8 GB for a quantized model) and '
        'can rapidly drain the device battery during sustained inference. Modern devices with Snapdragon 8 '
        'Gen 3 or Apple A17 Pro chips are well-suited for this configuration, as their NPUs can handle '
        'the matrix operations required by transformer models with remarkable efficiency.',
        body_style
    ),
    Spacer(1, 8),
    add_heading('Option B: Local Server (Stable)', h3_style),
    Paragraph(
        'For broader device compatibility and better battery life, the LLM can run on a small home server '
        'such as a Raspberry Pi 5, an Intel NUC, or even a laptop that remains on the same Wi-Fi network '
        'as the phone. The phone connects to this server via a local HTTP API, sending context data and '
        'receiving AI-generated decisions. This approach, powered by LocalAI (an open-source drop-in '
        'replacement for OpenAI\'s API that runs entirely locally), provides a stable and power-efficient '
        'alternative. The main trade-off is the introduction of network latency (typically 50-200ms on a '
        'local network), which is generally acceptable for safety-critical reasoning but must be accounted '
        'for in the system\'s timeout and failover logic.',
        body_style
    ),
    Spacer(1, 12),
])

# Options comparison table
opts_data = [
    [
        Paragraph('<b>Criteria</b>', header_cell_style),
        Paragraph('<b>Option A: On-Device</b>', header_cell_style),
        Paragraph('<b>Option B: Local Server</b>', header_cell_style),
    ],
    [
        Paragraph('Latency', cell_center_style),
        Paragraph('Minimal (0-10ms)', cell_center_style),
        Paragraph('Low (50-200ms)', cell_center_style),
    ],
    [
        Paragraph('Battery Impact', cell_center_style),
        Paragraph('High drain', cell_center_style),
        Paragraph('Minimal', cell_center_style),
    ],
    [
        Paragraph('Hardware Required', cell_center_style),
        Paragraph('Flagship phone with NPU', cell_center_style),
        Paragraph('Raspberry Pi / NUC / Laptop', cell_center_style),
    ],
    [
        Paragraph('Offline Support', cell_center_style),
        Paragraph('Full', cell_center_style),
        Paragraph('Requires Wi-Fi', cell_center_style),
    ],
    [
        Paragraph('Recommended For', cell_center_style),
        Paragraph('High-end deployments', cell_center_style),
        Paragraph('General use, home setup', cell_center_style),
    ],
]
story.append(make_table(opts_data, [0.25, 0.375, 0.375], available_width))
story.append(Spacer(1, 6))
story.append(Paragraph('<b>Table 2:</b> AI Brain Host Options Comparison', caption_style))
story.append(Spacer(1, 18))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4: PHASE 2 - THE EYES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('4. Phase 2: The Eyes (Computer Vision)', h1_style, 0),
    Paragraph(
        'The computer vision subsystem is responsible for transforming raw camera frames into structured '
        'data that the AI agent can reason about. This phase covers the entire visual pipeline, from '
        'model selection and conversion to real-time integration with the Flutter camera and the '
        'implementation of the critical fall detection logic. The vision system must operate with minimal '
        'latency, as safety-critical applications demand real-time or near-real-time analysis of the '
        'user\'s environment. A delay of even a few seconds could mean the difference between a timely '
        'alert and a missed emergency.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('4.1 Model Selection and Preparation', h2_style, 1),
    Paragraph(
        'The Ultralytics YOLOv8 family provides a range of models optimized for different trade-offs '
        'between speed and accuracy. For The Guard, the Nano variant (yolov8n.pt) is the recommended '
        'starting point. At approximately 6.3 million parameters, it achieves inference speeds of over '
        '100 frames per second on modern smartphone CPUs while maintaining sufficient accuracy for person '
        'detection and basic scene understanding. For devices with dedicated NPUs, the Small variant '
        '(yolov8s.pt) can be considered for improved accuracy at the cost of higher computational demand.',
        body_style
    ),
    Paragraph(
        'The downloaded PyTorch model (.pt file) must be converted to a mobile-friendly format. The '
        'recommended pipeline involves exporting the model to TensorFlow Lite (.tflite) format using '
        'Ultralytics\' built-in export function. This conversion optimizes the model\'s computational '
        'graph for mobile inference, applying operator fusion, quantization (INT8 where supported), '
        'and layout optimization. The resulting .tflite file is typically 5-15 MB, making it practical '
        'for inclusion in the application bundle without excessive download sizes.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('4.2 Flutter Integration', h2_style, 1),
    Paragraph(
        'Integrating YOLOv8 with the Flutter camera requires the tflite_flutter package, which provides '
        'Dart bindings for the TensorFlow Lite runtime. The application opens a camera stream using the '
        'official camera package, processes each frame through the TFLite interpreter, and overlays '
        'bounding boxes on a custom painter widget. The detectObjects function is the core of this '
        'module, accepting a CameraImage and returning a list of detected objects with their class '
        'labels, confidence scores, and bounding box coordinates. The function must be optimized to '
        'run asynchronously, ensuring that the camera preview remains smooth at 30+ FPS while the '
        'detection runs on a separate isolate or thread.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('4.3 Fall Detection Logic', h2_style, 1),
    Paragraph(
        'Standard YOLOv8 detects objects such as "person" with high reliability, but it does not natively '
        'detect falls. The fall detection capability is implemented as a logic layer built on top of the '
        'person tracking output. The system tracks the bounding box of each detected person across '
        'consecutive frames, analyzing changes in the box\'s geometry to infer the person\'s posture '
        'and movement.',
        body_style
    ),
    Paragraph(
        'The core algorithm monitors the ratio of the bounding box\'s height to its width over time. '
        'Under normal conditions (a standing or walking person), the height significantly exceeds the '
        'width. When a person falls, the vertical dimension of the bounding box decreases rapidly while '
        'the horizontal dimension either stays constant or increases, as the person transitions from an '
        'upright to a horizontal position. The system triggers a "Potential Fall Detected" alert when '
        'the height-to-width ratio drops below a calibrated threshold (typically 0.6-0.8) within a short '
        'time window (typically 1-2 seconds). To minimize false positives, the system also considers '
        'factors such as the velocity of the ratio change and the person\'s proximity to furniture or '
        'other objects that might indicate sitting down rather than falling.',
        body_style
    ),
    Spacer(1, 12),
])

# Fall detection parameters table
fall_data = [
    [
        Paragraph('<b>Parameter</b>', header_cell_style),
        Paragraph('<b>Value</b>', header_cell_style),
        Paragraph('<b>Description</b>', header_cell_style),
    ],
    [
        Paragraph('Height/Width Ratio Threshold', cell_style),
        Paragraph('0.6 - 0.8', cell_center_style),
        Paragraph('Triggers fall alert when ratio drops below this value', cell_style),
    ],
    [
        Paragraph('Time Window', cell_style),
        Paragraph('1 - 2 seconds', cell_center_style),
        Paragraph('Duration within which the ratio change must occur', cell_style),
    ],
    [
        Paragraph('Confidence Threshold', cell_style),
        Paragraph('0.85', cell_center_style),
        Paragraph('Minimum YOLO detection confidence for person class', cell_style),
    ],
    [
        Paragraph('False Positive Filter', cell_style),
        Paragraph('Context-aware', cell_center_style),
        Paragraph('Checks proximity to furniture and rate of change', cell_style),
    ],
]
story.append(make_table(fall_data, [0.30, 0.20, 0.50], available_width))
story.append(Spacer(1, 6))
story.append(Paragraph('<b>Table 3:</b> Fall Detection Parameters', caption_style))
story.append(Spacer(1, 18))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5: PHASE 3 - THE AGENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('5. Phase 3: The Agent (AI Reasoning)', h1_style, 0),
    Paragraph(
        'The Agent subsystem is what transforms The Guard from a simple motion detector into an '
        'intelligent safety companion. While traditional safety apps rely on rigid if-else logic and '
        'fixed threshold triggers, The Guard uses a local large language model to reason about detected '
        'events contextually, much like a human safety monitor would. The LLM evaluates the totality '
        'of available information, including the nature of the detected event, the user\'s recent '
        'activity patterns, environmental context, and responses to voice check-ins, to make nuanced '
        'decisions about the appropriate level of response.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('5.1 Local LLM Setup', h2_style, 1),
    Paragraph(
        'The recommended models for The Guard\'s reasoning engine are small but capable language models '
        'that can run efficiently on consumer hardware. Microsoft\'s Phi-3 Mini (3.8 billion parameters) '
        'and Google\'s Gemma 2B (2 billion parameters) are both excellent candidates, offering strong '
        'reasoning capabilities in compact form factors. When quantized to 4-bit precision using '
        'GGUF format, these models require only 2-4 GB of RAM, making them practical for on-device '
        'deployment on modern smartphones or lightweight edge servers. The models are deployed using '
        'llama.cpp, a highly optimized C++ inference engine that supports quantized models across '
        'multiple hardware platforms including ARM (mobile), x86 (desktop/server), and Apple Silicon.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('5.2 The Guard Persona (System Prompt)', h2_style, 1),
    Paragraph(
        'The LLM\'s behavior is shaped by a carefully crafted system prompt that defines its role, '
        'capabilities, and constraints. This prompt is injected at the beginning of every inference '
        'request, ensuring consistent behavior across all interactions. The Guard persona is designed '
        'to be protective, cautious, and decisive, with a clear escalation framework that maps '
        'situations to specific actions.',
        body_style
    ),
    Spacer(1, 8),
])

story.append(Paragraph(
    '<b>System Prompt:</b> "You are \'The Guard,\' a personal safety AI. Your goal is to protect the '
    'user. You receive sensory data (e.g., \'Fall detected,\' \'User unresponsive\'). Based on the '
    'severity, decide on an action: 1. Ignore (False alarm), 2. Alert User (Vibration), '
    '3. Emergency Protocol (Contact authorities/family). Respond ONLY with the action number and a '
    'short explanation."',
    callout_style
))
story.append(Spacer(1, 12))

story.extend([
    Paragraph(
        'The three-tier action framework provides a clean interface between the AI\'s reasoning and the '
        'application\'s response mechanisms. Action 1 (Ignore) is selected when the AI determines that '
        'a detected event is a false alarm, such as the user sitting down quickly or a pet triggering '
        'the motion sensor. Action 2 (Alert User) is the most common response, used when the AI detects '
        'a potentially concerning event but cannot confirm it is an emergency; this triggers a subtle '
        'vibration pattern and a voice check-in asking the user to confirm they are safe. Action 3 '
        '(Emergency Protocol) is reserved for high-confidence emergency scenarios, such as a confirmed '
        'fall followed by non-responsiveness, which triggers immediate contact with emergency services '
        'and designated family members.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('5.3 The Reasoning Loop', h2_style, 1),
    Paragraph(
        'The reasoning loop is the core operational cycle of The Guard. It begins with sensory input '
        'from the vision subsystem, flows through the LLM for contextual reasoning, and produces an '
        'action decision that is executed by the connectivity subsystem. The loop runs continuously '
        'during active monitoring mode, processing each new frame of sensory data as it arrives.',
        body_style
    ),
    Paragraph(
        'A typical scenario illustrates the loop in action. The vision subsystem detects a sudden change '
        'in the user\'s bounding box geometry consistent with a fall. This triggers a voice check-in: '
        '"Are you okay?" The system waits for a response, typically setting a timeout of 15-20 seconds. '
        'If the user responds with a designated safe phrase (such as "I\'m fine"), the LLM receives the '
        'context: "Vision detected a fall. User responded with safe phrase within 10 seconds." The LLM '
        'reasons: "The fall was likely minor. The user\'s prompt response indicates awareness and '
        'mobility. Action 1 is appropriate." If the user does not respond within the timeout, the LLM '
        'receives: "Vision detected a fall. Voice check: User did not answer within 15 seconds." The LLM '
        'reasons: "The fall combined with non-response indicates high danger. Action 3 is required." This '
        'produces the output: "Action 3: Emergency Protocol. Reasoning: High probability of injury."',
        body_style
    ),
    Spacer(1, 18),
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 6: PHASE 4 - ACTION & CONNECTIVITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('6. Phase 4: Action and Connectivity', h1_style, 0),
    Paragraph(
        'Once The Guard\'s AI agent has made a decision, the application must translate that decision '
        'into concrete actions that protect the user. This phase implements the voice interface for '
        'check-ins, the emergency contact notification system, and the GPS location sharing mechanism. '
    'The connectivity subsystem must be robust and reliable, as it represents the final link in the '
    'safety chain. A failure in this subsystem, even after the AI has correctly identified an emergency, '
    'renders the entire system ineffective.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('6.1 Voice Interface (The Check-In)', h2_style, 1),
    Paragraph(
        'The voice interface serves a dual purpose: it allows The Guard to check on the user when a '
        'potentially dangerous event is detected, and it provides the user with a hands-free way to '
        'cancel false alarms. The implementation uses the speech_to_text package in Flutter for '
        'real-time speech recognition and the flutter_tts package for text-to-speech output. When a '
        'fall or other concerning event is detected, the application uses the text-to-speech engine to '
        'ask: "Are you okay? Please say \'I\'m fine\' if you do not need help." The speech-to-text '
        'engine listens for a designated safe phrase or any spoken response. If the user says the safe '
        'phrase, the alert is cancelled. If the user says something else or does not respond within the '
        'configured timeout (default 20 seconds), the emergency protocol is activated.',
        body_style
    ),
    Paragraph(
        'The voice interface is designed to work even in noisy environments, using noise-cancellation '
        'preprocessing and multiple recognition attempts before declaring non-responsiveness. The system '
        'also accounts for users who may be disoriented or in pain after a fall, implementing a simple '
        'tap-to-confirm fallback that appears on screen alongside the voice prompt. This multi-modal '
        'approach ensures that the system does not escalate to emergency protocols due to a temporary '
        'inability to speak.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('6.2 Emergency Contacts and SMS Notification', h2_style, 1),
    Paragraph(
        'The emergency notification system uses the url_launcher and sms packages to send pre-composed '
        'alert messages to designated emergency contacts. When the AI agent triggers Action 3 (Emergency '
        'Protocol), the application constructs an SMS message using the LLM\'s reasoning output, '
        'including the GPS coordinates of the user\'s last known location, the nature of the detected '
        'event, and the user\'s response status. The message template follows a clear, actionable format:',
        body_style
    ),
    Spacer(1, 8),
])

story.append(Paragraph(
    '<b>Emergency SMS Template:</b> "The Guard AI detected a fall at [GPS Location]. '
    'User is unresponsive. Emergency services are being notified. Please respond immediately."',
    callout_style
))
story.append(Spacer(1, 12))

story.extend([
    Paragraph(
        'The application maintains a list of emergency contacts configured by the user during initial '
        'setup, with each contact assigned a priority level. Priority 1 contacts (typically immediate '
        'family members) are notified first, followed by Priority 2 contacts (close friends or neighbors) '
        'if no Priority 1 contact acknowledges the alert within a configurable time window. The system '
        'also provides an option to directly call emergency services (911 or the local equivalent) using '
        'the tel: URL scheme, bypassing the SMS system for the most urgent situations.',
        body_style
    ),
    Spacer(1, 18),
])

# Action Framework table
action_data = [
    [
        Paragraph('<b>Action Level</b>', header_cell_style),
        Paragraph('<b>Trigger</b>', header_cell_style),
        Paragraph('<b>Response</b>', header_cell_style),
    ],
    [
        Paragraph('Action 1: Ignore', cell_style),
        Paragraph('False alarm detected by AI', cell_style),
        Paragraph('No action; continue monitoring', cell_style),
    ],
    [
        Paragraph('Action 2: Alert User', cell_style),
        Paragraph('Potential concern detected', cell_style),
        Paragraph('Vibration + voice check-in ("Are you okay?")', cell_style),
    ],
    [
        Paragraph('Action 3: Emergency', cell_style),
        Paragraph('Fall + non-response confirmed', cell_style),
        Paragraph('SMS to contacts + GPS sharing + call emergency services', cell_style),
    ],
]
story.append(make_table(action_data, [0.22, 0.35, 0.43], available_width))
story.append(Spacer(1, 6))
story.append(Paragraph('<b>Table 4:</b> Three-Tier Action Framework', caption_style))
story.append(Spacer(1, 18))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 7: PHASE 5 - PRIVACY & GUARD MODE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('7. Phase 5: Privacy and Guard Mode', h1_style, 0),
    Paragraph(
        'Privacy is not an afterthought in The Guard; it is a foundational design principle that influences '
        'every architectural decision. The application is designed with a strict "zero cloud upload" policy '
        'for video and audio data. All sensitive processing happens in the device\'s memory (RAM) and is '
        'never written to persistent storage or transmitted over the network, except in the specific case '
        'of an emergency where a brief incident clip may be shared with emergency contacts. This section '
        'details the privacy architecture and introduces The Guard Mode, a specialized operating mode '
        'designed for situations where the user needs maximum safety with maximum discretion.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('7.1 Zero Cloud Upload Architecture', h2_style, 1),
    Paragraph(
        'The codebase includes explicit safeguards to ensure that video frames and audio recordings are '
        'processed exclusively in volatile memory. The camera stream is read into byte buffers that are '
        'processed by the TFLite interpreter and immediately discarded. No frame data is written to the '
        'device\'s file system unless the user explicitly enables the optional incident recording feature. '
        'Even when incident recording is enabled, the recorded clip is stored in an encrypted container '
        'on the device and is only accessible through biometric authentication. The code includes runtime '
        'assertions that verify the absence of any network requests containing frame or audio data, and '
        'these assertions are validated through automated testing on every commit.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('7.2 Black Box Mode', h2_style, 1),
    Paragraph(
        'Black Box Mode is a critical feature for users who find themselves in potentially unsafe '
        'situations where drawing attention to a safety app could be counterproductive. When activated, '
        'the phone\'s screen goes completely black, showing only a small, translucent "Guardian Shield" '
        'icon in the center of the display. Despite the appearance of being powered off, the phone '
        'continues to actively monitor the environment through the camera, analyze the audio feed, and '
        'run the AI reasoning loop in the background. If an emergency is detected, the system activates '
        'the emergency protocol silently, vibrating the phone with a coded pattern and sending alerts '
        'to emergency contacts without any visible on-screen activity.',
        body_style
    ),
    Paragraph(
        'This mode is particularly relevant for scenarios such as walking alone at night, traveling in '
        'unfamiliar areas, or situations where the user feels uncomfortable but does not want to '
        'escalate by visibly using a safety application. The Black Box Mode leverages Android\'s '
        'foreground service capabilities and iOS\'s background processing modes to maintain continuous '
        'monitoring even when the screen is off. The feature is activated through a configurable trigger, '
        'such as pressing the power button three times in quick succession or tapping a discreet widget, '
        'making it easy to activate in stressful situations without fumbling through menus.',
        body_style
    ),
    Spacer(1, 18),
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 8: GITHUB REPOSITORIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('8. Key GitHub Repositories', h1_style, 0),
    Paragraph(
        'The Guard is built on top of several outstanding open-source projects. Each of these repositories '
        'represents a critical component of the system and should be bookmarked by any developer working '
        'on this project. Understanding the capabilities, limitations, and active development status of '
        'each dependency is essential for making informed architectural decisions and troubleshooting '
        'integration issues. The following table provides a comprehensive overview of the key repositories, '
        'their roles within the system, and the specific versions or branches recommended for The Guard.',
        body_style
    ),
    Spacer(1, 12),
])

repo_data = [
    [
        Paragraph('<b>Repository</b>', header_cell_style),
        Paragraph('<b>Purpose</b>', header_cell_style),
        Paragraph('<b>Usage in The Guard</b>', header_cell_style),
    ],
    [
        Paragraph('flutter/flutter', cell_style),
        Paragraph('Cross-platform UI framework', cell_style),
        Paragraph('Frontend application, camera interface, UI widgets, and platform channels', cell_style),
    ],
    [
        Paragraph('ultralytics/ultralytics', cell_style),
        Paragraph('YOLO object detection models', cell_style),
        Paragraph('Person detection and scene analysis via YOLOv8 Nano model', cell_style),
    ],
    [
        Paragraph('ggerganov/llama.cpp', cell_style),
        Paragraph('On-device LLM inference', cell_style),
        Paragraph('Running Phi-3 Mini or Llama-3-8B locally for AI reasoning', cell_style),
    ],
    [
        Paragraph('langchain-ai/langchain', cell_style),
        Paragraph('LLM application framework', cell_style),
        Paragraph('Structuring the agent\'s logic, prompt templates, and reasoning chains', cell_style),
    ],
]
story.append(make_table(repo_data, [0.22, 0.28, 0.50], available_width))
story.append(Spacer(1, 6))
story.append(Paragraph('<b>Table 5:</b> Key Open-Source Repositories', caption_style))
story.append(Spacer(1, 18))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 9: GETTING STARTED
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
story.extend([
    add_heading('9. Getting Started: First Steps', h1_style, 0),
    Paragraph(
        'The recommended starting point for any developer embarking on The Guard project is to build '
        'a simple Flutter application that opens the camera and draws bounding boxes around detected '
        'persons in real time. This seemingly simple milestone actually exercises the entire visual '
        'pipeline, from camera initialization to model loading to inference to rendering, and provides '
        'an excellent foundation for building the more complex features described in the later phases. '
        'Once the developer can see a bounding box tracking a person smoothly across the camera feed, '
        'they have successfully built "the eyes of The Guard" and can proceed with confidence.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('9.1 Step-by-Step First Milestone', h2_style, 1),
    Paragraph(
        'Begin by creating a new Flutter project and installing the camera and tflite_flutter packages. '
        'Download the YOLOv8 Nano model from the Ultralytics repository and convert it to TFLite format '
        'using the export command. Add the converted model file to the project\'s assets directory and '
        'configure the pubspec.yaml to include it. Implement the camera preview widget, the TFLite '
        'inference function, and the bounding box overlay painter. Test the application on a physical '
        'device (emulators do not have camera access) and verify that person detection works reliably '
        'across different lighting conditions and distances. The entire first milestone can typically be '
        'completed in 2-4 days by a developer familiar with Flutter and basic machine learning concepts.',
        body_style
    ),
    Spacer(1, 12),
    add_heading('9.2 Development Timeline', h2_style, 1),
    Paragraph(
        'The complete development of The Guard, from initial concept to production-ready application, '
        'is estimated to require approximately three to six months for a solo developer, depending on '
        'prior experience with the relevant technologies. The following timeline provides a realistic '
        'breakdown of each phase, including the key deliverables and milestones that mark successful '
        'completion of each stage. The timeline assumes part-time development effort of approximately '
        '15-20 hours per week.',
        body_style
    ),
    Spacer(1, 12),
])

timeline_data = [
    [
        Paragraph('<b>Phase</b>', header_cell_style),
        Paragraph('<b>Duration</b>', header_cell_style),
        Paragraph('<b>Key Deliverable</b>', header_cell_style),
    ],
    [
        Paragraph('Phase 1: Setup', cell_style),
        Paragraph('1 - 2 weeks', cell_center_style),
        Paragraph('Configured Flutter project with camera access and LLM host ready', cell_style),
    ],
    [
        Paragraph('Phase 2: Vision', cell_style),
        Paragraph('2 - 4 weeks', cell_center_style),
        Paragraph('Real-time person detection and fall detection working on device', cell_style),
    ],
    [
        Paragraph('Phase 3: Agent', cell_style),
        Paragraph('3 - 6 weeks', cell_center_style),
        Paragraph('Local LLM reasoning with Guard persona making contextual decisions', cell_style),
    ],
    [
        Paragraph('Phase 4: Action', cell_style),
        Paragraph('2 - 3 weeks', cell_center_style),
        Paragraph('Voice check-in, SMS alerts, and emergency contact system functional', cell_style),
    ],
    [
        Paragraph('Phase 5: Privacy', cell_style),
        Paragraph('2 - 4 weeks', cell_center_style),
        Paragraph('Zero-cloud architecture verified, Black Box Mode implemented', cell_style),
    ],
]
story.append(make_table(timeline_data, [0.22, 0.18, 0.60], available_width))
story.append(Spacer(1, 6))
story.append(Paragraph('<b>Table 6:</b> Estimated Development Timeline', caption_style))
story.append(Spacer(1, 18))

story.extend([
    Paragraph(
        'Building an application that combines computer vision and large language models is at the '
        'absolute frontier of AI engineering. The Guard represents not just a product, but an opportunity '
        'to master some of the most in-demand skills in the technology industry: on-device machine '
        'learning, real-time computer vision, natural language reasoning, and mobile application '
        'development. Each phase of development builds on the last, creating a progressively more '
        'capable and intelligent system. By the end of this journey, the developer will have built '
        'a sophisticated AI application that can genuinely improve people\'s safety and well-being.',
        body_style
    ),
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BUILD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
doc.multiBuild(story)
print(f"Body PDF generated: {output_path}")
