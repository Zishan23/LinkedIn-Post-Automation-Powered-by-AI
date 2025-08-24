import React, { useState } from 'react';
import axios from 'axios';
import Markdown from 'react-markdown';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faLinkedin,
} from '@fortawesome/free-brands-svg-icons';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { SyncLoader } from 'react-spinners';
import { mockLinkedInPost } from '../config/demo';

export default function Preview({ content, image, selectedDays }) {
    const [showPreview, setShowPreview] = useState(false);
    const [posting, setPosting] = useState(false);
    const [postStatus, setPostStatus] = useState('');

    const handlePostToLinkedIn = async () => {
        if (!content || !image) {
            setPostStatus('Please generate both content and image first');
            return;
        }

        setPosting(true);
        setPostStatus('Posting to LinkedIn...');

        try {
            // Try to use the backend first
            const response = await axios.post(
                `${process.env.REACT_APP_BACKEND_URL || 'http://localhost:5005'}/api/v1/post-linkedin`,
                {
                    generated_content: content,
                    image_path: 'generated_image.png' // This would be the actual image path
                }
            );

            if (response.data.success) {
                setPostStatus('Successfully posted to LinkedIn! 🎉');
            } else {
                setPostStatus(`Failed to post to LinkedIn: ${response.data.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.log('Backend not available, using demo mode');
            // Fallback to demo mode
            const demoPost = mockLinkedInPost(content, image);
            setPostStatus(`Demo: ${demoPost.message} 🎭`);
        } finally {
            setPosting(false);
        }
    };

    const hasContent = content && image;

    return (
        <div className="mt-8 card p-6" >
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-bebas">Preview & Post</h3>
                <button
                    onClick={() => setShowPreview(!showPreview)}
                    className="flex items-center px-4 py-2 text-teal-400 hover:text-teal-300 font-montserrat"
                >
                    <FontAwesomeIcon 
                        icon={showPreview ? faEyeSlash : faEye} 
                        className="mr-2" 
                    />
                    {showPreview ? 'Hide Preview' : 'Show Preview'}
                </button>
            </div>

            {!hasContent && (
                <div className="text-center py-8 text-gray-500">
                    <p className="text-lg">Generate both content and image to see the preview</p>
                </div>
            )}

            {hasContent && showPreview && (
                <div className="space-y-6">
                    {/* Content Preview */}
                    <div className="bg-gray-50 rounded-lg p-4">
                        <h4 className="text-lg font-semibold mb-3 text-gray-800">Content Preview:</h4>
                        <div className="bg-white rounded-lg p-4 border">
                            <Markdown className="prose max-w-none text-black">
                                {content}
                            </Markdown>
                        </div>
                    </div>

                    {/* Image Preview */}
                    <div className="bg-gray-50 rounded-lg p-4">
                        <h4 className="text-lg font-semibold mb-3 text-gray-800">Image Preview:</h4>
                        <div className="bg-white rounded-lg p-4 border">
                            <img 
                                src={image} 
                                alt="Generated LinkedIn post" 
                                className="max-w-full h-auto rounded-lg shadow-sm"
                            />
                        </div>
                    </div>

                    {/* Posting Controls */}
                    <div className="bg-teal-50 rounded-lg p-4">
                        <h4 className="text-lg font-semibold mb-3 text-teal-800">Ready to Post?</h4>
                        <p className="text-teal-700 mb-4">
                            This post will be scheduled for {selectedDays} day{selectedDays > 1 ? 's' : ''} from now.
                        </p>
                        
                        <button
                            onClick={handlePostToLinkedIn}
                            disabled={posting}
                            className={`flex items-center px-6 py-3 text-white rounded-xl font-montserrat font-semibold ${
                                posting 
                                    ? 'bg-gray-400 cursor-not-allowed' 
                                    : 'bg-teal-500 hover:bg-teal-600 drop-shadow-[0_0_14px_rgba(20,184,166,0.55)]'
                            }`}
                        >
                            {posting ? (
                                <>
                                    <SyncLoader size={8} color="#ffffff" className="mr-2" />
                                    Posting...
                                </>
                            ) : (
                                <>
                                    <FontAwesomeIcon icon={faLinkedin} className="mr-2" />
                                    Post to LinkedIn
                                </>
                            )}
                        </button>

                        {postStatus && (
                            <div className={`mt-3 p-3 rounded-lg ${
                                postStatus.includes('Success') 
                                    ? 'bg-green-100 text-green-800' 
                                    : postStatus.includes('Error') 
                                        ? 'bg-red-100 text-red-800'
                                        : 'bg-blue-100 text-blue-800'
                            }`}>
                                {postStatus}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {hasContent && !showPreview && (
                <div className="text-center py-8">
                    <button
                        onClick={() => setShowPreview(true)}
                        className="px-6 py-3 bg-teal-500 hover:bg-teal-600 text-white rounded-xl font-montserrat font-semibold"
                    >
                        <FontAwesomeIcon icon={faEye} className="mr-2" />
                        Preview Your LinkedIn Post
                    </button>
                </div>
            )}
        </div>
    );
} 