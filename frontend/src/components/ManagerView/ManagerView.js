import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import './ManagerView.css';

const ManagerView = ({ username }) => {
  const [inquiries, setInquiries] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
  const [filterCategory, setFilterCategory] = useState('All');
  const [filterUrgency, setFilterUrgency] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchInquiries = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || ''}/api/manager/inquiries`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setInquiries(data.inquiries);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchInquiries();
  }, []);

  const sortedInquiries = useMemo(() => {
    let sortableItems = [...inquiries];
    if (sortConfig.key !== null) {
      sortableItems.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [inquiries, sortConfig]);

  const filteredInquiries = useMemo(() => {
    return sortedInquiries.filter(inquiry => {
      const matchesCategory = filterCategory === 'All' || inquiry.category === filterCategory;
      const matchesUrgency = filterUrgency === 'All' || inquiry.urgency === filterUrgency;
      const matchesSearch = searchTerm === '' ||
                            Object.values(inquiry).some(value =>
                              String(value).toLowerCase().includes(searchTerm.toLowerCase())
                            );
      return matchesCategory && matchesUrgency && matchesSearch;
    });
  }, [sortedInquiries, filterCategory, filterUrgency, searchTerm]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const handleRowClick = (id) => {
    navigate(`/inquiry/${id}`);
  };

  const getSortIndicator = (key) => {
    if (sortConfig.key === key) {
      return sortConfig.direction === 'ascending' ? ' ▲' : ' ▼';
    }
    return '';
  };

  return (
    <div className="manager-dashboard-container">
      <h1 className="welcome-greeting">Hi, {username}!</h1>
      <p className="welcome-text">Here's a summary of the current inquiries to manage them efficiently.</p>

      {loading && <div className="loading-message">Loading inquiries...</div>}
      {error && <div className="error-message">Error: {error}</div>}

      {!loading && !error && (
        <>
          <div className="filter-search-section">
            <h2 className="section-title">Filter & Search:</h2>
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="filter-select"
            >
              <option value="All">All Categories</option>
              <option value="Technical">Technical</option>
              <option value="Billing">Billing</option>
              <option value="General">General</option>
              <option value="Sales">Sales</option>
            </select>
            <select
              value={filterUrgency}
              onChange={(e) => setFilterUrgency(e.target.value)}
              className="filter-select"
            >
              <option value="All">All Urgencies</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
            <input
              type="text"
              placeholder="Search inquiries..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>

          <div className="inquiries-table-section">
            <h2 className="section-title">Inquiries</h2>
            <div className="table-responsive">
              <table className="inquiries-table">
                <thead>
                  <tr>
                    <th onClick={() => requestSort('id')}>ID {getSortIndicator('id')}</th>
                    <th onClick={() => requestSort('category')}>Category {getSortIndicator('category')}</th>
                    <th onClick={() => requestSort('urgency')}>Urgency {getSortIndicator('urgency')}</th>
                    <th>Short Summary</th>
                    <th>Email</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredInquiries.length > 0 ? (
                    filteredInquiries.map((inquiry) => (
                      <tr key={inquiry.id} onClick={() => handleRowClick(inquiry.id)}>
                        <td>{inquiry.id}</td>
                        <td>{inquiry.category}</td>
                        <td>
                          <span className={`urgency-icon urgency-icon-${inquiry.urgency.toLowerCase()}`}></span>
                          {inquiry.urgency}
                        </td>
                        <td>{inquiry.summary}</td>
                        <td>{inquiry.email}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" className="no-inquiries-found">
                        No inquiries found matching your criteria.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ManagerView;
