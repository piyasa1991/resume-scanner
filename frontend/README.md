# Resume Scanner Frontend

A React application for uploading and analyzing resumes using AI, built with Vite and TypeScript.

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher)
- **npm** or **yarn**

### Installation

```bash
# From the project root
make install-frontend

# Or manually
cd frontend
npm install
```

### Development

```bash
# From the project root
make dev-frontend

# Or manually
cd frontend
npm run dev
```

The frontend will be available at: http://localhost:5173

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/         # React components
│   │   ├── FileUpload/     # File upload component
│   │   ├── Analysis/       # Analysis results component
│   │   └── common/         # Shared components
│   ├── services/           # API services
│   │   └── AnalysisService.ts
│   ├── types/              # TypeScript type definitions
│   │   └── analysis.ts
│   ├── utils/              # Utility functions
│   ├── App.tsx             # Main application component
│   ├── main.tsx            # Application entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
└── index.html              # HTML entry point
```

## 🛠️ Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint

# From project root (using Make)
make dev-frontend    # Start development server
make build-frontend  # Build for production
make lint-frontend   # Run linting
```

## 🎨 Styling

This project uses **Tailwind CSS** for styling:

- **Configuration**: `tailwind.config.js`
- **PostCSS**: `postcss.config.js`
- **Global Styles**: `src/index.css`

### Adding New Styles

```css
/* In src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
@layer components {
  .btn-primary {
    @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
  }
}
```

## 🔧 Configuration

### Vite Configuration (`vite.config.ts`)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

### TypeScript Configuration (`tsconfig.json`)

The project uses strict TypeScript configuration with React-specific settings.

## 📡 API Integration

The frontend communicates with the backend API through the `AnalysisService`:

```typescript
// src/services/AnalysisService.ts
export class AnalysisService {
  private baseUrl = 'http://localhost:8000/api'

  async uploadResume(file: File): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      body: formData
    })
    
    return response.json()
  }

  async analyzeResume(data: AnalysisRequest): Promise<AnalysisResponse> {
    const response = await fetch(`${this.baseUrl}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    
    return response.json()
  }
}
```

## 🧪 Testing

```bash
# Run tests (when configured)
npm test

# Run tests in watch mode
npm run test:watch
```

## 🚀 Building for Production

```bash
# Build the application
npm run build

# Preview the build
npm run preview
```

The built files will be in the `dist/` directory, ready for deployment to static hosting services like:

- **Netlify**
- **Vercel**
- **GitHub Pages**
- **AWS S3**

## 🔍 Development Tools

### ESLint

Configuration: `eslint.config.js`

```bash
# Run linting
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

### TypeScript

The project uses strict TypeScript configuration. All components and functions should have proper type definitions.

## 📦 Dependencies

### Core Dependencies

- **React** (18.3.1) - UI framework
- **React DOM** (18.3.1) - React DOM rendering
- **Vite** (5.4.2) - Build tool and dev server

### Development Dependencies

- **TypeScript** (5.5.3) - Type checking
- **ESLint** (9.9.1) - Code linting
- **Tailwind CSS** (3.4.1) - Utility-first CSS framework
- **PostCSS** (8.4.35) - CSS processing
- **Autoprefixer** (10.4.18) - CSS vendor prefixing

## 🎯 Features

- **File Upload**: Drag-and-drop resume file upload
- **Real-time Analysis**: AI-powered resume analysis
- **ATS Compatibility**: Applicant Tracking System compatibility check
- **Job Matching**: Compare resume against job descriptions
- **Responsive Design**: Mobile-friendly interface
- **Type Safety**: Full TypeScript support

## 🔗 Backend Integration

The frontend is designed to work with the FastAPI backend:

- **API Base URL**: http://localhost:8000
- **CORS**: Configured for local development
- **File Upload**: Multipart form data
- **Error Handling**: Comprehensive error states

## 🚀 Deployment

### Static Hosting

```bash
# Build the application
npm run build

# Deploy to your preferred platform
# The dist/ directory contains the built files
```

### Environment Variables

Create a `.env` file for environment-specific configuration:

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=Resume Scanner
```

## 🤝 Contributing

1. Follow the existing code structure
2. Use TypeScript for all new code
3. Follow the established component patterns
4. Write tests for new features
5. Update documentation as needed

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/) 