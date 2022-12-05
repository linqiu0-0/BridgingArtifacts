import React from 'react';

import './App.css';
import Mainpage from "./Mainpage";
import ZoomComponent from "./ZoomComponent";
import BridgingArtifact from "./BrdgingArtifact";

function App() {
  return (
    <div className="App">
        <ZoomComponent/>
        <div className="split right">
                <BridgingArtifact/>
        </div>
    </div>
  );
}

export default App;
