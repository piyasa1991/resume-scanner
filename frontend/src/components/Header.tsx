import React from 'react';
import { FileSearch, Zap } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-600 rounded-lg">
              <FileSearch className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent">
                Resume Scanner
              </h1>
              <p className="text-sm text-gray-600">ATS & Job Match Analyzer</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
            <Zap className="h-4 w-4 text-yellow-500" />
            <span>Powered by AI</span>
          </div>
        </div>
      </div>
    </header>
  );
};