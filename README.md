# Text Generation Using Local LLM and AWS Deployment via Docker

## Overview
This project demonstrates how to deploy a text generation system using a local **Language Learning Model (LLM)** and **AWS EC2** using **Docker**. The system uses **FastAPI** to serve a simple API that accepts prompts from users and generates text based on those prompts using the locally deployed LLM.

## Features
- **Text Generation**: Uses a large language model (LLM) to generate text based on input prompts.
- **FastAPI**: Serves as the backend API for receiving prompts and responding with generated text.
- **Docker**: Containerizes the application for easier deployment across different environments.
- **AWS EC2**: Deploys the Dockerized app on an AWS Virtual Machine (VM) to provide a scalable, accessible platform for the API.
- **Uvicorn**: An ASGI server that serves the FastAPI app.

## Components
1. **Local LLM Setup**: The language model is hosted on an AWS EC2 instance, using HuggingFace's `transformers` library, PyTorch or TensorFlow for inference.
2. **FastAPI**: Web framework for building the API that handles incoming prompt requests and returns generated text.
3. **Docker**: Containerizes the entire application, including the FastAPI server, LLM, and dependencies.
4. **AWS EC2**: A cloud-based virtual machine to deploy the Docker container and expose the application to the internet.
5. **Uvicorn**: An ASGI server that serves the FastAPI app.

## Prerequisites
Before running the application, ensure the following dependencies are installed:
- **Python 3.7+**
- **Docker**
- **AWS Account** for setting up EC2 instances
- **FastAPI**
- **Transformers**
- **Uvicorn**

### Installing Dependencies
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/text-generation-llm-aws-docker.git
   cd text-generation-llm-aws-docker
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add necessary environment variables like the OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. Build the Docker image:
   ```bash
   docker build -t local-llm-app .
   ```

5. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 local-llm-app
   ```

6. Access the FastAPI app on your AWS instance using the public IP at port `8000` (e.g., `http://your-aws-public-ip:8000/generate-story`).

## API Endpoints
- **POST /generate-story**: Accepts a JSON object containing a `prompt` and optionally a `max_tokens` field for limiting the number of tokens in the generated response.

### Example Request Body
```json
{
  "prompt": "Tell me a story about AI",
  "max_tokens": 3000
}
```

### Example Response
```json
{
  "story": "The Oracle of Glitch sat cross-legged on a pixelated cushion, her form flickering between genders and species..."
}
```

## Dockerfile
```dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Deployment on AWS EC2
1. **Create EC2 Instance**:
   - Launch an EC2 instance using an Ubuntu AMI (Amazon Machine Image).
   - Configure security groups to allow inbound traffic on port `8000`.

2. **Install Docker on EC2**:
   - SSH into the EC2 instance and install Docker:
     ```bash
     sudo apt-get update
     sudo apt-get install docker.io
     sudo systemctl start docker
     sudo systemctl enable docker
     ```

3. **Run the Docker Container on EC2**:
   - SSH into your EC2 instance and build and run the Docker container.
     ```bash
     docker build -t local-llm-app .
     docker run -d -p 8000:8000 local-llm-app
     ```

4. **Access the FastAPI App**:
   - The FastAPI app will now be accessible at `http://your-aws-public-ip:8000`.

## Scaling and Performance
- **Scaling**: The application can be scaled horizontally using **AWS Elastic Load Balancing (ELB)** for distributing the traffic across multiple EC2 instances.
- **Caching**: For heavy traffic, implement caching strategies like Redis to cache generated text for repeated prompts.

## Security Considerations
- Use **AWS Security Groups** to restrict access to only trusted IPs or networks.
- Secure sensitive data (like API keys) using **environment variables** and **dotenv**.

## Logging and Monitoring
- Integrate logging into the application to monitor API request/response.
- Consider using AWS **CloudWatch** for centralized monitoring of the deployed EC2 instances and application logs.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
