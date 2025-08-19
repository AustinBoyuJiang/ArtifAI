# ArtifAI Deployment Guide

## CapRover Deployment

This project is configured for deployment using CapRover with the following setup:

### Prerequisites

1. CapRover server running
2. Domain configured (artifa.apps.austinjiang.com)
3. Git LFS installed and configured

### Environment Variables

Before deploying, configure the following environment variables in CapRover:

```
SERP_API_KEY=your_serp_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Deployment Steps

1. **Push to Git Repository**
   ```bash
   git add .
   git commit -m "Deploy to production"
   git push origin main
   ```

2. **Deploy via CapRover**
   - The `captain-definition` file is configured to use `./backend/Dockerfile`
   - CapRover will automatically build and deploy the application
   - The application will be available at https://artifa.apps.austinjiang.com

### File Structure

```
/
├── captain-definition          # CapRover deployment config
├── backend/
│   ├── Dockerfile             # Container configuration
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── gunicorn.conf.py      # Gunicorn configuration
│   ├── .env.example          # Environment variables template
│   └── models/
│       └── model.h5          # AI model (managed by Git LFS)
└── frontend/                  # React frontend (separate deployment)
```

### API Endpoints

- `GET /` - Root endpoint with service info
- `GET /health` - Health check endpoint
- `POST /detect` - Image AI detection
- `POST /query` - GPT consultation

### Troubleshooting

1. **Missing Environment Variables**: The application will run but some features will be disabled
2. **Model Loading Issues**: Ensure Git LFS is properly configured
3. **Build Failures**: Check Docker logs in CapRover dashboard

### Security Notes

- The application runs as a non-root user
- Environment variables are not stored in the repository
- Health checks are configured for monitoring