import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import CustomerView from './components/CustomerView/CustomerView';
import ManagerView from './components/ManagerView/ManagerView';
import InquiryDetailView from './components/InquiryDetailView/InquiryDetailView';
import Login from './components/Login/Login';
import './App.css'; 
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');

  const handleLoginSuccess = (loggedInUsername) => {
    setIsAuthenticated(true);
    setUsername(loggedInUsername);
  };

  return (
    <Router>
      <div>
        <ToastContainer />
        <nav className="navbar">
          <div className="navbar-container">
            <Link to="/" className="navbar-brand">Customer Inquiry Manager</Link>
            <div className="nav-links">
              <Link to="/customer" className="nav-item">Customer View</Link>
              {isAuthenticated ? (
                <Link to="/manager" className="nav-item">Manager View</Link>
              ) : (
                <Link to="/login" className="nav-item">Manager Login</Link>
              )}
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/customer" element={<CustomerView />} />
          <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
          <Route
            path="/manager"
            element={isAuthenticated ? <ManagerView username={username} /> : <Navigate to="/login" replace />}
          />
          <Route
            path="/inquiry/:id"
            element={isAuthenticated ? <InquiryDetailView /> : <Navigate to="/login" replace />}
          />
        </Routes>
      </div>
    </Router>
  );
}

const Home = () => (
  <div className="home-container">
    <h1 className="home-title">Welcome to Customer Inquiry Manager</h1>
    <p className="home-description">Please use the navigation bar above to access the Customer or Manager views.</p>
  </div>
);

export default App;