import React from 'react';
import { showDemoMode } from '../config/demo';

const DemoBanner = () => {
  const demoInfo = showDemoMode();

  return (
    <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 shadow-lg">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-white/20 rounded-full p-2">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-lg">{demoInfo.title}</h3>
              <p className="text-sm text-blue-100">{demoInfo.description}</p>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="bg-white/20 rounded-lg p-3">
              <h4 className="font-medium text-sm mb-2">Demo Features:</h4>
              <ul className="text-xs space-y-1">
                {demoInfo.features.map((feature, index) => (
                  <li key={index} className="flex items-center space-x-2">
                    <span className="w-1.5 h-1.5 bg-green-400 rounded-full"></span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DemoBanner; 