import React, { useState } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faWandMagicSparkles,
  faCheckCircle,
} from '@fortawesome/free-solid-svg-icons';
import {SyncLoader} from 'react-spinners'

export default function ImageQuery({image, setImage}){
    const [imageQuery, setImageQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    
    const handleGenerateImage = async () => {
        if (!imageQuery.trim()) {
            setError('Please enter a prompt for image generation');
            return;
        }

        setLoading(true);
        setError('');
        
        try {
          const imageResponse = await axios.post(
            `${process.env.REACT_APP_BACKEND_URL}/api/v1/generate-image`,
            {
              query: imageQuery,
            },
            { responseType: 'blob' }
          );
    
          const imageURL = URL.createObjectURL(imageResponse.data);
          setImage(imageURL);
          setLoading(false);
        } catch (error) {
          setLoading(false);
          setError('Failed to generate image. Please try again.');
          console.error('Error generating image:', error);
        }
      };

    return(
        <>
        <div className="card p-6">
          <h3 className="text-2xl font-bebas text-accent">Image Generation</h3>
          <p className="text-md font-montserrat mt-3 text-slate-300">Generate post image for LinkedIn.</p>
          <div className="gap-5 mt-3">
            
            <input
              value={imageQuery}
              onChange={(e) => setImageQuery(e.target.value)}
              placeholder="Enter prompt for LinkedIn Image"
              className="w-full p-4 mt-2 bg-zinc-100 border-2 border-gray-300 rounded-xl resize-none font-montserrat text-black"
            />
            
            {error && (
                <div className="mt-2 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
                    {error}
                </div>
            )}

            <button
              onClick={handleGenerateImage}
              disabled={loading || !imageQuery.trim()}
              className={`w-1/3 flex items-center justify-center px-3 py-4 mt-2 text-white rounded-xl font-montserrat text-md ${
                  loading || !imageQuery.trim() 
                      ? 'bg-gray-400 cursor-not-allowed' 
                      : 'bg-teal-500 hover:bg-teal-600 drop-shadow-[0_0_14px_rgba(20,184,166,0.55)]'
              }`}
            >
             {loading ? (
                 <> 
                     <SyncLoader className='ml-2' size={5} color='#ffffff' />
                     Generating Image...
                 </>
             ) : (
                 <>
                     Generate Image 
                     <FontAwesomeIcon icon={faWandMagicSparkles} className="ml-2" />
                 </>
             )}
            </button>
           
          </div>
          
          {image && (
              <div>
                <div className="flex items-center mt-10 mb-3">
                    <FontAwesomeIcon icon={faCheckCircle} className="text-teal-400 mr-2" />
                    <h4 className="text-md font-montserrat font-semibold text-black">Image Generated Successfully!</h4>
                </div>
                <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <img 
                        src={image} 
                        alt="Generated LinkedIn post" 
                        className="max-w-full h-auto rounded-lg shadow-sm"
                    />
                </div>
              </div>
            )}
        </div>
        </>
    )
}
