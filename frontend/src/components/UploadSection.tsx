import React, { useRef } from 'react';
import { Upload, FileText, Target, Zap } from 'lucide-react';

interface UploadSectionProps {
  resumeText: string;
  setResumeText: (text: string) => void;
  jobDescription: string;
  setJobDescription: (text: string) => void;
  onAnalysis: (mode: 'ats' | 'job-match') => void;
  isAnalyzing: boolean;
}

export const UploadSection: React.FC<UploadSectionProps> = ({
  resumeText,
  setResumeText,
  jobDescription,
  setJobDescription,
  onAnalysis,
  isAnalyzing
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (file: File) => {
    if (file.type !== 'application/pdf') {
      alert('Please upload a PDF file');
      return;
    }

    try {
      // In a real implementation, you'd use pdf-parse or PDF.js here
      // For demo purposes, we'll use a mock extraction
      const mockResumeText = `
JOHN DOE
Software Engineer
📧 john.doe@email.com | 📱 (555) 123-4567 | 🔗 linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Results-driven Software Engineer with 5+ years of experience in full-stack development, 
specializing in React, Node.js, and cloud technologies. Proven track record of delivering 
scalable web applications and leading cross-functional teams.

TECHNICAL SKILLS
• Frontend: React, TypeScript, JavaScript, HTML5, CSS3, Tailwind CSS
• Backend: Node.js, Python, Express.js, FastAPI
• Databases: PostgreSQL, MongoDB, Redis
• Cloud: AWS, Docker, Kubernetes
• Tools: Git, Webpack, Jest, CI/CD

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
• Led development of customer-facing web application serving 100k+ users
• Implemented microservices architecture reducing system downtime by 40%
• Mentored junior developers and established coding best practices
• Technologies: React, Node.js, AWS, PostgreSQL

Software Developer | StartupXYZ | 2019 - 2021
• Developed responsive web applications using modern JavaScript frameworks
• Collaborated with design team to implement pixel-perfect user interfaces
• Optimized database queries improving application performance by 60%
• Technologies: Vue.js, Python, MongoDB

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2015 - 2019

CERTIFICATIONS
• AWS Certified Solutions Architect
• Google Cloud Professional Developer

PROJECTS
• Open-source contributor to React ecosystem (2000+ GitHub stars)
• Built personal finance app with 10k+ active users
`;
      
      setResumeText(mockResumeText);
      alert('Resume uploaded successfully! (Demo version - using sample resume)');
    } catch (error) {
      console.error('Error reading file:', error);
      alert('Error reading file. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div className="p-6 border-b border-gray-100">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Upload Resume</h2>
          <p className="text-gray-600 text-sm">Upload your PDF resume to get started</p>
        </div>
        
        <div className="p-6">
          <div 
            className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 transition-colors cursor-pointer group"
            onClick={() => fileInputRef.current?.click()}
          >
            <Upload className="h-12 w-12 text-gray-400 group-hover:text-blue-500 mx-auto mb-4 transition-colors" />
            <p className="text-lg font-medium text-gray-700 mb-2">Drop your resume here</p>
            <p className="text-sm text-gray-500">or click to browse (PDF only)</p>
            
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
            />
          </div>
          
          {resumeText && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center space-x-2">
                <FileText className="h-5 w-5 text-green-600" />
                <span className="text-sm font-medium text-green-800">Resume uploaded successfully!</span>
              </div>
              <p className="text-xs text-green-600 mt-1">
                {resumeText.length} characters extracted
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div className="p-6 border-b border-gray-100">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Job Description (Optional)</h2>
          <p className="text-gray-600 text-sm">Paste the job description for targeted analysis</p>
        </div>
        
        <div className="p-6">
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here for job-specific analysis..."
            className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          />
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <button
          onClick={() => onAnalysis('ats')}
          disabled={isAnalyzing || !resumeText}
          className="flex items-center justify-center space-x-2 px-6 py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-colors"
        >
          <FileText className="h-5 w-5" />
          <span>{isAnalyzing ? 'Analyzing...' : 'ATS Health Check'}</span>
        </button>
        
        <button
          onClick={() => onAnalysis('job-match')}
          disabled={isAnalyzing || !resumeText || !jobDescription}
          className="flex items-center justify-center space-x-2 px-6 py-4 bg-green-600 hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-colors"
        >
          <Target className="h-5 w-5" />
          <span>{isAnalyzing ? 'Analyzing...' : 'Job Match Analysis'}</span>
        </button>
      </div>
    </div>
  );
};