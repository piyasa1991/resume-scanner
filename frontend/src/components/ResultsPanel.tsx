import React from 'react';
import { Clock, CheckCircle, AlertTriangle, TrendingUp } from 'lucide-react';
import { AnalysisResult } from '../App';

interface ResultsPanelProps {
  result: AnalysisResult | null;
  isAnalyzing: boolean;
}

export const ResultsPanel: React.FC<ResultsPanelProps> = ({ result, isAnalyzing }) => {
  if (isAnalyzing) {
    return (
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
        <div className="flex items-center justify-center space-x-3">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="text-lg font-medium text-gray-700">Analyzing your resume...</span>
        </div>
        <div className="mt-4 space-y-2">
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-blue-500 to-green-500 rounded-full animate-pulse"></div>
          </div>
          <p className="text-sm text-gray-600 text-center">This usually takes a few seconds</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 text-center">
        <div className="mb-4">
          <TrendingUp className="h-16 w-16 text-gray-300 mx-auto" />
        </div>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">Ready to Analyze</h3>
        <p className="text-gray-500">
          Upload your resume and choose an analysis type to get started.
        </p>
        <div className="mt-6 grid grid-cols-1 gap-4">
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
            <h4 className="font-medium text-blue-900 mb-1">ATS Health Check</h4>
            <p className="text-sm text-blue-700">Analyze resume structure, formatting, and ATS compatibility</p>
          </div>
          <div className="p-4 bg-green-50 rounded-lg border border-green-100">
            <h4 className="font-medium text-green-900 mb-1">Job Match Analysis</h4>
            <p className="text-sm text-green-700">Compare resume against specific job requirements</p>
          </div>
        </div>
      </div>
    );
  }

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600 bg-green-100';
    if (score >= 6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 8) return <CheckCircle className="h-5 w-5" />;
    return <AlertTriangle className="h-5 w-5" />;
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-semibold text-gray-900">
            {result.mode === 'ats' ? 'ATS Health Check Results' : 'Job Match Analysis Results'}
          </h3>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Clock className="h-4 w-4" />
            <span>{result.timestamp.toLocaleTimeString()}</span>
          </div>
        </div>
        
        {(result.atsScore !== undefined || result.matchScore !== undefined) && (
          <div className="mt-4">
            <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-full ${getScoreColor(result.atsScore || result.matchScore || 0)}`}>
              {getScoreIcon(result.atsScore || result.matchScore || 0)}
              <span className="font-semibold">
                Score: {result.atsScore || result.matchScore}/10
              </span>
            </div>
          </div>
        )}
      </div>
      
      <div className="p-6">
        <div 
          className="prose max-w-none"
          dangerouslySetInnerHTML={{ __html: result.feedback }}
        />
      </div>
    </div>
  );
};