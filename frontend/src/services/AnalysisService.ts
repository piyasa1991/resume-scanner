import { AnalysisResult } from '../App';

export class AnalysisService {
  static async analyzeResume(
    resumeText: string, 
    jobDescription?: string,
    mode: 'ats' | 'job-match' = 'ats'
  ): Promise<AnalysisResult> {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    if (mode === 'ats') {
      return this.generateATSAnalysis(resumeText);
    } else {
      return this.generateJobMatchAnalysis(resumeText, jobDescription || '');
    }
  }

  private static generateATSAnalysis(resumeText: string): AnalysisResult {
    // Mock ATS analysis based on resume content
    const score = Math.floor(Math.random() * 3) + 7; // Score between 7-10 for demo
    
    const feedback = `
      <div class="space-y-6">
        <div class="p-4 bg-green-50 border-l-4 border-green-400 rounded-r-lg">
          <h4 class="font-semibold text-green-800 mb-2">✅ Strengths</h4>
          <ul class="text-green-700 space-y-1">
            <li>• Clear contact information and professional summary</li>
            <li>• Well-structured sections (Experience, Skills, Education)</li>
            <li>• Good use of action verbs and quantified achievements</li>
            <li>• Relevant technical skills clearly listed</li>
          </ul>
        </div>

        <div class="p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r-lg">
          <h4 class="font-semibold text-yellow-800 mb-2">⚠️ Areas for Improvement</h4>
          <ul class="text-yellow-700 space-y-1">
            <li>• Consider adding a "Core Competencies" section with keywords</li>
            <li>• Include more industry-specific buzzwords</li>
            <li>• Add metrics to quantify your impact where possible</li>
          </ul>
        </div>

        <div class="p-4 bg-blue-50 border-l-4 border-blue-400 rounded-r-lg">
          <h4 class="font-semibold text-blue-800 mb-2">🚀 ATS Optimization Tips</h4>
          <ul class="text-blue-700 space-y-1">
            <li>• Use standard section headings (Experience, Education, Skills)</li>
            <li>• Avoid graphics, tables, or complex formatting</li>
            <li>• Include both acronyms and full terms (e.g., "AI" and "Artificial Intelligence")</li>
            <li>• Use keywords from job postings naturally throughout your resume</li>
          </ul>
        </div>

        <div class="p-4 bg-gray-50 rounded-lg">
          <h4 class="font-semibold text-gray-800 mb-2">📊 Format Analysis</h4>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="font-medium">Contact Info:</span> 
              <span class="text-green-600 ml-2">✅ Complete</span>
            </div>
            <div>
              <span class="font-medium">Section Headers:</span> 
              <span class="text-green-600 ml-2">✅ Standard</span>
            </div>
            <div>
              <span class="font-medium">Bullet Points:</span> 
              <span class="text-green-600 ml-2">✅ Proper Format</span>
            </div>
            <div>
              <span class="font-medium">Keywords:</span> 
              <span class="text-yellow-600 ml-2">⚠️ Could Improve</span>
            </div>
          </div>
        </div>
      </div>
    `;

    return {
      mode: 'ats',
      atsScore: score,
      feedback,
      timestamp: new Date()
    };
  }

  private static generateJobMatchAnalysis(resumeText: string, jobDescription: string): AnalysisResult {
    const score = Math.floor(Math.random() * 4) + 6; // Score between 6-10 for demo
    
    const feedback = `
      <div class="space-y-6">
        <div class="p-4 bg-green-50 border-l-4 border-green-400 rounded-r-lg">
          <h4 class="font-semibold text-green-800 mb-2">✅ Strong Matches</h4>
          <ul class="text-green-700 space-y-1">
            <li>• <strong>React & TypeScript:</strong> Direct experience matches job requirements</li>
            <li>• <strong>Full-stack Development:</strong> 5+ years aligns with "Senior" level requirement</li>
            <li>• <strong>Cloud Technologies:</strong> AWS experience matches infrastructure needs</li>
            <li>• <strong>Team Leadership:</strong> Mentoring experience shows leadership capability</li>
          </ul>
        </div>

        <div class="p-4 bg-red-50 border-l-4 border-red-400 rounded-r-lg">
          <h4 class="font-semibold text-red-800 mb-2">❌ Missing Keywords</h4>
          <ul class="text-red-700 space-y-1">
            <li>• <strong>GraphQL:</strong> Mentioned as required but not in your resume</li>
            <li>• <strong>Microservices:</strong> You have experience but not explicitly stated</li>
            <li>• <strong>Agile/Scrum:</strong> Important methodology not mentioned</li>
            <li>• <strong>Testing (Jest/Cypress):</strong> QA experience should be highlighted</li>
          </ul>
        </div>

        <div class="p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r-lg">
          <h4 class="font-semibold text-yellow-800 mb-2">⚠️ Partial Matches</h4>
          <ul class="text-yellow-700 space-y-1">
            <li>• <strong>Database Experience:</strong> You have PostgreSQL, they prefer MySQL</li>
            <li>• <strong>Mobile Development:</strong> React Native would strengthen your profile</li>
            <li>• <strong>DevOps:</strong> Docker mentioned but CI/CD pipeline experience unclear</li>
          </ul>
        </div>

        <div class="p-4 bg-blue-50 border-l-4 border-blue-400 rounded-r-lg">
          <h4 class="font-semibold text-blue-800 mb-2">🚀 Recommendations</h4>
          <ul class="text-blue-700 space-y-1">
            <li>• Add "GraphQL" to your technical skills section</li>
            <li>• Explicitly mention "microservices architecture" in your TechCorp experience</li>
            <li>• Include "Agile methodology" and "Scrum practices" in your experience</li>
            <li>• Highlight testing frameworks usage in your projects</li>
            <li>• Consider adding any mobile development experience if applicable</li>
          </ul>
        </div>

        <div class="p-4 bg-gray-50 rounded-lg">
          <h4 class="font-semibold text-gray-800 mb-2">📈 Keyword Match Analysis</h4>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium">Technical Skills Match</span>
              <div class="flex items-center space-x-2">
                <div class="w-32 bg-gray-200 rounded-full h-2">
                  <div class="bg-green-500 h-2 rounded-full" style="width: 75%"></div>
                </div>
                <span class="text-sm text-gray-600">75%</span>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium">Experience Level</span>
              <div class="flex items-center space-x-2">
                <div class="w-32 bg-gray-200 rounded-full h-2">
                  <div class="bg-green-500 h-2 rounded-full" style="width: 90%"></div>
                </div>
                <span class="text-sm text-gray-600">90%</span>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium">Industry Keywords</span>
              <div class="flex items-center space-x-2">
                <div class="w-32 bg-gray-200 rounded-full h-2">
                  <div class="bg-yellow-500 h-2 rounded-full" style="width: 60%"></div>
                </div>
                <span class="text-sm text-gray-600">60%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    return {
      mode: 'job-match',
      matchScore: score,
      feedback,
      timestamp: new Date()
    };
  }
}