# The Guard - Personal Safety AI

> A comprehensive technical development roadmap for building an AI-powered personal safety application that combines real-time computer vision with on-device large language model reasoning.

## Overview

**The Guard** is a privacy-first personal safety AI application designed to serve as a constant, intelligent watchdog over the user or their loved ones. By combining cutting-edge computer vision, on-device language model reasoning, and seamless emergency connectivity, The Guard represents the frontier of AI engineering applied to personal security.

## What's Inside

This repository contains the complete **Technical Development Roadmap** document (`The_Guard_Technical_Development_Roadmap.pdf`), which covers:

| Section | Description |
|---------|-------------|
| System Architecture | Hybrid Mobile Architecture with Flutter, YOLOv8, Llama.cpp, and LangChain |
| Phase 1: Setup | Flutter project initialization and AI brain host configuration |
| Phase 2: Vision | YOLOv8 integration, real-time object detection, and fall detection logic |
| Phase 3: Agent | Local LLM reasoning, Guard persona, and contextual decision-making |
| Phase 4: Action | Voice check-in interface, SMS emergency alerts, and GPS sharing |
| Phase 5: Privacy | Zero-cloud architecture and Black Box Mode |

## Architecture

```
Frontend (Flutter)          Computer Vision (YOLOv8)         AI Brain (Llama.cpp)
       |                            |                              |
       +----------------------------+------------------------------+
                                    |
                          Backend Orchestration (Python)
```

- **Frontend:** Flutter (Dart) - Cross-platform UI for iOS and Android
- **Vision:** YOLOv8 (TFLite/ONNX) - Real-time on-device object detection
- **Brain:** Llama.cpp (Phi-3 Mini) - Local LLM reasoning engine
- **Orchestration:** Python + LangChain - Vision-language coordination

## Files

| File | Description |
|------|-------------|
| `The_Guard_Technical_Development_Roadmap.pdf` | The complete 15-page roadmap document (final deliverable) |
| `generate_guard_body.py` | ReportLab Python script to regenerate the body PDF |
| `cover_guard.html` | HTML/CSS cover page source (rendered via Playwright) |
| `README.md` | This file |

## Key Technologies

- [Flutter](https://github.com/flutter/flutter) - Cross-platform UI framework
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection models
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - On-device LLM inference
- [LangChain](https://github.com/langchain-ai/langchain) - LLM application framework

## Quick Start

The recommended first milestone is to build a simple Flutter app that opens the camera and draws bounding boxes around detected persons in real time.

1. Create a new Flutter project: `flutter create the_guard_app`
2. Add camera permissions in `AndroidManifest.xml` and `Info.plist`
3. Download and convert YOLOv8 Nano to TFLite format
4. Implement `detectObjects(cameraImage)` function
5. Draw bounding boxes on a custom painter widget

## License

This roadmap document is provided as a technical reference. The open-source tools referenced (Flutter, YOLOv8, llama.cpp, LangChain) are subject to their respective licenses.
