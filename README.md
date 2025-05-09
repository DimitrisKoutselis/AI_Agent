# AI Agent for University Thesis

## Overview
This project implements an intelligent AI Agent developed as part of a university thesis. The system leverages advanced natural language processing techniques to provide contextually relevant responses to user queries, with a focus on university-specific information and general utility functions.

## Architecture

### Core Components
- **LLM Engine**: Powered by Mistral 7B Instruct, providing the core reasoning capabilities
- **RAG Implementation**: Retrieval-Augmented Generation architecture using ChromaDB for knowledge retrieval
- **Function Calling**: Dynamic capability to invoke specialized functions based on query intent
- **Multilingual Support**: Complete translation pipeline using Meta's SeamlessM4T model
- **API Layer**: Flask-based REST API for service integration
- **User Interface**: Discord bot integration for conversational interaction

### Data Sources
- University website content (embedded in ChromaDB)
- Real-time weather data
- Current news articles
- Text summarization

## Technical Pipeline

1. **Input Processing**:
   - User query received via Discord or direct API call
   - Language detection and translation to English if necessary

2. **Query Processing**:
   - For general knowledge queries: RAG architecture retrieves relevant university documents
   - For functional queries: Function calling mechanism invokes appropriate utility

3. **Response Generation**:
   - LLM generates contextually appropriate response based on retrieved information
   - Translation back to original query language if needed

4. **Delivery**:
   - Response returned via Discord or API endpoint

## Key Features

### Multilingual Support
The system can understand and respond in multiple languages through a seamless translation pipeline:
- Input language detection
- Translation to English for processing
- Translation of response back to the original query language

### Function Calling
The agent can perform specialized tasks through function calling:
- Weather forecasts (current and multi-day)
- News retrieval (by location, category, or keywords)
- Text summarization with configurable parameters

### Knowledge Retrieval
The RAG architecture enables the agent to:
- Access and retrieve university-specific information
- Provide contextually relevant answers based on the university's knowledge base
- Ground responses in factual information rather than hallucinating answers

## Implementation Details

- **Vector Database**: ChromaDB with multilingual-e5-large-instruct embeddings
- **Translation Model**: Meta's SeamlessM4T for high-quality machine translation
- **API Framework**: Flask for lightweight REST API implementation
- **User Interface**: Discord service for conversational interaction

## Deployment

The system is designed with a modular architecture allowing for:
- Independent scaling of components
- Easy extension with new functions and capabilities
- Integration with additional user interfaces beyond Discord

## Academic Context

This project was developed as part of a university thesis exploring the practical applications of large language models and retrieval-augmented generation in educational contexts, with a focus on providing accurate, contextual information to university stakeholders.
