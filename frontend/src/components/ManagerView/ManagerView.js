import React, { useState, useMemo } from 'react';
import './ManagerView.css';

const initialInquiries = [
  { id: 1, category: 'Technical', urgency: 'High', summary: 'Login issue on portal', email: 'john.doe@example.com' },
  { id: 2, category: 'Billing', urgency: 'Medium', summary: 'Question about recent invoice', email: 'jane.smith@example.com' },
  { id: 3, category: 'General', urgency: 'Low', summary: 'Feedback on new feature', email: 'bob.johnson@example.com' },
  { id: 4, category: 'Technical', urgency: 'Medium', summary: 'App crashing on startup', email: 'alice.brown@example.com' },
  { id: 5, category: 'Sales', urgency: 'High', summary: 'Inquiry about enterprise plan', email: 'charlie.d@example.com' },
];

const ManagerView = () => {
  const [inquiries, setInquiries] = useState(initialInquiries);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
  const [filterCategory, setFilterCategory] = useState('All');
  const [filterUrgency, setFilterUrgency] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');

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

  const getSortIndicator = (key) => {
    if (sortConfig.key === key) {
      return sortConfig.direction === 'ascending' ? ' ▲' : ' ▼';
    }
    return '';
  };

  return (
    <div className="manager-dashboard-container">
      <h1 className="welcome-greeting">Hi, Fabian!</h1>
      <p className="welcome-text">Here's a summary of the current inquiries to manage them efficiently.</p>

      {/* Filter and Search */}
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
                  <tr key={inquiry.id}>
                    <td>{inquiry.id}</td>
                    <td>{inquiry.category}</td>
                    <td>{inquiry.urgency}</td>
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
    </div>
  );
};

export default ManagerView;
