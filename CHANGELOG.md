# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
# Changelog

## [0.5.0] - 2025-03-23

### Added
- Created a new `rag_service.py` that utilizes ChromaDB and Mistral 7B model for Retrieval-Augmented Generation (RAG).
- Implemented a new RAG endpoint in the Flask API to handle RAG requests.
- Added a new `!rag` command in the Discord service for RAG functionality.

### Changed
- Updated `mistral_7b_service.py` to improve function calling handling.
- Modified the weather function parameter name from 'format' to 'unit' in `mistral_7b_service.py` for consistency.
- Changed the previous inference command in Discord service from `!test` to `!functions`.

### Fixed
- Corrected parameter naming and handling in the weather function within `mistral_7b_service.py`.

## [0.4.0] - 2025-03-22

### Added
- Implemented web scraping functionality for iee.ihu.gr to gather important information for RAG (Retrieval-Augmented Generation).
- Installed and initialized ChromaDB for storing embeddings of scraped information.
- Created a repository for ChromaDB integration (`chromadb_repo.py`).
- Implemented document embedding generation using the HIT-TMG/KaLM-embedding-multilingual-mini-v1 model.
- Added an inference function in the ChromaDB repository to retrieve similar documents from the database.
- Created a utility (`pdf_to_txt.py`) to convert PDF files to TXT format.

### Changed
- Updated the project structure to include new modules for web scraping and document processing.
- Modified the data processing pipeline to include the conversion of scraped data into embeddings.

## [0.3.0] - 2025-03-20

### Added
- Created a new utility `news.py` with functions `get_news_by_keywords` and `get_top_news` to fetch articles from major news sites and blogs.
- Integrated the new news functions as tools in `mistral_7b_service.py` for the model to call.
- Added a new utility for fetching football match updates (currently not working and needs further development).

### Changed
- Modified `discord_service.py` to handle the different format of the news API responses.
- Updated `app.py` to accommodate changes related to the news API format.
- Made a minor change to the import statements in `llama_3.1_8b_service.py`.

### Known Issues
- The football matches utility is not functioning as expected and requires further work.

## [0.2.0] - 2025-03-19
### Added
- Introduced `meltemi_service.py` for new service functionality.
- Added `krikri_service.py` to extend service capabilities.
- Created `utils/weather.py` with functions for current and forecast weather retrieval.
- Added `discord_service.py` to run the Discord bot for model inference.

### Changed
- Modified `mistral_7b_service.py` to address function calling issues, ensuring accurate weather data retrieval.
- Updated `mistral_7b_service.py` to clean the GPU's VRAM after inference.
- Changed handling of non-function calling requests in `mistral_7b_service.py`.
- Changed the path for `.env` in `weather.py` utility from relative to absolute to avoid conflicts based on inference location.

### Fixed
- Resolved function calling issues in `mistral_7b_service.py` for both current and forecast weather functionalities.
- Resolved issue with VRAM not being freed after model usage.

## [0.1.0] - 2025-03-17
### Added
- Initial project setup
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