# Lightweight Image Search System

A resource-efficient image search system built with Docker, designed to run on constrained environments
(tested on 6GB RAM, 2 CPU).

## System Overview

The system consists of 5 microservices:

1. **Downloader Service**:
   - Uses Alpine Linux and curl for minimal resource usage
   - Downloads images and validates them before saving
   - Written in shell script instead of Python to minimize overhead

2. **Embedding Service**:
   - Creates simple feature vectors using ImageMagick
   - Extracts basic properties: width, height, mean brightness, standard deviation
   - Avoids heavy ML models to work within memory constraints

3. **Vector Database (Qdrant)**:
   - Runs in memory mode for better performance
   - Stores 4-dimensional vectors instead of large embeddings
   - Configured with minimal resource allocation

4. **Indexer Service**:
   - Lightweight service using Alpine Linux
   - Processes embedding files and loads them into Qdrant
   - Uses simple shell scripts and minimal Python

5. **Web UI Service**:
   - Minimal Flask application
   - Uses system curl instead of Python requests
   - Basic but functional search interface

## Service Synchronization

The current implementation uses a simple file-based synchronization mechanism where services wait for completion marker files (e.g., .download_complete, .embedding_complete) before proceeding. While this works for a proof of concept, a production environment would benefit from:
- Message queue system (like RabbitMQ or Apache Kafka) for reliable event handling
- Service-to-service communication with proper retry mechanisms
- Event tracking and monitoring
- Parallel processing capabilities
- Error recovery and dead letter queues
- Horizontal scaling support

## Why So Lean?

- Designed to run on Docker Machine with limited resources
- Avoids thread-heavy operations that can crash in constrained environments
- Uses shell scripts where possible instead of Python
- Leverages Alpine Linux for minimal container sizes
- Employs simple numerical features instead of deep learning models

## Current Features

- Simple image search based on basic image properties
- Lightweight implementation suitable for resource-constrained environments
- Real-time image search and display
- System-wide logging
- Docker-based deployment

## Limitations

- Basic image feature extraction (no deep learning)
- Search based on image properties rather than content
- In-memory vector storage (no persistence)
- Simple error handling

## Potential Improvements (for Better Resources)

1. **ML-Based Features**:
   - Replace ImageMagick features with ViT (Vision Transformer) embeddings
   - Use CLIP model for better text-to-image search
   - Implement proper image recognition capabilities

2. **Infrastructure**:
   - Use persistent storage for Qdrant
   - Advanced services sync mechanisms
   - Add monitoring and extensive logging
   - Implement proper error recovery
   - Add load balancing and scaling capabilities
   - Proper separation of concerns in web_ui:
      - Move business logic (vector generation, search) to separate modules
      - Implement proper dependency injection
      - Add service layer between web routes and business logic
      - Better error handling and validation at each layer

3. **UI Improvements**:
   - Add image upload search capability
   - Implement advanced filtering options
   - Add user management and search history

## Usage

1. Ensure Docker Machine has at least 6GB RAM and 2 CPUs
2. Place image URLs in `data/image_urls.txt`
3. Run with `docker compose up --build`
4. Access web UI at `http://<docker-machine-ip>:8080`

## Logging

System logs are collected in the logs directory. To gather all logs:
1. chmod +x collect_logs.sh
2. ./collect_logs.sh

A sample log and a sample search output are added to /logs.
