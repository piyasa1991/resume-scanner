import React, { useState } from 'react';
import { Header } from './components/Header';
import { UploadSection } from './components/UploadSection';
import { ResultsPanel } from './components/ResultsPanel';
import { AnalysisService } from './services/AnalysisService';

export interface AnalysisResult {
  mode: 'ats' | 'job-match';
  atsScore?: number;
  matchScore?: number;
  feedback: string;
  timestamp: Date;
}

function App() {
  const [resumeText, setResumeText] = useState<string>('');
  const [jobDescription, setJobDescription] = useState<string>('');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalysis = async (mode: 'ats' | 'job-match') => {
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
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          <UploadSection
            resumeText={resumeText}
            setResumeText={setResumeText}
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            onAnalysis={handleAnalysis}
            isAnalyzing={isAnalyzing}
          />
          
          <ResultsPanel
            result={analysisResult}
            isAnalyzing={isAnalyzing}
          />
        </div>
      </main>
    </div>
  );
}

export default App;