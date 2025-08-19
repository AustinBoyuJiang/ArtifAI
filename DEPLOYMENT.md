# ArtifAI Deployment Guide

## CapRover Git Deployment

This project is configured for **Git-based deployment** using CapRover with the following setup:

### Prerequisites

1. CapRover server running
2. Domain configured (artifa.apps.austinjiang.com)
3. Git LFS installed and configured
4. Git repository connected to CapRover app

### Environment Variables

Before deploying, configure the following environment variables in CapRover dashboard:

```
SERP_API_KEY=your_serp_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Git Deployment Steps

1. **Connect Git Repository to CapRover**
   - In CapRover dashboard, go to your app
   - Navigate to "Deployment" tab
   - Connect your Git repository (GitHub/GitLab/etc.)
   - Set branch to `main`

2. **Deploy via Git Push**
   
   **Option A: Manual deployment**
   ```bash
   git add .
   git commit -m "Deploy to production"
   git push origin main
   git lfs push origin main  # Push LFS files
   ```
   
   **Option B: Using deployment script**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Automatic Deployment**
   - CapRover will automatically detect the push
   - Build using `./backend/Dockerfile` (defined in `captain-definition`)
   - Deploy the new version
   - Application available at https://artifa.apps.austinjiang.com

### Git LFS Considerations

- Model files (`*.h5`) are tracked with Git LFS
- CapRover will automatically handle LFS files during Git deployment
- No manual tar/zip uploads needed

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

### Git Deployment Best Practices

1. **Branch Strategy**
   - Use `main` branch for production deployments
   - Test changes in feature branches before merging
   - CapRover will auto-deploy on push to configured branch

2. **Git LFS Management**
   ```bash
   # Verify LFS files are tracked
   git lfs ls-files
   
   # Push LFS files
   git lfs push origin main
   ```

3. **Deployment Verification**
   - Check CapRover logs for build status
   - Verify health endpoint: `https://artifa.apps.austinjiang.com/health`
   - Monitor application logs in CapRover dashboard

### Troubleshooting

1. **Git LFS Issues**: 
   - Ensure LFS is installed: `git lfs install`
   - Verify model files: `git lfs ls-files`
   - Check LFS quota/bandwidth limits

2. **Build Failures**: 
   - Check CapRover build logs
   - Verify Dockerfile paths are correct
   - Ensure all dependencies are in requirements.txt

3. **Missing Environment Variables**: 
   - Configure in CapRover dashboard under "App Configs"
   - Application will run with limited functionality if missing

### Security Notes

- Git deployment is more secure than tar uploads
- Environment variables are not stored in repository
- Application runs as non-root user in container
- Health checks configured for monitoring