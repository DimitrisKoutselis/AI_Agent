# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Implemented Llama 3.1-8B-Instruct model integration
- Implemented Mistral 7B model integration
- Added function calling capabilities to both models
- Created `llama_3.1_8b_service.py` for Llama model interaction
- Created `mistral_7b_service.py` for Mistral model interaction
- Implemented `get_current_weather` function as a utility for function calling
- Added support for using ollama as a backend for running the Llama model
- Added support for using vLLM as an alternative backend for improved performance

### Changed
- Updated model initialization process to support local model files for Llama
- Modified response generation to handle function calls in both services
- Adjusted query processing to incorporate function calling results
- Updated Mistral service to use the Hugging Face Transformers library
- Refactored weather function into a separate utility module

### Fixed
- Resolved issues with loading local model files for Llama
- Corrected typo in mistral_7b_service.py file

## [0.1.0] - 2023-XX-XX
### Added
- Initial project setup