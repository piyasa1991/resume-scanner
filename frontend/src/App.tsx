import React, { useState, useCallback, lazy, Suspense } from 'react';
import { Header } from './components/Header';
import { UploadSection } from './components/UploadSection';
import { AnalysisService } from './services/AnalysisService';

// Lazy load the ResultsPanel component for better initial load performance
const ResultsPanel = lazy(() => import('./components/ResultsPanel').then(module => ({ default: module.ResultsPanel })));

export interface AnalysisResult {
  mode: 'ats' | 'job-match';
  atsScore?: number;
  matchScore?: number;
  feedback: string;
  timestamp: Date;
}

// Loading fallback component
const LoadingFallback = () => (
  <div className="flex items-center justify-center h-64">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
);

function App() {
  const [resumeText, setResumeText] = useState<string>('');
  const [jobDescription, setJobDescription] = useState<string>('');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Memoize the analysis handler to prevent unnecessary re-renders
  const handleAnalysis = useCallback(async (mode: 'ats' | 'job-match') => {
    if (!resumeText.trim()) {
      alert('Please upload a resume first');
      return;
    }

    if (mode === 'job-match' && !jobDescription.trim()) {
      alert('Please provide a job description for job-specific analysis');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const result = await AnalysisService.analyzeResume(
        resumeText, 
        mode === 'job-match' ? jobDescription : undefined,
        mode
      );
      
      setAnalysisResult(result);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  }, [resumeText, jobDescription]);

  // Memoize the setResumeText handler
  const handleSetResumeText = useCallback((text: string) => {
    setResumeText(text);
  }, []);

  // Memoize the setJobDescription handler
  const handleSetJobDescription = useCallback((text: string) => {
    setJobDescription(text);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-optimized animate-fade-in">
      <Header />
      
      <main className="container mx-auto px-4 py-8 animate-slide-up">
        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          <UploadSection
            resumeText={resumeText}
            setResumeText={handleSetResumeText}
            jobDescription={jobDescription}
            setJobDescription={handleSetJobDescription}
            onAnalysis={handleAnalysis}
            isAnalyzing={isAnalyzing}
          />
          
          <Suspense fallback={<LoadingFallback />}>
            <ResultsPanel
              result={analysisResult}
              isAnalyzing={isAnalyzing}
            />
          </Suspense>
        </div>
      </main>
    </div>
  );
}

export default React.memo(App);