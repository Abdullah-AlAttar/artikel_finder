FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# # Copy the requirements file
# COPY requirements.txt .

# # Install the dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U pip setuptools wheel && \
    pip install -U pyinput pyperclip spacy  

RUN python -m spacy download de_dep_news_trf \
    python -m spacy download en_core_web_trf

# Copy the application files
COPY . .

# Set the command to run the application
CMD ["python", "artikel_finder.py"]