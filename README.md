# MoodMagic - Moodboard App

A modern moodboard application that helps users create and manage visual inspiration boards.

## Project Structure

```
moodmagic/
├── frontend/     # Next.js frontend application
├── backend/      # FastAPI backend service
├── api/          # Image and text generation services
├── utils/        # Shared utilities and helpers
├── public/       # Static assets
└── firebase/     # Firebase configuration and services
```

## Features

- Create and manage moodboards
- Image and text generation capabilities
- Real-time collaboration
- Cloud storage integration
- Modern, responsive UI

## Tech Stack

- Frontend: Next.js, React, Tailwind CSS
- Backend: FastAPI
- Database: Firebase
- Image Generation: Stable Diffusion API
- Text Generation: OpenAI API

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- Firebase CLI
- Docker (optional)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   # Frontend
   cd frontend
   npm install

   # Backend
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables
4. Start the development servers:
   ```bash
   # Frontend
   cd frontend
   npm run dev

   # Backend
   cd backend
   uvicorn main:app --reload
   ```

## License

MIT 