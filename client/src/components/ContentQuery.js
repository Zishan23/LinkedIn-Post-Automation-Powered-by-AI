import React, { useState } from 'react';
import axios from 'axios';
import Markdown from 'react-markdown';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faWandMagicSparkles,
  faCheckCircle,
} from '@fortawesome/free-solid-svg-icons';
import {SyncLoader} from 'react-spinners';
import { generateMockContent } from '../config/demo';

export default function ContentQuery({ content, setContent }) {

    const [contentQuery, setContentQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleGenerateContent = async () => {
        if (!contentQuery.trim()) {
            setError('Please enter a prompt for content generation');
            return;
        }

        setLoading(true);
        setError('');
        
        try {
          // Try to use the backend first
          const contentResponse = await axios.post(
            `${process.env.REACT_APP_BACKEND_URL || 'http://localhost:5005'}/api/v1/generate-content`,
            {
              query: contentQuery,
            }
          );
          const generatedContent = contentResponse.data.content;
          setContent(generatedContent);
          setLoading(false);
        } catch (error) {
          console.log('Backend not available, using demo mode');
          // Fallback to demo mode
          const demoContent = generateMockContent(contentQuery);
          setContent(demoContent.content);
          setLoading(false);
        }
    };

    return (
        <div>
            <div className="card p-6">
                <h3 className="text-2xl font-bebas text-accent">Content Generation</h3>
                <p className="text-md font-montserrat mt-3 text-slate-300">Generate post content for LinkedIn.</p>
                <div className="gap-5 mt-3">

                    <input
                        value={contentQuery}
                        onChange={(e) => setContentQuery(e.target.value)}
                        placeholder="Enter prompt for LinkedIn post content"
                        className="w-full p-4 mt-2 bg-zinc-100 border-2 border-gray-300 rounded-xl resize-none font-montserrat text-black"
                    />
                    
                    {error && (
                        <div className="mt-2 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
                            {error}
                        </div>
                    )}

                    <button
                        onClick={handleGenerateContent}
                        disabled={loading || !contentQuery.trim()}
                        className={`w-1/3 flex items-center justify-center px-3 py-4 mt-2 text-white rounded-xl font-montserrat text-md ${
                            loading || !contentQuery.trim() 
                                ? 'bg-gray-400 cursor-not-allowed' 
                                : 'bg-teal-500 hover:bg-teal-600'
                        }`}
                    >
                        {loading ? (
                            <> 
                                <SyncLoader className='ml-2' size={5} color='#ffffff' />
                                Generating Content...
                            </>
                        ) : (
                            <>
                                Generate Content 
                                <FontAwesomeIcon icon={faWandMagicSparkles} className="ml-2" />
                            </>
                        )}
                    </button>
                </div>
            </div>
            
            {content && (
                <div className="card p-6 mt-6">
                    <div className="flex items-center mb-3">
                        <FontAwesomeIcon icon={faCheckCircle} className="text-teal-400 mr-2" />
                        <h4 className="text-md font-montserrat font-semibold text-black">Content Generated Successfully!</h4>
                    </div>
                    <div className="bg-white border border-gray-200 rounded-xl p-6 text-black">
                        <Markdown className="prose max-w-none text-black">
                            {content}
                        </Markdown>
                    </div>
                </div>
            )}
        </div>
    )
}
