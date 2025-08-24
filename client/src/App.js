import React from 'react';
import Navbar from './components/Navbar';
import DemoBanner from './components/DemoBanner';
import Landing from './components/Landing';
import Generation from './components/Generation'

function App() {
  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      <DemoBanner />
      <div>
        <Landing />
        <Generation/>
      </div>
    </div>
  );
}

export default App;
