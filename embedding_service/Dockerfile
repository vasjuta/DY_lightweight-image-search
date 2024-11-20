FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONTHREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1

WORKDIR /app

# Install minimal dependencies
RUN pip install --no-cache-dir \
    torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html \
    transformers==4.5.0 \
    pillow==8.2.0 \
    numpy==1.19.5

COPY create_embeddings.py .

CMD ["python", "create_embeddings.py"]