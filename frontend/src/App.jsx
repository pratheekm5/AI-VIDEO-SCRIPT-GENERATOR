import React, { useState } from 'react';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import CopyIcon from './components/CopyIcon';
import './index.css';

export default function App() {
  // State for the multi-step flow
  const [step, setStep] = useState(1); // 1: Search, 2: Transcribe, 3: Customize, 4: Result
  // State for each step's data
  const [searchQuery, setSearchQuery] = useState({ topic: '', keywords: '' });
  const [fetchedVideos, setFetchedVideos] = useState([]);
  const [selectedVideos, setSelectedVideos] = useState({});
  const [transcripts, setTranscripts] = useState([]);
  const [scriptDetails, setScriptDetails] = useState({
    host_name: '',
    channel_name: '',
    signature_lines: '',
    required_lines: '',
    additional_instructions: '',
  });
  const [finalScript, setFinalScript] = useState('');
  // Global state
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copySuccess, setCopySuccess] = useState('');
  // API base URL
  const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

  // --- API Handlers ---
  const handleSearch = async () => {
    if (!searchQuery.topic) {
      setError('Please enter a topic to search.');
      return;
    }
    setIsLoading(true);
    setError(null);
    setFetchedVideos([]);
    try {
      const response = await fetch(`${API_BASE_URL}/agent/fetch-videos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(searchQuery),
      });
      if (!response.ok) throw new Error('Failed to fetch videos.');
      const data = await response.json();
      setFetchedVideos(data.videos || []);
    } catch (e) {
      setError(e.message || 'Could not connect to the backend.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetTranscript = async () => {
    const urlsToTranscribe = Object.values(selectedVideos);
    if (urlsToTranscribe.length === 0) {
      setError('Please select at least one video to transcribe.');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/transcript/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_urls: urlsToTranscribe }),
      });
      if (!response.ok) throw new Error('Failed to get transcripts.');
      const data = await response.json();
      const successfulTranscripts = data.transcripts.filter(t => !t.startsWith("ERROR:"));
      if (successfulTranscripts.length === 0) {
        setError(data.transcripts[0] || "Could not fetch any transcripts.");
        setTranscripts([]);
      } else {
        setTranscripts(successfulTranscripts);
        setStep(3); // Move to Customize step
      }
    } catch (e) {
      setError(e.message || 'Could not connect to the backend.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateScript = async () => {
    if (!scriptDetails.host_name || !scriptDetails.channel_name) {
      setError('Host Name and Channel Name are required.');
      return;
    }
    setIsLoading(true);
    setError(null);
    const combinedInstructions = `
      ${scriptDetails.additional_instructions}
      \nIMPORTANT: The following lines MUST be included naturally somewhere in the script: "${scriptDetails.required_lines}"
    `.trim();
    const requestBody = {
      transcripts: transcripts,
      host_name: scriptDetails.host_name,
      channel_name: scriptDetails.channel_name,
      signature_lines: scriptDetails.signature_lines.split('\n').filter(line => line.trim() !== ''),
      additional_instructions: combinedInstructions,
    };
    
    try {
      const response = await fetch(`${API_BASE_URL}/agent/create-script`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to generate script.');
      }
      const data = await response.json();
      setFinalScript(data.script);
      setStep(4); // Move to Result step
    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  // --- UI Handlers ---
  const handleSearchChange = (e) => setSearchQuery({ ...searchQuery, [e.target.name]: e.target.value });
  const handleDetailChange = (e) => setScriptDetails({ ...scriptDetails, [e.target.name]: e.target.value });
  const handleVideoSelect = (video) => {
    const newSelected = { ...selectedVideos };
    if (newSelected[video.id]) {
      delete newSelected[video.id];
    } else {
      newSelected[video.id] = video.url;
    }
    setSelectedVideos(newSelected);
  };
  const copyToClipboard = () => {
    const scriptTextArea = document.createElement('textarea');
    scriptTextArea.value = finalScript;
    document.body.appendChild(scriptTextArea);
    scriptTextArea.select();
    try {
      document.execCommand('copy');
      setCopySuccess('Copied!');
      setTimeout(() => setCopySuccess(''), 2000);
    } catch (err) {
      setCopySuccess('Failed!');
    }
    document.body.removeChild(scriptTextArea);
  };
  const handleStartOver = () => {
    setStep(1);
    setSearchQuery({ topic: '', keywords: '' });
    setFetchedVideos([]);
    setSelectedVideos({});
    setTranscripts([]);
    setScriptDetails({ host_name: '', channel_name: '', signature_lines: '', required_lines: '', additional_instructions: '' });
    setFinalScript('');
    setError(null);
    setIsLoading(false);
  };
  const ProgressIndicator = () => (
    <div className="flex justify-between items-center mb-8 px-2">
      {['Search', 'Transcribe', 'Customize', 'Result'].map((name, index) => (
        <React.Fragment key={name}>
          <div className="flex flex-col items-center">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 ${step >= index + 1 ? 'bg-orange-500 border-orange-500 text-white' : 'bg-white/50 border-slate-400 text-slate-500'}`}>
              {index + 1}
            </div>
            <p className={`mt-2 text-xs font-bold ${step >= index + 1 ? 'text-slate-700' : 'text-slate-500'}`}>{name}</p>
          </div>
          {index < 3 && <div className={`flex-1 h-1 mx-2 ${step > index + 1 ? 'bg-orange-500' : 'bg-slate-400/50'}`}></div>}
        </React.Fragment>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen font-sans text-slate-800 antialiased bg-gradient-to-br from-yellow-200 via-orange-300 to-red-300 p-4">
      <div className="container mx-auto max-w-4xl">
        <header className="text-center my-6 md:my-10">
          <h1 className="text-4xl sm:text-5xl font-bold text-slate-900 tracking-tight">
            Samanvaya - AI Video Script Generator
          </h1>
          <p className="mt-3 text-lg text-slate-700">Your 4-Step Path from Idea to Final Script</p>
        </header>
        <main className="bg-white/50 backdrop-blur-xl p-6 sm:p-8 rounded-2xl shadow-lg border border-white/20 transition-all duration-500">
          <ProgressIndicator />
          <div className="mt-8">
            {isLoading && <LoadingSpinner />}
            {error && <ErrorMessage message={error} />}
            {/* Step 1: Search for Videos */}
            {step === 1 && (
              <div>
                <h2 className="text-2xl font-bold text-slate-800 mb-4">1. Find Your Inspiration</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input type="text" name="topic" placeholder="Topic (e.g., 'React Hooks')" value={searchQuery.topic} onChange={handleSearchChange} className="p-3 bg-white/60 border border-white/30 rounded-lg focus:ring-2 focus:ring-orange-500 placeholder-slate-500" />
                  <input type="text" name="keywords" placeholder="Keywords (e.g., 'tutorial, beginners')" value={searchQuery.keywords} onChange={handleSearchChange} className="p-3 bg-white/60 border border-white/30 rounded-lg focus:ring-2 focus:ring-orange-500 placeholder-slate-500" />
                </div>
                <button onClick={handleSearch} disabled={isLoading} className="mt-4 w-full bg-orange-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-orange-700 disabled:bg-orange-400 shadow-lg">Search Videos</button>
                {fetchedVideos.length > 0 && (
                  <div className="mt-8">
                    <h3 className="font-bold text-xl mb-4">Select Videos to Transcribe:</h3>
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                      {fetchedVideos.map(video => (
                        <div key={video.id} onClick={() => handleVideoSelect(video)} className={`p-2 rounded-lg cursor-pointer transition-all ${selectedVideos[video.id] ? 'ring-4 ring-orange-500' : 'ring-2 ring-transparent hover:ring-orange-300'}`}>
                          <img src={video.thumbnail} alt={video.title} className="w-full h-auto rounded-md aspect-video object-cover" />
                          <p className="text-xs mt-2 font-semibold text-slate-700 line-clamp-2">{video.title}</p>
                        </div>
                      ))}
                    </div>
                    <button onClick={() => setStep(2)} disabled={Object.keys(selectedVideos).length === 0} className="mt-6 w-full bg-green-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-700 disabled:bg-green-400 shadow-lg">Next: Get Transcripts</button>
                  </div>
                )}
              </div>
            )}
            {/* Step 2: Confirm and Get Transcript */}
            {step === 2 && (
              <div>
                <h2 className="text-2xl font-bold text-slate-800 mb-4">2. Get Transcripts</h2>
                <p className="mb-4 text-slate-600">You've selected {Object.keys(selectedVideos).length} video(s). Ready to fetch their transcripts?</p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <button onClick={() => setStep(1)} className="w-full bg-slate-900/20 text-white font-bold py-3 px-4 rounded-lg hover:bg-slate-900/30 flex-1">Back to Search</button>
                  <button onClick={handleGetTranscript} disabled={isLoading} className="w-full bg-orange-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-orange-700 disabled:bg-orange-400 shadow-lg flex-1">Get Transcripts</button>
                </div>
              </div>
            )}
            {/* Step 3: Customize Script */}
            {step === 3 && (
              <div>
                <h2 className="text-2xl font-bold text-slate-800 mb-4">3. Customize Your Script</h2>
                <div className="mb-6">
                  <label className="font-bold text-slate-700">Generated Transcript(s):</label>
                  <textarea
                    readOnly
                    value={transcripts && transcripts.length > 0 ? transcripts.join('\n\n---\n\n') : 'No transcripts available.'}
                    className="w-full h-40 p-3 mt-2 bg-white/60 border border-white/30 rounded-lg placeholder-slate-500"
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input type="text" name="host_name" placeholder="Host's Name" value={scriptDetails.host_name} onChange={handleDetailChange} className="p-3 bg-white/60 border border-white/30 rounded-lg focus:ring-2 focus:ring-orange-500 placeholder-slate-500" />
                  <input type="text" name="channel_name" placeholder="Channel Name" value={scriptDetails.channel_name} onChange={handleDetailChange} className="p-3 bg-white/60 border border-white/30 rounded-lg focus:ring-2 focus:ring-orange-500 placeholder-slate-500" />
                  <textarea name="signature_lines" placeholder="Signature Lines (one per line)" value={scriptDetails.signature_lines} onChange={handleDetailChange} className="p-3 bg-white/60 border border-white/30 rounded-lg md:col-span-2 h-20 focus:ring-2 focus:ring-orange-500 placeholder-slate-500" />
                  <textarea name="required_lines" placeholder="Lines that MUST be in the script" value={scriptDetails.required_lines} onChange={handleDetailChange} className="p-3 bg-white/60 border border-white/30 rounded-lg md:col-span-2 h-20 focus:ring-2 focus:ring-orange-500 placeholder-slate-500" />
                  <textarea name="additional_instructions" placeholder="Additional Prompt / Instructions" value={scriptDetails.additional_instructions} onChange={handleDetailChange} className="p-3 bg-white/60 border border-white/30 rounded-lg md:col-span-2 h-20 focus:ring-2 focus:ring-orange-500 placeholder-slate-500" />
                </div>
                <button onClick={handleGenerateScript} disabled={isLoading} className="mt-6 w-full bg-orange-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-orange-700 disabled:bg-orange-400 shadow-lg">✨ Generate Final Script</button>
              </div>
            )}
            {/* Step 4: Display Result */}
            {step === 4 && finalScript && (
              <div>
                <h2 className="text-3xl font-bold text-center mb-6 text-slate-800">Your Generated Script</h2>
                <div className="relative">
                  <div className="bg-black/20 p-6 rounded-lg whitespace-pre-wrap text-left leading-relaxed shadow-inner text-white/90 backdrop-blur-sm" style={{ fontFamily: 'monospace' }}>
                    {finalScript}
                  </div>
                  <button onClick={copyToClipboard} className="absolute top-2 right-2 bg-slate-900/30 text-white/80 hover:bg-slate-900/50 p-2 rounded-lg transition-all flex items-center gap-2">
                    {copySuccess ? copySuccess : <CopyIcon />}
                  </button>
                </div>
                <button onClick={handleStartOver} className="mt-6 w-full bg-orange-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-orange-700 shadow-lg">Create Another Script</button>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
