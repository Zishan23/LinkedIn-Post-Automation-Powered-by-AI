import React from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter, Routes, Route } from "react-router-dom"
import './index.css';
import Postanalysis from './pages/Postanalysis';
import App from './App';


export default function Approuter(){
  return(
    <HashRouter basename={process.env.PUBLIC_URL || ""}>
    <Routes>
        <Route path="/" element={<App />}></Route>
        <Route path="/postanalysis" element={<Postanalysis />}></Route>
    </Routes>
    </HashRouter>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Approuter />);
